#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())
exec(open('analyze.py').read())

Leaf = str
Node = dict

def addFromMem(addr1, addr2, heap):
    instrs = []
    instrs += copy(str(addr1), 1)
    instrs += copy(str(addr2), 2)
    instrs += ['add']
    instrs += copy(0, heap)
    return instrs, heap, heap + 1

def set(addr, val):
    return ['set ' + str(addr) + ' ' + str(val)]

def storeVal(val, addr):
    instrs = set(addr, val)
    return instrs, addr, addr + 1

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap+1)
            elif label == "Variable":
                if env[children[0]] is not None:
                    return [], env[children[0]], heap
                else:
                    ins, addr, heap = storeVal(children[0], heap)
                    return ins, addr, heap
            elif label == "Plus":
                ins1, addr1, heap = compileExpression(env, children[0], heap)
                ins2, addr2, heap = compileExpression(env, children[1], heap)
                ins3, addr3, heap = addFromMem(addr1, addr2, heap)
                return ins1 + ins2 + ins3, addr3, heap
            elif label == "Array":
                var = children[0]['Variable'][0]
                ins1, addr1, heap = compileExpression(env, children[1], heap)
                # addr1 has the offset
                ins2, addr2, heap = storeVal(env[var], heap)
                # addr2 has the start value
                # now, add them and put them in addr3
                ins3, addr3, heap = addFromMem(addr1, addr2, heap)
                ins4 = copyFromRef(addr3, heap)
                return ins1+ins2+ins3+ins4, heap, heap + 1
    else:
        #  This probably means it is True or False
        if e == "True":
            ins, addr, heap = storeVal(1, heap)
            return ins, addr, heap
        elif e == "False":
            ins, addr, heap = storeVal(0, heap)
            return ins, addr, heap

    pass # Complete 'True', 'False', 'Array', and 'Plus' cases for Problem #3.

def compileProgram(env, p, heap = 8): # Set initial heap default address.
    if type(p) == Leaf:
        if p == 'End':
            return (env, [], heap)

    if type(p) == Node:
        for label in p:
            children = p[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            elif label == 'Assign':
                [v, e1, e2, e3, p] = children
                (instsE1, addr1, heap) = compileExpression(env, e1, heap)
                (instsE2, addr2, heap) = compileExpression(env, e2, heap)
                (instsE3, addr3, heap) = compileExpression(env, e3, heap)
                env[v['Variable'][0]] = heap
                ins = []
                ins += copy(addr1, heap)
                ins += copy(addr2, heap+1)
                ins += copy(addr3, heap+2)
                env, instsE4, heap = compileProgram(env, p, heap+3)
                return (env, instsE1 + instsE2 + instsE3 + ins + instsE4, heap)


def compile(s):
    s_ = tokenizeAndParse(s)

    # Add call to type checking algorithm for Problem #4.
    g = typeProgram({}, s_)
    # Add calls to optimization algorithms for Problem #3.
    p_ = foldConstants(s_)
    p = unrollLoops(p_)


    (env, insts, heap) = compileProgram({}, p)
    return insts

def compileAndSimulate(s):
    comp = compile(s)
    return simulate(comp)

