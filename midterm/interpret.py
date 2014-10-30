#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
# Modified by Kevin Mannix

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
                if children[1] is not None:
                    env, index = evaluate(env, children[1])
                    var = children[0]['Variable'][0]
                    el = env[var][index]
                    return env, el
                else:
                    return env, None
    else:
        if type(e) == type(0):
            return env, e
        elif e == 'True':
                return env, True
        elif e == 'False':
                return env, False
        elif type(e) == type(""):
            return env, e
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
                if len(children) > 4:
                    env, a1 = evaluate(env, children[1])
                    env, a2 = evaluate(env, children[2])
                    env, a3 = evaluate(env, children[3])
                    env[var] = [a1, a2, a3]
                    if children[4]:
                        env, g = execute(env, children[4])
                        return env, g
                    else:
                        return None, None
                else:
                    return None, None
            elif label == "For":
                var = children[0]["Variable"][0] # Get variable name
                body = children[1]
                env[var] = 0;
                env, e1 = execute(env, body)
                env[var] = 1;
                env, e2 = execute(env, body)
                env[var] = 2;
                env, e3 = execute(env, body)
                if children[2] is not None:
                    env, e4 = execute(env, children[2])
                    return env, e1 + e2 + e3 + e4
                else:
                    return env, e1 + e2 + e3
    if s == "End":
        return env, []

def interpret(s):
    parsed = tokenizeAndParse(s)
    (env, o) = execute({}, parsed) # Ignore this error, it's in parse.py
    return o