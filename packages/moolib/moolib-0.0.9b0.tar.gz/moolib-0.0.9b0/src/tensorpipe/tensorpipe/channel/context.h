/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <memory>
#include <string>
#include <vector>

#include <tensorpipe/common/defs.h>
#include <tensorpipe/transport/context.h>

namespace tensorpipe_moorpc {
namespace channel {

enum class Endpoint : bool { kConnect, kListen };

template <typename TBuffer>
class Channel;

// Abstract base class for channel context classes.
//
// Instances of these classes are expected to be registered with a
// context. All registered instances are assumed to be eligible
// channels for all pairs.
//
template <typename TBuffer>
class Context {
 public:
  // Return whether the context is able to operate correctly.
  //
  // Some channel types may be unable to perform as intended under some
  // circumstances (e.g., specialized hardware unavailable, lack of
  // permissions). They can report it through this method in order for
  // the core context to avoid registering them in the first place.
  //
  virtual bool isViable() const = 0;

  // Return the number of control connections needed to create an instance of
  // this channel.
  //
  // Most channels require only one, but some require more (cuda_basic), and
  // some might require none.
  //
  virtual size_t numConnectionsNeeded() const = 0;

  // Return string to describe the domain for this channel.
  //
  // Two processes with a channel context of the same type can connect
  // to each other if one side's domain descriptor is "accepted" by the
  // other one, using the canCommunicateWithRemote method below. That
  // method must be symmetric, and unless overridden defaults to string
  // comparison.
  //
  virtual const std::string& domainDescriptor() const = 0;

  // Compare local and remote domain descriptor for compatibility.
  //
  // Determine whether a channel can be opened between this context and
  // a remote one that has the given domain descriptor. This function
  // needs to be symmetric: if we called this method on the remote
  // context with the local descriptor we should get the same answer.
  // Unless overridden it defaults to string comparison.
  //
  virtual bool canCommunicateWithRemote(
      const std::string& remoteDomainDescriptor) const = 0;

  // Return newly created channel using the specified connections.
  //
  // It is up to the channel to either use these connections for further
  // initialization, or use them directly. Either way, the returned
  // channel should be immediately usable. If the channel isn't fully
  // initialized yet, take care to queue these operations to execute
  // as soon as initialization has completed.
  //
  virtual std::shared_ptr<Channel<TBuffer>> createChannel(
      std::vector<std::shared_ptr<transport::Connection>>,
      Endpoint) = 0;

  // Tell the context what its identifier is.
  //
  // This is only supposed to be called from the high-level context. It will
  // only used for logging and debugging purposes.
  virtual void setId(std::string id) = 0;

  // Put the channel context in a terminal state, in turn closing all of its
  // channels, and release its resources. This may be done asynchronously, in
  // background.
  virtual void close() = 0;

  // Wait for all resources to be released and all background activity to stop.
  virtual void join() = 0;

  virtual ~Context() = default;

 private:
  std::string name_;
};

} // namespace channel
} // namespace tensorpipe_moorpc
