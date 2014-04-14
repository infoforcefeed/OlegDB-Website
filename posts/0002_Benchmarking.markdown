---
title:Benchmarking with Wrk
author:Quinlan Pfiffer
icon_class:
date: 2014-04-12
---

Today at Proleg Labs&trade; we're going to discuss the awesome bechmarking tool
[wrk](https://github.com/wg/wrk). wrk is a badass little HTTP stress testing
utility written by a [mysterious open-source do-gooders](http://glozer.net/).
I'm gonna run through how we torture OlegDB with it to make sure everything is
working in an acceptable fashion.

Building and installing wrk is outside the scope of this article, but it's not
hard. You just need to do your standard `make && make install` dance and you'll
do fine. Once you have your `wrk` executable handy, we can get started.

On my particular machine, I like to test with these settings:

````
$ ./wrk -t8 -c400 -d30s http://localhost:8080/test
````

This requires a little explanation.

* `-t8` is the number of threads to use. I've got eight cores, lets use eight threads.
* `-c400` is the number of connections to have open. 400 seems like a nice, round number.
* `-d30s` is the amount of time to stress test. Thirty seconds should be [enough for anyone](http://quoteinvestigator.com/2011/09/08/640k-enough/).

and the last parameter is the URL we'll be hitting with the `wrk` jackhammer.
Since we need to actually test Oleg and not some 404 page we'll need to put
something into the database for `wrk` to fetch. Results will vary based on how
much data you put in, but lets just test with this quote from <a href="http://en.wikipedia.org/wiki/Leviathan_(book)">
Thomas Hobbes' Leviathan:</a>

````
Man is distinguished, not only by his reason, but by this singular passion from
other animals, which is a lust of the mind, that by a perseverance of delight
in the continued and indefatigable generation of knowledge, exceeds the short
vehemence of any carnal pleasure.
````

Say, thats neat Thomas Hobbes! Let's throw that into OlegDB, which I'll assume
you have running on `localhost:8080`:

````
$ curl -X POST -d '
> Man is distinguished, not only by his reason, but by this singular passion from
> other animals, which is a lust of the mind, that by a perseverance of delight
> in the continued and indefatigable generation of knowledge, exceeds the short
> vehemence of any carnal pleasure.' http://localhost:8080/test
無駄
````

Just to do a quick test that it actually inserted (Hey, who knows, right?) let's
curl it back out:

````
$ curl localhost:8080/test
Man is distinguished, not only by his reason, but by this singular passion from
other animals, which is a lust of the mind, that by a perseverance of delight
in the continued and indefatigable generation of knowledge, exceeds the short
vehemence of any carnal pleasure.
````

Excellent, now lets fire up wrk, point it at that URL and see what happens:

````
$ ./wrk -t8 -c400 -d30s http://localhost:8080/test
Running 30s test @ http://localhost:8080/test
  8 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    18.05ms   93.64ms 866.52ms   96.72%
    Req/Sec     4.71k     2.15k   16.44k    70.58%
  1070154 requests in 30.00s, 420.48MB read
  Socket errors: connect 0, read 0, write 0, timeout 27
Requests/sec:  35675.16
Transfer/sec:     14.02MB
````

Hey, <code>35,600</code> Requests/second. Not bad. Not bad at all. For fun, let's see how
[Kyoto Tycoon](http://fallabs.com/kyototycoon/) performs with the same data and
conditions:

````
$ ./wrk -t8 -c400 -d30s http://localhost:1978/test
Running 30s test @ http://localhost:1978/test
  8 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     3.05ms    2.47ms 340.86ms   99.65%
    Req/Sec    17.59k     2.75k   37.67k    77.99%
  3991195 requests in 30.00s, 1.39GB read
Requests/sec: 133041.46
Transfer/sec:     47.58MB
````

...well damn. I guess theres always room to improve.
