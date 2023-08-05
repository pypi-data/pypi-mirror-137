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
#include <thread>

#include <tensorpipe/channel/context_impl_boilerplate.h>
#include <tensorpipe/channel/cpu_context.h>
#include <tensorpipe/common/cpu_buffer.h>
#include <tensorpipe/common/deferred_executor.h>
#include <tensorpipe/common/error.h>
#include <tensorpipe/common/optional.h>
#include <tensorpipe/common/queue.h>

namespace tensorpipe_moorpc {
namespace channel {
namespace xth {

class ChannelImpl;

class ContextImpl final
    : public ContextImplBoilerplate<CpuBuffer, ContextImpl, ChannelImpl> {
 public:
  static std::shared_ptr<ContextImpl> create();

  ContextImpl();

  std::shared_ptr<CpuChannel> createChannel(
      std::vector<std::shared_ptr<transport::Connection>> connections,
      Endpoint endpoint);

  // Implement the DeferredExecutor interface.
  bool inLoop() const override;
  void deferToLoop(Function<void()> fn) override;

  using copy_request_callback_fn = Function<void(const Error&)>;

  void requestCopy(
      void* remotePtr,
      void* localPtr,
      size_t length,
      copy_request_callback_fn fn);

 protected:
  // Implement the entry points called by ContextImplBoilerplate.
  void closeImpl() override;
  void joinImpl() override;

 private:
  OnDemandDeferredExecutor loop_;

  struct CopyRequest {
    void* remotePtr;
    void* localPtr;
    size_t length;
    copy_request_callback_fn callback;
  };

  std::thread thread_;
  Queue<optional<CopyRequest>> requests_;

  // This is atomic because it may be accessed from outside the loop.
  std::atomic<uint64_t> nextRequestId_{0};

  void handleCopyRequests();
};

} // namespace xth
} // namespace channel
} // namespace tensorpipe_moorpc
