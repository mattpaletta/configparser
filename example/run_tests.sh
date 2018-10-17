#!/usr/bin/env bash

test0=$(python ex_basic.py)
cat $test0

test1=$(python ex_basic.py --a 1 --b 2)
cat $test1

test2=$(python ex_config.py --config config.yml)
cat $test2

test3=$(python ex_config.py -a 1 --config config.yml)
cat $test3