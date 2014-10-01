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
                    return None
            elif label == "While":
                o = []
                if evalFormula(env, children[0]): # Children 0 is condition, children 1 in loop, children 2 after
                    env2, e1 = execProgram(env, children[1])
                    if e1 is not None:
                        o.append(e1)
                    env3, e2 = execProgram(env2, s)
                    if e2:
                        o.append(e2)
                if children[2] is not None:
                    env, e3 = execProgram(env3, children[2])
                    if e3 is not None:
                        o.append(e3)
                return env, o
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
                   'not', 'and', 'or', 'equal', 'less', 'than',
                   'greater', 'plus', 'mult', 'log', '@', '#', ';',
                   ':=', '(', ')', ',', '+', '*', '&&', "||",
                   "==", "<", ">"], s)

    pt, throwaway = program(t)
    env, e = execProgram({}, pt)
    if e is not None:
        return e
    else:
        return None

def check(name, function, inputs_result_pairs):
    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            output = function(inputs[0], inputs[1]) if len(inputs) == 2 else function(inputs[0])
        except:
            output = None

        if output == result: passed = passed + 1
        else: print("\n  Failed on:\n    "+name+"("+', '.join([str(i) for i in inputs])+")\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

try: interpret
except: print("The interpret() function is not defined.")
else: check('interpret', interpret, [\
    # (["print true;"], [True]),\
    # (["print 1 + 2 + 3;"], [6]),\
    # (["assign x := 3+4 ; print x*x+1;"], [50]),\
    # (["assign x := true; if x { print x; } print x;"], [True, True]),\
    # (["assign x := true; while x { print x; assign x := false; } print x;"], [True, False]),\
    # ([""], []),\
    # (["assign x := true; if x { while not ( x ) { print 123; } } print x;"], [True]),\
    # (["assign x := true; if x { while x xor false { print 123; assign x := x xor true; } } print x;"], [123, False]),\
    (["assign x := true; assign y := true; while x { while y { print x; assign y := x xor y; } assign x := x xor true; } print x; print y;"], [True, False, False]),\
    ])



