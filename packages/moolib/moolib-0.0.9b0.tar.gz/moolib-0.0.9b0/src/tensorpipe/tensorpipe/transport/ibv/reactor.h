/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <atomic>
#include <functional>
#include <future>
#include <list>
#include <mutex>
#include <set>
#include <thread>
#include <vector>

#include <tensorpipe/common/busy_polling_loop.h>
#include <tensorpipe/common/callback.h>
#include <tensorpipe/common/fd.h>
#include <tensorpipe/common/ibv.h>
#include <tensorpipe/common/optional.h>
#include <tensorpipe/transport/ibv/constants.h>
#include <tensorpipe/util/ringbuffer/consumer.h>
#include <tensorpipe/util/ringbuffer/producer.h>

namespace tensorpipe_moorpc {
namespace transport {
namespace ibv {

class IbvEventHandler {
 public:
  virtual void onRemoteProducedData(uint32_t length) = 0;

  virtual void onRemoteConsumedData(uint32_t length) = 0;

  virtual void onWriteCompleted() = 0;

  virtual void onAckCompleted() = 0;

  virtual void onError(IbvLib::wc_status status, uint64_t wrId) = 0;

  virtual ~IbvEventHandler() = default;
};

// Reactor loop.
//
// Companion class to the event loop in `loop.h` that executes
// functions on triggers. The triggers are posted to a shared memory
// ring buffer, so this can be done by other processes on the same
// machine. It uses extra data in the ring buffer header to store a
// mutex and condition variable to avoid a busy loop.
//
class Reactor final : public BusyPollingLoop {
 public:
  Reactor();

  Reactor(IbvLib ibvLib, IbvDeviceList deviceList);

  const IbvLib& getIbvLib() {
    return ibvLib_;
  }

  IbvProtectionDomain& getIbvPd() {
    return pd_;
  }

  IbvCompletionQueue& getIbvCq() {
    return cq_;
  }

  IbvSharedReceiveQueue& getIbvSrq() {
    return srq_;
  }

  const IbvAddress& getIbvAddress() {
    return addr_;
  }

  void registerQp(uint32_t qpn, std::shared_ptr<IbvEventHandler> eventHandler);

  void unregisterQp(uint32_t qpn);

  void postWrite(IbvQueuePair& qp, IbvLib::send_wr& wr);

  void postAck(IbvQueuePair& qp, IbvLib::send_wr& wr);

  void setId(std::string id);

  void close();

  void join();

  ~Reactor();

 protected:
  bool pollOnce() override;

  bool readyToClose() override;

 private:
  // InfiniBand stuff
  const IbvLib ibvLib_;
  IbvContext ctx_;
  IbvProtectionDomain pd_;
  IbvCompletionQueue cq_;
  IbvSharedReceiveQueue srq_;
  IbvAddress addr_;

  void postRecvRequestsOnSRQ(int num);

  std::atomic<bool> closed_{false};
  std::atomic<bool> joined_{false};

  // This marks whether the event loop thread was started (it isn't in case the
  // reactor isn't viable), in order to determine whether to join it at the end.
  // It's a bad solution, a better one would be to not even create the reactor
  // if it's not viable.
  bool threadRunning_{false};

  // An identifier for the context, composed of the identifier for the context,
  // combined with the transport's name. It will only be used for logging and
  // debugging purposes.
  std::string id_{"N/A"};

  // The registered event handlers for each queue pair.
  std::unordered_map<uint32_t, std::shared_ptr<IbvEventHandler>>
      queuePairEventHandler_;

  uint32_t numAvailableWrites_{kNumPendingWriteReqs};
  uint32_t numAvailableAcks_{kNumPendingAckReqs};
  std::deque<std::tuple<IbvQueuePair&, IbvLib::send_wr>> pendingQpWrites_;
  std::deque<std::tuple<IbvQueuePair&, IbvLib::send_wr>> pendingQpAcks_;
};

} // namespace ibv
} // namespace transport
} // namespace tensorpipe_moorpc
