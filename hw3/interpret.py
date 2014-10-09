######################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# interpret.py
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evalTerm(env, e):
    pass # Complete for Problem #1, part (a).

def evalFormula(env, e):
    pass # Complete for Problem #1, part (b).			

def evalExpression(env, e): # Useful helper function.
    pass

def execProgram(env, s):
    pass # Complete for Problem #1, part (c).
                    
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof