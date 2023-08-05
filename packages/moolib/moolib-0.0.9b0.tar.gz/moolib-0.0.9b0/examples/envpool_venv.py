import dataclasses
import multiprocessing as mp
from typing import Callable
import weakref


import gym
import torch


STEP = 0
RESET = 1
CLOSE = 2


def worker(conn, env):
    print("Here's a worker")
    try:
        while True:
            cmd, data = conn.recv()
            if cmd == STEP:
                obs, reward, done, info = env.step(data)
                new_obs = None
                if done:
                    new_obs = env.reset()
                conn.send((obs, reward, done, new_obs, info))
            elif cmd == RESET:
                obs = env.reset()
                conn.send(obs)
            elif cmd == CLOSE:
                env.close()
                conn.send(True)
                break
            else:
                raise NotImplementedError
    except KeyboardInterrupt:
        return


class ParallelEnv(gym.Env):
    """A concurrent execution of environments in multiple processes."""

    def __init__(self, envs):
        assert len(envs) >= 1, "No environment given."

        self.envs = envs
        self.procs = []
        self.locals = []

        ctx = mp.get_context("fork")

        for env in self.envs:
            local, remote = ctx.Pipe()
            self.locals.append(local)
            p = ctx.Process(target=worker, args=(remote, env))
            self.procs.append(p)
            p.start()
            remote.close()

        self.stepping = False
        self.resetting = False

    def reset_async(self):
        assert not self.resetting
        for local in self.locals:
            local.send((RESET, None))
        self.resetting = True

    def reset_wait(self):
        assert self.resetting
        results = [local.recv() for local in self.locals]
        self.resetting = False
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


def _close(venvs):
    for venv in venvs:
        venv.close()


class EnvPool:
    @dataclasses.dataclass
    class Future:
        venv: ParallelEnv

        def result(self):
            obs, reward, done, new_obs, _ = self.venv.step_wait()
            return {
                "state": torch.stack([torch.from_numpy(o) for o in obs]),
                "new_obs": new_obs,
                "reward": torch.Tensor(reward),
                "done": torch.Tensor(done).to(torch.bool),
            }

    def __init__(self, create_env, num_processes, batch_size, num_batches=2):
        # Could not require this, but do for now.
        assert batch_size * num_batches == num_processes

        self.venvs = [
            ParallelEnv([create_env() for _ in range(batch_size)])
            for _ in range(num_batches)
        ]
        for e in self.venvs:
            e.reset_async()
            e.reset_wait()
        weakref.finalize(self, _close, self.venvs)

    def step(self, index, actions):
        venv = self.venvs[index]
        venv.step_async(actions.numpy())
        return EnvPool.Future(venv)
