#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evaluate(env, e):
    if type(e) is dict:
        for label in e:
            children = e[label]
            if label == "Number":
                return env, children[0]
            elif label == "Plus":
                return env, evaluate(env, children[0])[1] + evaluate(env, children[1])[1]
            elif label == "Variable":
                if env[children[0]] is not None:
                    env, s = evaluate(env, env[children[0]])
                    return env, s
                else:
                    return env, None
            elif label == "Array":
                if len(children) > 2:
                    env, a1 = evaluate(env, children[0])
                    env, a2 = evaluate(env, children[1])
                    env, a3 = evaluate(env, children[2])
                    env
    else:
        if e == "True":
                return env, True
        elif e == "False":
                return env, False
        else:
            return env, None

def execute(env, s):
    if type(s) is dict:
        for label in s:
            children = s[label]
            if label == "Print": # Might have to do a check for "End"
                env, t = evaluate(env, children[0])
                if children[1] is not None:
                    env, s = execute(env, children[1])
                    return env, [t] + s
                else:
                    return env, [t]
            elif label == "Assign":
                var = children[0]["Variable"][0] # Get variable name
                val = children[1] # Get the expression. This won't be evaluated until the variable is called
                env[var] = val
                if children[2]:
                    env, g = execute(env, children[2])
                    return env, g
                else:
                    return None, None
            elif label == "If":
                env, t = evaluate(env, children[0])
                if (t):
                    env, g = execute(env, children[1])
                    if children[2]:
                        env, h = execute(env, children[2])
                        return env, g + h
                    else:
                        return env, g
                else:
                    if children[2]:
                        env, h = execute(env, children[2])
                        return env, h
                    else:
                        return env, []
    if s == "End":
        return env, []

def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s)) # Ignore this error, it's in parse.py
    return o


#eof