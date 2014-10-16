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
                return env, evalTerm(env, children[0])[1] + evalTerm(env, children[1])[1]
            elif label == "Variable":
                if env[children[0]] is not None:
                    env, s = evalExpression(env, env[children[0]])
                    return env, s
                else:
                    return env, None
            elif label == "Log":
                return env, math.log(evalTerm(env, children[0]), 2)
            elif label == "Mult":
                return env, evalTerm(env, children[0])[1] * evalTerm(env, children[1])[1]
            else:
                return None, None
    else:
        return None, None

# I don't believe any Formulas other than "Variable can change the env" - this is important for logical operations
def evalFormula(env, e):
    if type(e) is dict:
        for label in e:
            children = e[label]
            if label == "Variable":
                if env[children[0]] is not None:
                    env, s = evalExpression(env, env[children[0]])
                    return env, s
                else:
                    return env, None
            elif label == "Not":
                return env, not evalFormula(env, children[0])[1]
            elif label == "Xor":
                return env, evalFormula(env, children[0])[1] != evalFormula(env, children[1])[1]
            elif label == "And":
                return env, evalFormula(env, children[0])[1] and evalFormula(env, children[1])[1]
            elif label == "Or":
                return env, evalFormula(env, children[0])[1] or evalFormula(env, children[1])[1]
            else:
                return env, None
    else:
        if e == "True":
                return env, True
        elif e == "False":
                return env, False
        else:
            return env, None

def evalExpression(env, e): # Useful helper function.
    envTerm, t = evalTerm(env, e)
    envForm, f = evalFormula(env, e)
    if t is not None:
        return env, t
    elif f is not None:
        return env, f
    else:
        return None, None

def execProgram(env, s):
    if type(s) is dict:
        for label in s:
            children = s[label]
            # print(children)
            if label == "Print": # Might have to do a check for "End"
                env, t = evalExpression(env, children[0])
                if children[1] is not None:
                    env, s = execProgram(env, children[1])
                    return env, [t] + s
                else:
                    return env, [t]
            elif label == "Assign":
                var = children[0]["Variable"][0] # Get variable name
                val = children[1] # Get the expression. This won't be evaluated until the variable is called
                env[var] = val
                if children[2]:
                    env, g = execProgram(env, children[2])
                    return env, g
                else:
                    return None, None
            elif label == "If":
                env, t = evalExpression(env, children[0])
                if (t):
                    env, g = execProgram(env, children[1])
                    if children[2]:
                        env, h = execProgram(env, children[2])
                        return env, g + h
                    else:
                        return env, g
                else:
                    if children[2]:
                        env, h = execProgram(env, children[2])
                        return env, h
                    else:
                        return env, []
            elif label == "Procedure":
                var = children[0]["Variable"][0] # Get variable name
                val = children[1] # Get the expression. This won't be evaluated until the variable is called
                env[var] = val
                if children[2]:
                    env, g = execProgram(env, children[2])
                    return env, g
                else:
                    return None, None
            elif label == "Call":
                val = children[0]["Variable"][0]
                env, e = execProgram(env, env[val])
                if children[1] is not None:
                    env, f = execProgram(env, children[1])
                    return env, e + f
                else:
                    return env, e
            elif label == "While":
                e = []
                env, t = evalExpression(env, children[0])
                while (t):
                    if children[1] is not None:
                        env, f = execProgram(env, children[1])
                        e += f
                if children[2] is not None:
                    env, g = execProgram(env, children[2])
                    return env, e + g
                else:
                    return env, e

    if s == "End":
        return env, []

def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s)) # Ignore this error, it's in parse.py
    return o

#eof