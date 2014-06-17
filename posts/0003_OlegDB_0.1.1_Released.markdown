---
title:OlegDB 0.1.1 'Cartwheeling Trespassers' released
author:Quinlan Pfiffer
date: 2014-05-05
---

Proleg Labs&trade; is happy to announce a new and improved OlegDB! Nicknamed
[Cartwheeling Trespassers](https://github.com/infoforcefeed/OlegDB/releases/tag/v.0.1.1),
this release packs in a whopping delta of 44 files
changed, 869 insertions and 2864 deletions. Hot damn!

Bugfixes in this release include the
[longstanding](https://github.com/infoforcefeed/OlegDB/issues/43)
segfault-on-deletion-but-only-sometimes bug, lots of [memory leak](https://github.com/infoforcefeed/OlegDB/pulls?direction=desc&page=1&sort=created&state=closed)
fixes and a much more rigorous attention to
[static](https://scan.coverity.com/projects/1414)
[analysis](https://padrepio.in/richelieu/infoforcefeed/OlegDB/). Also of note
are some compilation fixes for BSD, so hopefully we'll see Oleg running on
more platforms.

As for features, we've recently added [LZ4
compression](https://code.google.com/p/lz4/) which works really well on some
datasets but not on others. It's fast though and it saves a lot of memory.
We've also added some weird looking data structures called [splay trees](http://en.wikipedia.org/wiki/Splay_tree).
Splay trees will eventually allow use to get cursor-style iteration and 
prefix-matching when `0.2.0` rolls around.

Prefix-matching isn't quite ready via the Erlang frontend, but you can get your
hands wet with [liboleg's prefix matching](/docs/0.1.1/en/documentation.html#ol_prefix_match)
if you're into that sort of thing.

And finally, thanks to those who contributed, [Alessandro
Gatti](https://faulty.equipment/) and [Colby Olson](https://github.com/colby).

Look forward to `0.2.0` sometime later in May. Probably. Otherwise, yell at me
on [twitter.](https://twitter.com/WAallLy)

Warning, pretty loud:

<video src="/static/img/inthemayo.webm" controls></video>
