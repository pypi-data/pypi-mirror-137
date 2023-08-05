/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <tensorpipe/channel/context_impl_boilerplate.h>
#include <tensorpipe/channel/cuda_context.h>
#include <tensorpipe/common/cuda_buffer.h>
#include <tensorpipe/common/cuda_lib.h>
#include <tensorpipe/common/deferred_executor.h>

namespace tensorpipe_moorpc {
namespace channel {
namespace cuda_xth {

class ChannelImpl;

class ContextImpl final
    : public ContextImplBoilerplate<CudaBuffer, ContextImpl, ChannelImpl> {
 public:
  static std::shared_ptr<ContextImpl> create();

  ContextImpl();

  explicit ContextImpl(CudaLib cudaLib);

  std::shared_ptr<CudaChannel> createChannel(
      std::vector<std::shared_ptr<transport::Connection>> connections,
      Endpoint endpoint);

  const CudaLib& getCudaLib();

  // Implement the DeferredExecutor interface.
  bool inLoop() const override;
  void deferToLoop(Function<void()> fn) override;

 protected:
  // Implement the entry points called by ContextImplBoilerplate.
  void closeImpl() override;
  void joinImpl() override;

 private:
  OnDemandDeferredExecutor loop_;

  const CudaLib cudaLib_;
};

} // namespace cuda_xth
} // namespace channel
} // namespace tensorpipe_moorpc
