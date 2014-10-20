exec(open('machine.py').read())
exec(open('interpret.py').read())
exec(open("parse.py").read())
import re, math


def compileExpression(env, e, heap): # Useful helper function.
    insTerm, addrTerm, heapTerm = compileTerm(env, e, heap)
    insForm, addrForm, heapForm = compileFormula(env, e, heap)
    if insTerm is not None:
        return insTerm, addrTerm, heapTerm
    elif insForm is not None:
        return insForm, addrForm, heapForm
    else:
        return [], None, heap

    # Variable needs to be changed in both accounts

# compile term should return env, instrs, and heap
def compileTerm(env, t, heap):
    if type(t) is dict:
        for label in t:
            children = t[label]
            if label == "Number":
                ins, addr, heap = storeVal(children[0], heap)
                return ins, addr, heap
            elif label == "Variable":
                if env[children[0]] is not None:
                    return [], env[children[0]], heap
                else:
                    ins, addr, heap = storeVal(children[0], heap)
                    return ins, addr, heap
            elif label == "Plus":
                print("Plus")
                print(children)
                ins1, addr1, heap = compileTerm(env, children[0], heap)
                ins2, addr2, heap = compileTerm(env, children[1], heap)
                ins, addr3, heap = addFromMem(addr1, addr2, heap)
                return ins1 + ins2 + ins, addr3, heap

    return None, None, None



def compileFormula(env, f, heap):
    if type(f) is dict:
        for label in f:
            children = f[label]
    else:
        #  This probably means it is True or False
        if f == "True":
            ins, addr, heap = storeVal(1, heap)
            return ins, addr, heap
        elif f == "False":
            ins, addr, heap = storeVal(0, heap)
            return ins, addr, heap
    return None, None, None



# Assign should remove 'Variable' from list. As in, it should get the variable and then
# call evaluate expression on children[1]
# Then call assignVal
# If we reach a variable, we should return it's address space
def compileProgram(env, s, heap):
    if type(s) is dict:
        for label in s:
            children = s[label]
            if label == "Print":
                ins, addr, heap = compileExpression(env, children[0], heap)
                h = printMem(addr)
                if children[1] is not None:
                    env, g, heap = compileProgram(env, children[1], heap)
                    return env, ins + h + g, heap
                else:
                    return env, ins + h, heap
            elif label == "Assign":
                var = children[0]["Variable"][0]
                ins, addr, heap = compileExpression(env, children[1], heap)
                env[var] = addr
                if children[2] is not None:
                    env, ins_, heap = compileProgram(env, children[2], heap)
                    return env, ins + ins_, heap
                else:
                    return env, ins, heap





    if s == "End":
        return env, [], heap

def compile(s):
    (env, o, heap) = compileProgram({}, tokenizeAndParse(s), 8) # Ignore this error, it's in parse.py
    return o

