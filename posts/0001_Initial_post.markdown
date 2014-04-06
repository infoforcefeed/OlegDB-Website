---
title:Using OlegDB with Django
author:Quinlan Pfiffer
icon_class:
date: 2014-04-05
---

Using OlegDB with Django is trivial. Just install [django-olegdbcache](https://github.com/infoforcefeed/django-olegdbcache)
and you can be ready to go in seconds.

You can either grab it from pip:

````
$ pip install django-OlegDBCache
````

or get it via ssh and use your standard `setup.py` muckery. Once thats all
accomplished, all you have to do is tweak your settings a bit:

````
CACHES = {
    "default": {
        "BACKEND": "django_olegdbcache.oleg.OlegDBCache",
        "LOCATION": "http://localhost:8080"
    }
}
````

This, of course, assumes that OlegDB is running and accessible on
`localhost:8080`. Why would you try to use a cache without the cache running?
Silly goose.

