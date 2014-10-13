######################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# interpret.py
#
import re, math

exec(open("parse.py").read())

Node = dict
Leaf = str

def evalTerm(env, t):
    if type(t) is dict:
        for label in t:
            children = t[label]
            if label == "Number":
                return env, children[0]
            elif label == "Plus":
                return env, evalTerm(env, children[0]) + evalTerm(env, children[1])
            elif label == "Variable":
                if env[children[0]] is not None:
                    return env, env[children[0]]
                else:
                    return None
            elif label == "Log":
                return env, math.log(evalTerm(env, children[0]), 2)
            elif label == "Mult":
                return env, evalTerm(env, children[0]) * evalTerm(env, children[1])
            else:
                return None

def evalFormula(env, e):
    pass # Complete for Problem #1, part (b).			

def evalExpression(env, e): # Useful helper function.
    pass

def execProgram(env, s):
    pass # Complete for Problem #1, part (c).
                    
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s)) # Ignore this error, it's in parse.py
    return o

#eof