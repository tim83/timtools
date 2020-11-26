#! /usr/bin/python3
"""Module containing a collection of usefull tools"""

import bash
import log
import notify

a = dir(log)
b = dir(bash)
c = dir(notify)

del a, b, c
