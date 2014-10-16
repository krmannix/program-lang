exec(open('machine.py').read())
exec(open('interpret.py').read())
exec(open("parse.py").read())
import re, math

def convertBool(val):
    if val == True:
        return 1
    elif val == False:
        return 0


def compileExpression(env, e): # Useful helper function.
    envTerm, t = compileTerm(env, e)
    envForm, f = compileFormula(env, e)
    if t is not None:
        return env, t
    elif f is not None:
        return env, f
    else:
        return None, None

def compileTerm(env, t, heap):
    pass

def compileFormula(env, f, heap):
    pass

def compileProgram(env, s, heap):
    print(s)
    if type(s) is dict:
        for label in s:
            children = s[label]
            if label == "Print":
                env, e = compileExpression(env, children[0])
                print(e)
                if e is None:  # This means it is most likely a variable
                    var = children[0]["Variable"][0]
                    ins = printMem(env[var])
                else:  # Not a variable, just a normal value
                    if e == True or e == False:
                        e = convertBool(e)
                    ins = printVal(e)

                if children[1] is not None:
                    env, g, heap = compileProgram(env, children[1], heap)
                    return env, ins + g, heap
                else:
                    return env, ins, heap
            elif label == "Assign":
                var = children[0]["Variable"][0]
                env, e = compileExpression(env, children[1])
                if e == True or e == False:
                    e = convertBool(e)
                env[var], heap, ins = assignVal(heap, e)
                if children[2] is not None:
                    env, g, heap = compileProgram(env, children[2], heap)
                    return env, ins + g, heap
                else:
                    return env, ins, heap




    if s == "End":
        return env, [], heap

def compile(s):
    (env, o, heap) = compileProgram({}, tokenizeAndParse(s), 8) # Ignore this error, it's in parse.py
    return o

