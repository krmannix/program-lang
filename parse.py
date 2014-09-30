from math import log, floor


def variable(ts):
    if type(ts[0]) is str:
        if ts[0] == 'false' or ts[0] == 'true' or ts[0] == 'xor' or ts[0] == 'not':
            return None, None
        try:
            int(ts[0][0])
            return None, None
        except ValueError:
            if ts[0][0].islower():
                return ts[0], ts[1:]
    else:
        return None, None


def number(ts):
    if type(ts[0]) is int:
        return ts[0], ts[1:]
    else:
        try:
            return int(ts[0]), ts[1:]
        except ValueError:
            return None, None


# 1b
def formula(ts):
    e1, ts = left(ts)

    if e1 == None or ts == None:
        return None, None

    elif len(ts) != 0:
        if ts[0] == 'xor':
            e2, ts = formula(ts[1:])
            return {'Xor': [e1, e2]}, ts

    return e1, ts


def left(ts):
    if ts[0] == 'not':
        e1, ts = fparenthesis(ts[1:])
        return {'Not': [e1]}, ts

    if ts[0] == '(':
        e1, ts = fparenthesis(ts)
        return {'Parens': [e1]}, ts

    elif ts[0] == 'true':
        return 'True', ts[1:]

    elif ts[0] == 'false':
        return 'False', ts[1:]

    else:
        var, ts = variable(ts)
        if var != None:
            return {'Variable': [var]}, ts
        return None, None


def fparenthesis(ts):
    if ts[0] == '(':
        e1, ts = formula(ts[1:])
        if ts[0] == ')':
            return e1, ts[1:]


#1c

def term(ts):
    e1, ts = factor(ts)

    if e1 == None or ts == None:
        return None, None

    elif len(ts) != 0:
        if ts[0] == '+':
            e2, ts = term(ts[1:])
            return ({'Plus': [e1, e2]}, ts)

    return e1, ts


def factor(ts):
    e1, ts = leftfactor(ts)

    if e1 == None or ts == None:
        return None, None

    elif len(ts) != 0:
        if ts[0] == '*':
            e2, ts = factor(ts[1:]) # Put check for ; here?
            return ({'Mult': [e1, e2]}, ts)

    return e1, ts


def leftfactor(ts):
    if ts[0] == 'log':
        e1, ts = parenthesis(ts[1:])
        return {'Log': [e1]}, ts

    if ts[0] == '(':
        e1, ts = parenthesis(ts)
        return {'Parens': [e1]}, ts

    else:
        var, tsV = variable(ts)
        num, tsN = number(ts)
        if var != None:
            return {'Variable': [var]}, tsV
        elif num != None:
            return {'Number': [num]}, tsN

        return None, None


def parenthesis(ts):
    if ts[0] == '(':
        e1, ts = term(ts[1:])
        if ts[0] == ')':
            return e1, ts[1:]


def check(name, function, inputs_result_pairs):
    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            output = function(inputs[0], inputs[1]) if len(inputs) == 2 else function(inputs[0])
        except:
            output = None

        if output == result:
            passed = passed + 1
        else:
            print("\n  Failed on:\n    " + name + "(" + ', '.join(
                [str(i) for i in inputs]) + ")\n\n" + "  Should be:\n    " + str(
                result) + "\n\n" + "  Returned:\n    " + str(output) + "\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")


def expression(token):
    if len(token) > 1:
        e1, t1 = formula(token)
        e2, t2 = term(token)

    if (e1 is not None and t2 is None) or not (t2[0] == ";" or t2[0] == "{" or t2[0] == "}"):
        return e1, t1
    elif e2 is not None:
        return e2, t2
    else:
        return None, None

def program(ts):
    if ts is None or len(ts) is 0:
        return "End", []
    elif ts[0] == "print":
        e1, ts = expression(ts[1:])
        if ts[0] == ";":
            if (len(ts) > 1):
                if ts[1] == "}":
                    return {"Print": [e1, "End"]}, ts[1:]
                else:
                    e2, ts = program(ts[1:])
                    return {"Print": [e1, e2]}, ts
            else:
                return {"Print": [e1, "End"]}, []
    elif ts[0] == "assign":
        e1, ts = expression(ts[1:])
        if ts[0] == ":=":
            e2, ts = expression(ts[1:])
            if ts[0] == ";" and len(ts) == 1:
                return {"Assign": [e1, e2]}, []
            elif ts[0] == ";" and len(ts) > 1:
                if ts[1] == "}":
                    return {"Assign": [e1, e2, "End"]}, ts[1:]
                else:
                    e3, ts = program(ts[1:])
                    return {"Assign": [e1, e2, e3]}, []
    elif ts[0] == "if":
        e1, ts = expression(ts[1:])
        if ts[0] == "{":
            e2, ts = program(ts[1:])
            if ts[0] == "}":
                e3, ts = program(ts[1:]) # Possibly check for more ts here?
                if len(ts) > 1:
                    return {"If": [e1, e2, e3]}, ts
                else:
                    return {"If": [e1, e2, e3]}, []
    elif ts[0] == "while":
        e1, ts = expression(ts[1:])
        if ts[0] == "{":
            e2, ts = program(ts[1:])
            if ts[0] == "}":
                if len(ts) is 1:
                    return {"While": [e1, e2, "End"]}, []
                else:
                    e3, ts = program(ts[1:])
                    if len(ts) > 1:
                        return {"While": [e1, e2, e3]}, ts
                    else:
                        return {"While": [e1, e2, e3]}, []
    else:
        return None