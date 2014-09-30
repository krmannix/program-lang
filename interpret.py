import math

# Do I need to return env each time??

def evalTerm(env, t):

    if type(t) is dict:
        for label in t:
            children = t[label]
            if label == "Number":
                return children[0]
            elif label == "Plus":
                return evalTerm(env, children[0]) + evalTerm(env, children[1])
            elif label == "Variable":
                if env[children[0]] is not None:
                    return env[children[0]]
                else:
                    return None
            elif label == "Log":
                return math.log(evalTerm(env, children[0]), 2)
            elif label == "Mult":
                return evalTerm(env, children[0]) * evalTerm(env, children[1])
            else:
                return None

def evalFormula(env, f):

    if type(f) is dict:
        for label in f:
            children = f[label]
            if label == "Variable":
                if env[children[0]] is not None:
                    return env[children[0]]
                else:
                    return None
            elif label == "Not":
                return not evalFormula(env, children[0])
            elif label == "Xor":
                return evalFormula(env, children[0]) != evalFormula(env, children[1])
            else:
                return None
    else:
        if f == "True":
                return True
        elif f == "False":
                return False
        else:
            return None


def execProgram(env, s):

    if type(s) is dict:
        for label in s:
            children = s[label]
            if label == "Print": # Might have to do a check for "End"
                t = evalTerm(env, children[0])
                f = evalFormula(env, children[0])

                if t is not None:
                    return env, [t]
                elif f is not None:
                    return env, [f]
                else:
                    return None
            elif label == "Assign":
                var = children[0]["Variable"][0]
                if var is not None:
                    t = evalTerm(env, children[1])
                    f = evalFormula(env, children[1])
                    if t is not None:
                        env[var] = t
                        if children[2] is not None:
                            return execProgram(env, children[2])
                        else:
                            return env, []
                    elif f is not None:
                        env[var] = f
                        if children[2] is not None:
                            return execProgram(env, children[2])
                        else:
                            return env, []
                    else:
                        return None
            elif label == "If":
                if evalFormula(env, children[0]):
                    if children[1] is not None:
                        if children[2] is not None:
                            e1 = execProgram(env, children[1])
                            e2 = execProgram(env, children[2])
                            return e1, e2
                        else:
                            return execProgram(env, children[1])
                else:
                    return None
            #elif label == "While":


    else:
        if s == "End":
            return env, []






