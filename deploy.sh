#!/bin/bash -e

rsync -Paz built/* static shithouse.tv:/var/www/shithouse/oleg/
