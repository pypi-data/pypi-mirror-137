/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <tensorpipe/transport/uv/factory.h>

#include <tensorpipe/transport/context_boilerplate.h>
#include <tensorpipe/transport/uv/connection_impl.h>
#include <tensorpipe/transport/uv/context_impl.h>
#include <tensorpipe/transport/uv/listener_impl.h>

namespace tensorpipe_moorpc {
namespace transport {
namespace uv {

std::shared_ptr<Context> create() {
  return std::make_shared<
      ContextBoilerplate<ContextImpl, ListenerImpl, ConnectionImpl>>(
      ContextImpl::create());
}

} // namespace uv
} // namespace transport
} // namespace tensorpipe_moorpc
