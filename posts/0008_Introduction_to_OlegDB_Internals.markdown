---
title:Introduction to OlegDB Internals
author:Quinlan Pfiffer
date:2015-04-03
---

This post is intended as an introduction for would-be contributors intimidated
by jumping into a C project for the first time, and those that want to know how
OlegDB works on the inside. The code may be a little neurotic, but it's not that
bad if you know where things are and how the general flow of the storage engine
goes. At it's heart it's pretty simple, but it can get kind of hairy
conceptually at times (eg. transactions). I'll primarily be talking about the C
storage engine today, and not the Go frontend, since the storage engine is
mostly what I know.

There are a handful of major components to OlegDB:

* The hashtable
* The splay tree
* The AOL file(s)
* The Value file(s)
* The transaction wrappers

## The Hashtable

Internally OlegDB is just a bunch of code wrapped around a pretty naive
hashtable implementation. It has a maximum number of buckets, uses Murmur3 to
hashing and stops-the-world to rehash everything when we "run out of space" in
the table.

"run out of space" is in quotes in this context because when we see an
inevitable key collision, we use a [linked list](https://en.wikipedia.org/wiki/Hash_table#Separate_chaining_with_linked_lists)
to keep multiple keys. This means that we never really know if the table is
full, so as of right now we rehash when the table reaches the current maximum
bucket size.

The objects stored in the hashtable are `ol_bucket` structs. These are
essentially offsets into the values file of all inserted data, in addition to
some metadata, like the next bucket in the chain or the key or whatever.

