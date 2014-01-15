#!/bin/bash -e

rsync -Paz built/* massacre.sh static robots.txt favicon.ico olegdb.org:/var/www/oleg/
