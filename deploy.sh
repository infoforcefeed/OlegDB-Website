#!/bin/bash -e

rsync -Paz built/* static robots.txt favicon.ico shithouse.tv:/var/www/oleg/
