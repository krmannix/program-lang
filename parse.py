from math import log, floor


def variable(ts):
    if type(ts[0]) is str:
        try:
            float(ts[0][0])
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
            return float(ts[0]), ts[1:]
        except ValueError:
            return None, None


# 1b
def formula(ts):
    e1, ts = left(ts)

    if e1 == None or ts == None:
        return None

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
        return None

    elif len(ts) != 0:
        if ts[0] == '+':
            e2, ts = term(ts[1:])
            return ({'Plus': [e1, e2]}, ts)

    return e1, ts


def factor(ts):
    e1, ts = leftfactor(ts)

    if e1 == None or ts == None:
        return None

    elif len(ts) != 0:
        if ts[0] == '*':
            e2, ts = factor(ts[1:])
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
    e1, t1 = formula(token)
    e2, t2 = term(token)

    if e1 is not None:
        return e1, t1
    elif e2 is not None:
        return e2, t2
    else:
        return None, None

def program(ts):
    if ts[0] == "print":
        e1, ts = expression(ts[1:])
        if ts[0] == ";":
            if (len(ts) > 1):
                return {"Print": [e1, program(ts[1:])]}, []
            else:
                return {"Print": [e1, "End"]}, []
    elif ts[0] == "assign":
        e1, ts = expression(ts[1:])
        if ts[0] == ":=":
            e2, ts = expression(ts[1:])
    elif ts[0] == "if":
        return "print"
    elif ts[0] == "while":
        return "print"
    elif ts[0] == "":
        return "End"


print("Problem #1, part (d), program()...")
try: program
except: print("The program() function is not defined.")
else: check('program', program, [\
    # (["print true ;".split(" ")], ({'Print': ['True', 'End']}, [])),\
    (["assign x := 3 + 4 ; print x * x ;".split(" ")], ({'Assign': [{'Variable': ['x']}, {'Plus': [{'Number': [3]}, {'Number': [4]}]}, {'Print': [{'Mult': [{'Variable': ['x']}, {'Variable': ['x']}]}, 'End']}]}, [])),\
    # (["assign x := true xor false ; print false ;".split(" ")], ({'Assign': [{'Variable': ['x']}, {'Xor': ['True', 'False']}, {'Print': ['False', 'End']}]}, [])),\
    # (["if true { print 1 ; } print 0 ;".split(" ")], ({'If': ['True', {'Print': [{'Number': [1]}, 'End']}, {'Print': [{'Number': [0]}, 'End']}]}, [])),\
    # (["while true { if false { print 0 ; } print 1 ; } print 2 ;".split(" ")], ({'While': ['True', {'If': ['False', {'Print': [{'Number': [0]}, 'End']}, {'Print': [{'Number': [1]}, 'End']}]}, {'Print': [{'Number': [2]}, 'End']}]}, [])),\
    # (["assign x := 1 + 2 ; while false { assign y := a xor b ; }".split(" ")], ({'Assign': [{'Variable': ['x']}, {'Plus': [{'Number': [1]}, {'Number': [2]}]}, {'While': ['False', {'Assign': [{'Variable': ['y']}, {'Xor': [{'Variable': ['a']}, {'Variable': ['b']}]}, 'End']}, 'End']}]}, [])),\
    # ([[]], ('End', [])),\
    # (["print 1 + 2 + log ( z ) + 0 ; assign y := 1 + 2 + log ( z ) + 0 ; print log ( 4 ) + y ;".split(" ")], ({'Print': [{'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'Log': [{'Variable': ['z']}]}, {'Number': [0]}]}]}]}, {'Assign': [{'Variable': ['y']}, {'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'Log': [{'Variable': ['z']}]}, {'Number': [0]}]}]}]}, {'Print': [{'Plus': [{'Log': [{'Number': [4]}]}, {'Variable': ['y']}]}, 'End']}]}]}, [])),\
    # (["assign x := true ; while x { assign x := false ; } print x ;".split(" ")], ({'Assign': [{'Variable': ['x']}, 'True', {'While': [{'Variable': ['x']}, {'Assign': [{'Variable': ['x']}, 'False', 'End']}, {'Print': [{'Variable': ['x']}, 'End']}]}]}, [])),\
    ])