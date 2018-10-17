#!/usr/bin/env bash

test0="$(python3 ex_basic.py | tail -n 1)"
cat $test0

test1="$(python3 ex_basic.py --a 1 --b 2 | tail -n 1)"
cat $test1

test2="$(python3 ex_config.py --config config.yml | tail -n 1)"
cat $test2

test3="$(python3 ex_config.py -a 1 --config config.yml | tail -n 1)"
cat $test3