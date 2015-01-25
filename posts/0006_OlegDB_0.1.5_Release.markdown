---
title:OlegDB 0.1.5 "Spider Marketplace" Released
author:Quinlan Pfiffer
date:2015-01-25
---

With an exciting new year comes and exciting new release of OlegDB! We have a
sweet suite of backwards-compatible (kind of) changes in store for all 12 of you
using this mayo jar of a database! Including but not limited to:

* Removed Erlang in favor of Go
* Transactions! Sort of.
* [Mayo Workbench](https://github.com/infoforcefeed/mayo-workbench)
* Bug-fixes

## Go vs. Erlang
The reasons we're not using Erlang anymore are pretty simple:

* [Bus-factor](https://en.wikipedia.org/wiki/Bus_factor)
* The Port Driver
* Easier to find Go contributors
* Shipping a binary is infinitely easier than handling a VM
* Unix signal handling

Expect a full blog post elaborating on these reasons, but for now just know that
it was easier for us to switch to a Go + C stack rather than an Erlang + C
one.

## Transactions

In this release we've laid the foundation for full ACID transactions in OlegDB.
They're not exposed via the API yet, and they're [not fully ACID yet](https://github.com/infoforcefeed/OlegDB/issues/140) either, but
the mechanism in place is much more durable than what we were doing before.

Each internal API call is using transactions, so the chance that you'll get your
data back out of OlegDB is the highest it's ever been!

## Mayo Workbench

Mayo workbench is a tool that came [from our bot](https://twitter.com/oleg_dbooks/status/463347397696176128)
which is how we do most of our brainstorming. It's a simple CRUD application for
viewing and (soon) modifying your data. Check it out, it's a no-dependencies C
project. Just point it at your OlegDB instance and start clicking around. I
might eventually incorporate it into the official repository, but for now it's a
seperate thing.

## File Deltas
```
$ git diff --stat v.0.1.4 HEAD
...
70 files changed, 6479 insertions(+), 6340 deletions(-)
```
