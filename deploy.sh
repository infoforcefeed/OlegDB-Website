#!/bin/bash -e

rsync -Pavz built/* static shithouse.tv:/var/www/shithouse/oleg/
