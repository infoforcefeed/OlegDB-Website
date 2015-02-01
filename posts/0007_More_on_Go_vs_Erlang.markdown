---
title:More on Go vs. Erlang
author:Quinlan Pfiffer
date:2015-01-31
---

During our most recent episode of OlegDB muckery, I glossed over how we migrated
from [Go to Erlang for the latest release.](https://olegdb.org/blog/0006_OlegDB_0.1.5_Release.html)
I also promised that I would go over in more detail why we switched and what the
benefit was, even if our lines added/removed was about the same.

The first thing I would like to clarify is that OlegDB is **not** primarily written in Go,
nor was it primarily written in Erlang. OlegDB is, and will always be, a giant C
hairball. I say hairball with the fondest conotations a neurotic developer can
conjure up. It seems many people were confused about this concept, so I will
repeat: We did not **rewrite** OlegDB in Go, we rewrote the communication later
from Erlang to Go.

So to go over why we switched, I'll elaborate on the reasons I gave last time in more
detail:

* Bus-factor
* The Port Driver
* Easier to find Go contributors
* Shipping a binary is infinitely easier than handling a VM
* Unix signal handling

## Bus Factor

This is not Erlang's fault, it's completely mine. In the circles the OlegDB devs
run in, I push kind of a tyrannical [no dependencies](http://qp-nodeps.shithouse.tv/)
policy which results in a lot of reinvented wheels. Because of this, I [wrote my
own HTTP server.](https://github.com/qpfiffer/mttp) I had only
recently learned Erlang, and ignored a lot of best practices.

There are no OTP fundamentals, no dialyzer type checks, or tests. This made it kind of a mess, and
it doesn't help that everyone I talk to is scared to death of Erlang syntax for
some reason. So it was really just me maintaining this Erlang code, which made
it kind of a liability. Luckily [we don't have any users so it's not really an issue.](http://friends.shithouse.tv/)

## The Port Driver
Just [look at this bad boy.](https://github.com/infoforcefeed/OlegDB/blob/204779fa12334316e3c832a6881baa9b5cc43912/c_src/port_driver.c)
Thats 620 lines of weird looking C used to talk to Erlang. Those 620 lines took
a [long time to figure out,](http://qpfiffer.com/posts/2014-02-10-Erlang_port_drivers) and even
then half of the callbacks in the [ErlDrvEntry struct aren't used](https://github.com/infoforcefeed/OlegDB/blob/204779fa12334316e3c832a6881baa9b5cc43912/c_src/port_driver.c#L592).
Theres a lot of weird serialization that has to occur between the C and Erlang layers that isn't always
decipherable. Most people I talked to about the port driver just looked at the
code as one big black box of complexity. I guess this is probably my fault as
the completely fallible programmer.

I could've gone with Erlang [NIFs](http://www.erlang.org/doc/tutorial/nif.html)
but those are designed for short, stateless, side-effectless computation which
is basically the opposite of a database. Port drivers remain the fastest way to
interface with foreign libraries.

The Go FFI stuff just [makes more sense.](https://github.com/infoforcefeed/OlegDB/blob/master/frontend/goleg/wrapper.go)
You have a one-to-one mapping between C functions, types, calls, etc. that make
it really easy and readable.

I've used other FFI stuff, and Erlang's FFI solutions are definitely not my
favorite. I would love to know how others are using the port driver
interconnectivity in Erlang to see some good examples.

## Go Contributors

Maybe this is just the info-bubble I find myself in, but I have more Gopher
friends than Erlang friends. Since it's imperative and the syntax is mostly
familiar to people, I guess that makes it more open.

When your project is mayonnaise themed, you take what you can get.

## Shipping a Binary

I would rather ship a binary rather than beam files any day. I find it much easier to
ship plain old C/Go source code around than Erlang code that depends on the the
"ei.h" header, which apparently isn't even compiled [for the right architecture
on OS X](https://gist.github.com/kyleterry/15b9cb23f3dfca4d8c12). It takes
some real [witches brew](https://github.com/infoforcefeed/OlegDB/blob/d3b9f1ed5e8b60427f5285cc2790020c38684408/Makefile#L18)
to properly find, include and link the headers. I could never get these to link
properly on OS X.

## Unix Signal Handling

This was really what killed me. Erlang has this idea that all programs are
running in the VM together, on a seperate plane of existance than userland. You
can't just send a SIGTERM to your program and send events based on that.
Instead you have to send signals to the running Erlang shell, which you tell
to [ignore them](http://erlang.org/doc/man/erl.html#id165878)
with `+Bi`. Then Bash can catch them, send signals via a [new Erlang shell](https://github.com/infoforcefeed/OlegDB/blob/204779fa12334316e3c832a6881baa9b5cc43912/run_server.sh#L10)
telling your program to halt and cleanup.

All of this makes it a nightmare to deal with, which is why some of the bigger
Erlang programs ([RabbitMQ](http://www.rabbitmq.com/man/rabbitmqctl.1.man.html), [ActorDB](http://www.actordb.com/docs-getstarted.html#run))
use `ctl` scripts that do this sort of thing for you. If you want to have some
fun, peruse the CouchDB init script sometime.

## Conclusions

Erlang is great. I love it. I'd much rather create a project in Erlang than in
Go, but it's not [all about me,](https://github.com/infoforcefeed/OlegDB/graphs/contributors) so I made some
concessions. The next time, I'll probably follow the
guidelines:

* Listen to the community. OTP, `erlang.mk`, Rebar, everything.
* Erlang should be the only thing in the project. No weird dependencies, Erlang stands strong alone. See Riak, CouchDB, RabbitMQ.
* Read [Erlang in Anger](http://www.erlang-in-anger.com/) and then read it again to find out what not to do.

I would really love to see people talking more about what they've done with the
port drivers, NIFs, BIFs, all that stuff. Spelunking through the [Mochi webserver](https://github.com/mochi/mochiweb)
source code to figure out that acceptor pools are a thing was really fun! The
Erlang community really needs more visibility. For now we'll stick to Go and C.
