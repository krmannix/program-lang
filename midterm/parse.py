#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# parse.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
#

import re

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]) and tokens[0] not in ['true', 'false']:
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression():
    pass # Complete for Problem #1.

def program():
    pass # Complete for Problem #1.

def tokenizeAndParse(s):
    tokens = re.split(r"(\s+|assign|:=|\[|\]|,|print|\+|for|{|}|;|true|false|@|[0-9]|[A-Za-z0-9]*)", s)
    for tok in tokens:
        print(tok)

tokenizeAndParse("assign a := [1+2,4,6];")
#eof