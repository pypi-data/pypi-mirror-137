@dataclasses.dataclass
class StatMean:
    value: float = 0
    n: int = 0

    def result(self):
        if self.n == 0:
            return None
        return self.value / self.n

    def __sub__(self, other):
        assert isinstance(other, StatMean)
        return StatMean(self.value - other.value, self.n - other.n)

    def __iadd__(self, other):
        if isinstance(other, StatMean):
            self.value += other.value
            self.n += other.n
        else:
            self.value += other
            self.n += 1
        return self

    def reset(self):
        self.value = 0
        self.n = 0

    def __repr__(self):
        return repr(self.result())


@dataclasses.dataclass
class StatSum:
    value: float = 0

    def result(self):
        return self.value

    def __sub__(self, other):
        assert isinstance(other, StatSum)
        return StatSum(self.value - other.value)

    def __iadd__(self, other):
        if isinstance(other, StatSum):
            self.value += other.value
        else:
            self.value += other
        return self

    def reset(self):
        pass

    def __repr__(self):
        return repr(self.result())


class GlobalStatsAccumulator:
    """Class for global accumulation state. add_stats gets reduced."""

    def __init__(self, rpc_group, global_stats):
        self.rpc_group = rpc_group
        self.global_stats = global_stats
        self.reduce_future = None
        self.queued_global_stats = None
        self.sent_global_stats = None
        self.prev_stats = None

    def add_stats(self, dst, src):
        for k, v in dst.items():
            v += src[k]
        return dst

    def enqueue_global_stats(self, stats):
        if self.queued_global_stats is None:
            self.queued_global_stats = copy.deepcopy(stats)
        else:
            # Sum pending data.
            self.add_stats(self.queued_global_stats, stats)

    def reduce(self, stats):
        if self.reduce_future is not None and self.reduce_future.done():
            if self.reduce_future.exception() is not None:
                logging.info(
                    "global stats accumulation error: %s",
                    self.reduce_future.exception(),
                )
                self.enqueue_global_stats(self.sent_global_stats)
            else:
                self.add_stats(self.global_stats, self.reduce_future.result())
            self.reduce_future = None

        stats_diff = stats
        if self.prev_stats is not None:
            stats_diff = {k: v - self.prev_stats[k] for k, v in stats.items()}

        self.enqueue_global_stats(stats_diff)
        self.prev_stats = copy.deepcopy(stats)

        if self.reduce_future is None:
            # Only reduce when not currently reducing.
            # Otherwise, we keep queued_global_stats for next time.
            self.sent_global_stats = self.queued_global_stats
            self.queued_global_stats = None
            # Additional copy to deal with potential partial reductions.
            self.reduce_future = self.rpc_group.all_reduce(
                "global stats", copy.deepcopy(self.sent_global_stats), self.add_stats
            )

    def reset(self):
        if self.prev_stats is not None:
            for _, v in self.prev_stats.items():
                v.reset()


class EnvBatchState:
    def __init__(self, flags, model):
        batch_size = flags.actor_batch_size
        device = flags.device
        self.batch_size = batch_size
        self.prev_action = torch.zeros(batch_size).long().to(device)
        self.future = None
        self.core_state = model.initial_state(batch_size=batch_size)
        self.core_state = tuple(s.to(device) for s in self.core_state)
        self.initial_core_state = self.core_state

        self.running_reward = torch.zeros(batch_size)
        self.step_count = torch.zeros(batch_size)

        self.time_batcher = moolib.Batcher(flags.unroll_length + 1, flags.device)

    def update(self, env_outputs, action, stats):
        self.prev_action = action
        self.running_reward += env_outputs["reward"]
        self.step_count += 1

        done = env_outputs["done"]

        episode_return = self.running_reward * done
        episode_step = self.step_count * done

        episodes_done = done.sum().item()
        if episodes_done > 0:
            stats["mean_episode_return"] += episode_return.sum().item() / episodes_done
            stats["mean_episode_step"] += episode_step.sum().item() / episodes_done
        stats["steps_done"] += done.numel()
        stats["episodes_done"] += episodes_done

        stats["running_reward"] += self.running_reward.mean().item()
        stats["running_step"] += self.step_count.mean().item()

        not_done = ~done

        self.running_reward *= not_done
        self.step_count *= not_done
