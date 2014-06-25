---
title:OlegDB 0.1.2 "Mayo Indoctrination" Released
author:Quinlan Pfiffer
date:2014-06-25
---

This is a pretty heavy release, in which we introduce [prefix matching](/docs/0.1.2/en/documentation.html#prefix_matching)
, [key/cursor iteration](/docs/0.1.2/en/documentation.html#cursor_iteration) and a new
`mmap()` based data architecture which you can read about
[here.](/docs/0.1.2/en/documentation.html#values_file)

Thanks to our contributors, [Alessandro Gatti](https://faulty.equipment/) and [Martijn Gerkes.](http://zeroZshadow.com/)

Using OlegDB? Want help? Scared? Check out our [IRC channel](/community.html) on
freenode: #olegdb.

## Full Changelog
* Prefix matching via HTTP
* Cursor iteration via HTTP
* Values are now `mmap()`'d in from a values file, which means they don't quite have to be resident in-memory for use.
* Erlang frontend now periodically calls `fflush()` and `fsync()` to ensure data is written to disk.
* Erlang frontend now periodically compacts and cleanses the AOL file
* More tests
* Various bugfixes

## File Deltas
````
$ git diff --stat v.0.1.1 HEAD
...
76 files changed, 5743 insertions(+), 6052 deletions(-)
````
