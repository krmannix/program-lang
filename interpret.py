import math, re
from parse import program
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
                    if children[1]:
                        env2, t_ = execProgram(env, children[1])
                        if t_:
                            return env2, [t, t_]
                        else:
                            return env2, [t]
                    else:
                        return env, [t]
                elif f is not None:
                    if children[1]:
                        env2, f_ = execProgram(env, children[1])
                        if f_:
                            return env2, [f, f_]
                        else:
                            return env2, [f]
                    else:
                        return env, [f]
                else:
                    return None, None
            elif label == "Assign":
                var = children[0]["Variable"][0]
                if var is not None:
                    t = evalTerm(env, children[1])
                    f = evalFormula(env, children[1])
                    if t is not None:
                        env[var] = t
                        if children[2] is not None:
                            env2, l = execProgram(env, children[2])
                            if l:
                                return env2, l
                            else:
                                return env2, []
                        else:
                            return env, []
                    elif f is not None:
                        env[var] = f
                        if children[2] is not None:
                            env, p = execProgram(env, children[2])
                            return env, p
                        else:
                            return env, []
                    else:
                        return None, None
            elif label == "If":
                if evalFormula(env, children[0]):
                    if children[1] is not None:
                        if children[2] is not None:
                            env, e1 = execProgram(env, children[1])
                            env, e2 = execProgram(env, children[2])
                            o = []
                            for i in e1:
                                if i:
                                    o.append(i)
                            for j in e2:
                                if j:
                                    o.append(j)
                            return env, o
                        else:
                            env, e3 = execProgram(env, children[1])
                            return env, e3
                    else:
                        return None, None
                else:
                    return None, None
            elif label == "While":
                if evalFormula(env, children[0]):
                    env2, e1 = execProgram(env, children[1])
                    env3, e2 = execProgram(env2, children[2])
                    return env3, e1 + e2
                else:
                    env2, e2 = execProgram(env, children[2])
                    return env2, e2
    else:
        if s == "End":
            return env, []


def tokenize(input,s):
    #creates a tokenize string
    spch = ["\\", "^", "$", ":=", ">", "<", ".", "|", ";", "#", "@", ",", "?", "*", "+", "(", ")", "[", "]", "{", "}"]

    tstring = "\s+|[0-9]+"

    # Now add the special chars with backslashes in front
    for i in input:
        if i in spch:
            i = '\\' + i

            tstring += "|" + i

    tokens = [token for token in re.split(r"("+tstring+")", s)]

    # Throw out the spaces and return the result.
    return [t for t in tokens if not t.isspace() and not t == ""]


def interpret(s):
    t = tokenize(['print', 'assign', 'end', 'true', 'false',
                   'not', 'while', 'and', 'or', 'equal', 'less', 'than',
                   'greater', 'plus', 'mult', 'log', '@', '#', ';',
                   ':=', '(', ')', ',', '+', '*', '&&', "||",
                   "==", "<", ">"], s)
    pt, throwaway = program(t)
    env, e = execProgram({}, pt)
    if e is not None:
        return e
    else:
        return None



