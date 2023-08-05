import time
import argparse
import copy
import random

import torch
import moolib
import gym
from torch import nn
from torch.nn import functional as F

import vtrace
import atari_wrappers
import models
import atari_preprocessing


def boolarg(x):
    if str(x).lower() in ["true", "yes", "on", "1", "y"]:
        return True
    if str(x).lower() in ["false", "no", "off", "0", "n"]:
        return False
    raise RuntimeError("Unknown bool value " + str(x))


parser = argparse.ArgumentParser(description="hello world")

parser.add_argument(
    "broker_address", default="", type=str, help="Broker server address"
)

parser.add_argument("group", default="", type=str, help="Broker group")

# Loss settings.
parser.add_argument(
    "--entropy_cost", default=0.0006, type=float, help="Entropy cost/multiplier."
)
parser.add_argument(
    "--baseline_cost", default=0.5, type=float, help="Baseline cost/multiplier."
)
parser.add_argument(
    "--discounting", default=0.99, type=float, help="Discounting factor."
)
parser.add_argument(
    "--reward_clipping",
    default="abs_one",
    choices=["abs_one", "none"],
    help="Reward clipping.",
)

# Training settings.
parser.add_argument(
    "--batch_size", default=32, type=int, metavar="B", help="Learner batch size."
)
parser.add_argument(
    "--actor_batch_size", default=32, type=int, metavar="B", help="Actor batch size."
)
parser.add_argument(
    "--unroll_length",
    default=20,
    type=int,
    metavar="T",
    help="The unroll length (time dimension).",
)
parser.add_argument(
    "--total_steps",
    default=5e7,
    type=int,
    metavar="T",
    help="Total environment steps to train for.",
)
parser.add_argument(
    "--num_actors", default=4, type=int, metavar="N", help="Number of actors."
)

# Optimizer settings.
parser.add_argument(
    "--learning_rate", default=0.0006, type=float, metavar="LR", help="Learning rate."
)
parser.add_argument(
    "--alpha", default=0.99, type=float, help="RMSProp smoothing constant."
)
parser.add_argument("--momentum", default=0, type=float, help="RMSProp momentum.")
parser.add_argument("--epsilon", default=0.01, type=float, help="RMSProp epsilon.")
parser.add_argument(
    "--grad_norm_clipping", default=40.0, type=float, help="Global gradient norm clip."
)

parser.add_argument("--env", default="Pong", type=str, help="Gym environment.")
parser.add_argument("--env_version", default="v4", type=str, help="Gym env version.")


parser.add_argument("--use_lstm", default=False, type=boolarg, help="Use lstm")

parser.add_argument("--wandb", default=False, type=boolarg, help="Use wandb")

parser.add_argument(
    "--warmup_time", default=20, type=float, help="Warmup time in seconds"
)


flags = parser.parse_args()

moolib.set_log_level("verbose")

wandb = None
if flags.wandb:
    import wandb

    wandb.init(project="moolib-atari-" + flags.group)
    wandb.config.flags = flags


def compute_baseline_loss(advantages):
    return 0.5 * torch.sum(advantages**2)


def compute_entropy_loss(logits):
    """Return the entropy loss, i.e., the negative entropy of the policy."""
    policy = F.softmax(logits, dim=-1)
    log_policy = F.log_softmax(logits, dim=-1)
    return torch.sum(policy * log_policy)


def compute_policy_gradient_loss(logits, actions, advantages):
    cross_entropy = F.nll_loss(
        F.log_softmax(torch.flatten(logits, 0, 1), dim=-1),
        target=torch.flatten(actions, 0, 1),
        reduction="none",
    )
    cross_entropy = cross_entropy.view_as(advantages)
    return torch.sum(cross_entropy * advantages.detach())


use_new_wrapper = False


