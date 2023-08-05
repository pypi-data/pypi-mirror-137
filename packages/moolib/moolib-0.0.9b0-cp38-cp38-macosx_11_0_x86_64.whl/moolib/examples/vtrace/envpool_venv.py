import dataclasses
import multiprocessing as mp
from typing import Callable


import gym
import torch


STEP = 0
RESET = 1
CLOSE = 2


def worker(conn, env):
    while True:
        cmd, data = conn.recv()
        if cmd == STEP:
            obs, reward, done, info = env.step(data)
            if done:
                obs = env.reset()
            conn.send((obs, reward, done, info))
        elif cmd == RESET:
            obs = env.reset()
            conn.send(obs)
        elif cmd == CLOSE:
            env.close()
            conn.send(True)
            break
        else:
            raise NotImplementedError


class ParallelEnv(gym.Env):
    """A concurrent execution of environments in multiple processes."""

    def __init__(self, envs):
        assert len(envs) >= 1, "No environment given."

        self.envs = envs
        self.observation_space = self.envs[0].observation_space
        self.action_space = self.envs[0].action_space

        self.procs = []

        self.locals = []
        for env in self.envs[1:]:
            local, remote = mp.Pipe()
            self.locals.append(local)
            p = mp.Process(target=worker, args=(remote, env))
            self.procs.append(p)
            p.start()
            remote.close()

        self.stepping = False

    def reset(self):
        for local in self.locals:
            local.send((RESET, None))
        results = [local.recv() for local in self.locals]
        return results

    def step_async(self, actions):
        assert not self.stepping
        for local, action in zip(self.locals, actions):
            local.send((STEP, action))
        self.stepping = True

    def step_wait(self):
        assert self.stepping
        results = zip(*[local.recv() for local in self.locals])
        self.stepping = False
        return results

    def render(self):
        raise NotImplementedError

    def close(self):
        for local in self.locals:
            local.send((CLOSE, None))
        for p in self.procs:
            p.join(2)
            if p.exitcode is None:
                raise RuntimeError("Worker %s didn't finish" % p)


def from_numpy(values):
    return [torch.from_numpy(v) for v in values]  # Could be a nest.map.


class EnvPool:
    @dataclasses.dataclass
    class Future:
        result: Callable

    def __init__(self, create_env, num_processes, batch_size, num_batches=2):
        # Could not require this, but do for now.
        assert batch_size * num_batches == num_processes

        self.venvs = [
            ParallelEnv([create_env() for _ in range(batch_size)])
            for _ in range(num_batches)
        ]

    def step(self, index, actions):
        venv = self.venvs[index]
        venv.step_async(actions)
        return Future(lambda: from_numpy(venv.step_wait()))
