#!/bin/bash -e

rsync -Paz built/* static robots.txt favicon.ico olegdb.org:/var/www/oleg/