def create_env():
    full_env_name = "%sNoFrameskip-%s" % (flags.env, flags.env_version)
    if use_new_wrapper:
        return atari_wrappers.wrap_pytorch(
            atari_preprocessing.AtariPreprocessing(
                gym.make(full_env_name), max_random_noops=30
            )
        )
    else:
        return atari_wrappers.wrap_pytorch(
            atari_wrappers.wrap_deepmind(
                atari_wrappers.make_atari(full_env_name),
                clip_rewards=False,
                frame_stack=True,
                scale=False,
            )
        )


# EnvPool runs a batch of environments in separate processes, create_env is a user-defined function that returns a gym environment.
# the num_actors parameter is how many *processes* should be used for running environments, but the total number of environments
# that are ran depends on the batch size of the actions that are passed
env_pool = moolib.EnvPool(create_env, flags.num_actors)

device = torch.device("cuda:0")
# device = torch.device("cpu")

num_actions = create_env().action_space.n

model = models.Net(
    num_actions=num_actions,
    input_channels=1 if use_new_wrapper else 4,
    use_lstm=flags.use_lstm,
).to(device)
# model = torch.jit.script(model)

if wandb is not None:
    wandb.watch(model)

total_parameters = 0
for m in model.parameters():
    total_parameters += m.numel()
print("Model total parameters: %d" % total_parameters)

# accumulator = moolib.Accumulator(model.parameters(), model.buffers())
peer = moolib.Rpc()
group = moolib.Group(peer, "broker", flags.group, 10)
accumulator = moolib.Accumulator(group, "model", model.parameters(), model.buffers())

# accumulator.set_min_batch_size(256)
# accumulator.set_max_gradient_reductions(2)

peer.connect(flags.broker_address)

optimizer = torch.optim.RMSprop(
    model.parameters(),
    lr=flags.learning_rate,
    momentum=flags.momentum,
    eps=flags.epsilon,
    alpha=flags.alpha,
)


def lr_lambda(epoch):
    return (
        1
        - min(epoch * flags.unroll_length * flags.batch_size, flags.total_steps)
        / flags.total_steps
    )


scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


class Queue:
    def __init__(self):
        self.state = []
        self.reward = []
        self.done = []
        self.logits = []
        self.v = []
        self.action = []
        self.core_state = []


class SimpleQueue:
    def __init__(self):
        self.queue = []

    def push(self, data):
        if len(self.queue) < 16:
            self.queue.append(data)
        else:
            print("Warning: queue is full, discarding data")

    def empty(self):
        return len(self.queue) == 0

    def pop(self):
        return self.queue.pop(0)


# learn_queue = ReplayBuffer(10000)
learn_queue = SimpleQueue()

# EnvSet is used below to step through multiple sets of environments in parallel, so we can run
# model.forward for one set while stepping through another set.
# This is necessary for efficient GPU & CPU utilization
class EnvSet:
    def __init__(self, index):
        # This first envs.step call creates the environments and sets the batch size.
        # The actual action values that are passed in are not used.
        self.index = index
        self.future = envs.step(index, torch.zeros(flags.actor_batch_size).long())
        self.running_reward = torch.zeros(flags.actor_batch_size, 1)
        self.step_count = torch.zeros(flags.actor_batch_size, 1)
        self.queue = Queue()
        self.core_state = model.initial_state(batch_size=flags.actor_batch_size)
        self.core_state = tuple(s.to(device) for s in self.core_state)
        self.initial_core_state = self.core_state


envs = env_pool.spawn()

env_sets = []
env_set_index = 0

for i in range(1):
    env_sets.append(EnvSet(i))

lastprint = time.time()

episodes_done = 0
opt_steps = 0
env_steps = 0
donesteps = 0
donerewards = 0
donecount = 0
laststeps = 0
running_sps = 0

prev_meandonerewards = 0
total_loss = None

print("Warming up environments...")
start_time = time.time()
while time.time() - start_time < flags.warmup_time:
    for index, cur_set in enumerate(env_sets):
        _ = cur_set.future.result()
        cur_set.future = envs.step(
            index,
            torch.randint(low=0, high=num_actions, size=(flags.actor_batch_size,)),
        )
print("Warmed up!")

while True:
    if accumulator.connected():
        cur_index = env_set_index
        cur_set = env_sets[cur_index]
        env_set_index = (cur_index + 1) % len(env_sets)

        obs = cur_set.future.result()
        env_steps += flags.actor_batch_size

        # tensors in obs need to be copied as they point into shared memory which will
        # be overwritten by future env steps
        reward = (
            obs["rewards"].squeeze(1).to(device=device, copy=True, non_blocking=True)
        )
        state = obs["state"].to(device=device, copy=True, non_blocking=True)
        done = obs["done"].squeeze(1).to(device=device, copy=True, non_blocking=True)

        with torch.no_grad():
            model.eval()
            prev_core_state = cur_set.core_state
            (action, logits, v), cur_set.core_state = model.forward(
                state.unsqueeze(0),
                reward.unsqueeze(0),
                done.unsqueeze(0),
                cur_set.core_state,
            )
            logits = logits.squeeze(0)
            v = v.squeeze(0)
            action = action.squeeze(0)
        # envs.step will asynchronously copy action from the gpu to the cpu
        cur_set.future = envs.step(cur_set.index, action)

        queue = cur_set.queue
        queue.state.append(state)
        queue.reward.append(reward)
        queue.done.append(done)
        queue.logits.append(logits)
        queue.v.append(v)
        queue.action.append(action)
        if len(queue.state) >= flags.unroll_length + 1:
            state = torch.stack(queue.state)
            reward = torch.stack(queue.reward)
            done = torch.stack(queue.done)
            logits = torch.stack(queue.logits)
            v = torch.stack(queue.v)
            action = torch.stack(queue.action)

            learn_queue.push(
                {
                    "state": state,
                    "reward": reward,
                    "done": done,
                    "logits": logits,
                    "v": v,
                    "action": action,
                    "core_state": cur_set.initial_core_state,
                }
            )

            queue.state = [queue.state[-1]]
            queue.reward = [queue.reward[-1]]
            queue.done = [queue.done[-1]]
            queue.logits = [queue.logits[-1]]
            queue.v = [queue.v[-1]]
            queue.action = [queue.action[-1]]
            cur_set.initial_core_state = prev_core_state

        cur_set.running_reward = cur_set.running_reward + obs["rewards"]
        cur_set.step_count = cur_set.step_count + 1

        episodes_done += obs["done"].sum().item()

        donesteps += (cur_set.step_count * obs["done"]).sum().item()
        donecount += obs["done"].sum().item()
        donerewards += (cur_set.running_reward * obs["done"]).sum().item()

        now = time.time()
        if now - lastprint >= 1:
            meandonerewards = donerewards / donecount if donecount > 0 else 0
            meandonesteps = donesteps / donecount if donecount > 0 else 0
            sps = (env_steps - laststeps) / (now - lastprint)
            running_sps = running_sps * 0.9 + sps * 0.1
            print(
                "reward mean %g (done %g after %g steps) min %g max %g  episodes done %d optimizer steps %d env steps %d SPS %g (%g)"
                % (
                    cur_set.running_reward.mean().item(),
                    meandonerewards,
                    meandonesteps,
                    cur_set.running_reward.min().item(),
                    cur_set.running_reward.max().item(),
                    episodes_done,
                    opt_steps,
                    env_steps,
                    sps,
                    running_sps,
                )
            )

            if wandb is not None:
                wandb.log(
                    {
                        "loss": total_loss,
                        "mean running reward": cur_set.running_reward.mean().item(),
                        "min running reward": cur_set.running_reward.min().item(),
                        "max running reward": cur_set.running_reward.max().item(),
                        "mean episode reward": meandonerewards
                        if donecount > 0
                        else None,
                        "mean episode steps": meandonesteps if donecount > 0 else None,
                        "episodes done": episodes_done,
                        "optimizer steps": opt_steps,
                        "environment steps": env_steps,
                        "sps": sps,
                    }
                )

            donesteps = 0
            donerewards = 0
            donecount = 0
            laststeps = env_steps
            lastprint = now

        cur_set.running_reward *= ~obs["done"]
        cur_set.step_count *= ~obs["done"]
    else:
        # if we're not connected, sleep for a bit so we don't busy-wait
        time.sleep(0.25)

    group.update()
    accumulator.update()

    if accumulator.wants_state():
        accumulator.set_state(
            {
                "optimizer": optimizer.state_dict(),
                "scheduler": scheduler.state_dict(),
            }
        )

    if accumulator.has_new_state():
        optimizer.load_state_dict(accumulator.state()["optimizer"])
        scheduler.load_state_dict(accumulator.state()["scheduler"])

    if accumulator.has_gradients():
        # moolib has reduced gradients, so we can step the optimizer
        opt_steps += 1
        grad_norm = nn.utils.clip_grad_norm_(
            model.parameters(), flags.grad_norm_clipping
        )
        sum = None
        for t in model.parameters():
            sum = t.sum() if sum is None else sum + t.sum()
        print(
            "num updates %d - grad_norm is %g, sum of parameters %g"
            % (accumulator.num_updates(), grad_norm.item(), sum.item())
        )
        # for p in model.parameters():
        #  g = p.grad
        #  if g is not None:
        #    print("opt grad sum ", g.sum().item())
        optimizer.step()
        scheduler.step()
        accumulator.zero_gradients()  # has_gradients() will return false after this

    if accumulator.wants_gradients():
        if learn_queue.empty():
            # we need to signal to moolib that we did not calculate gradients,
            # but gradients will still be reduced from the other participants
            # that may or may not have calculated them
            accumulator.skip_gradients()
        else:
            # "train step", if we have any data to train on then we calculate
            # the gradients and initiate reduction

            data = learn_queue.pop()
            state = data["state"]
            reward = data["reward"]
            done = data["done"]
            logits = data["logits"]
            v = data["v"]
            action = data["action"]
            core_state = data["core_state"]

            model.train()

            # for p in model.parameters():
            #  g = p.grad
            #  if g is not None:
            #    print("zero grad sum ", g.sum().item())

            (new_action, new_logits, new_v), _ = model.forward(
                state, reward, done, core_state
            )

            bootstrap_value = new_v[-1]

            state = state[1:]
            reward = reward[1:]
            done = done[1:]

            logits = logits[:-1]
            v = v[:-1]
            action = action[:-1]

            new_logits = new_logits[:-1]
            new_v = new_v[:-1]

            print("state shape ", state.shape)
            # print("reward shape ", reward.shape)
            # print("done shape ", done.shape)
            # print("logits shape ", logits.shape)
            # print("v shape ", v.shape)
            # print("action shape ", action.shape)

            # print("new_logits shape ", new_logits.shape)
            # print("new_v shape ", new_v.shape)

            if flags.reward_clipping == "abs_one":
                clipped_rewards = torch.clamp(reward, -1, 1)
            elif flags.reward_clipping == "none":
                clipped_rewards = reward

            notdone = ~done

            discounts = notdone * flags.discounting

            vtrace_returns = vtrace.from_logits(
                behavior_policy_logits=logits,
                target_policy_logits=new_logits,
                actions=action,
                discounts=discounts,
                rewards=clipped_rewards,
                values=new_v,
                bootstrap_value=bootstrap_value,
            )

            pg_loss = compute_policy_gradient_loss(
                new_logits,
                action,
                vtrace_returns.pg_advantages,
            )
            baseline_loss = flags.baseline_cost * compute_baseline_loss(
                vtrace_returns.vs - new_v
            )
            entropy_loss = flags.entropy_cost * compute_entropy_loss(new_logits)

            total_loss = pg_loss + baseline_loss + entropy_loss

            total_loss.backward()

            print("loss: %g" % total_loss.item())

            # for p in model.parameters():
            #  g = p.grad
            #  if g is not None:
            #    print("out grad sum ", g.sum().item())

            # this will trigger an asynchronous gradient reduction.
            # has_gradients() will return true when the reduction is done
            accumulator.reduce_gradients(state.size(1))
