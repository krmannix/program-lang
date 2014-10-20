exec(open('machine.py').read())
exec(open('interpret.py').read())
exec(open("parse.py").read())
import re, math
from random import randint


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
                ins1, addr1, heap = compileTerm(env, children[0], heap)
                ins2, addr2, heap = compileTerm(env, children[1], heap)
                ins, addr3, heap = addFromMem(addr1, addr2, heap)
                return ins1 + ins2 + ins, addr3, heap

    return None, None, None



def compileFormula(env, f, heap):
    if type(f) is dict:
        for label in f:
            children = f[label]
            if label == "And":
                ins1, addr1, heap = compileFormula(env, children[0], heap)
                ins2, addr2, heap = compileFormula(env, children[1], heap)
                ins3, addr3, heap = addFromMem(addr1, addr2, heap)
                ins3 += set(1, -1)
                ins4, addr4, heap = addFromMem(1, addr3, heap)
                rand_ = randint(0, 10000000)
                ins4 += ['branch setOne'+str(rand_) + ' ' + str(addr4)]
                ins4 += ['goto setZero'+str(rand_)]
                ins4 += ['label setOne'+str(rand_)]
                ins4 += set(addr4, 1)
                ins4 += ['goto afterSet'+str(rand_)]
                ins4 += ['label setZero'+str(rand_)]
                ins4 += set(addr4, 0)
                ins4 += ['label afterSet'+str(rand_)]
                return ins1 + ins2 + ins3 + ins4, addr4, heap
            elif label == "Or":
                ins1, addr1, heap = compileFormula(env, children[0], heap)
                ins2, addr2, heap = compileFormula(env, children[1], heap)
                ins3, addr3, heap = addFromMem(addr1, addr2, heap)
                rand_ = randint(0, 10000000)
                ins3 += ['branch setOne'+str(rand_) + ' ' + str(addr3)]
                ins3 += ['goto setZero'+str(rand_)]
                ins3 += ['label setOne'+str(rand_)]
                ins3 += set(addr3, 1)
                ins3 += ['goto afterSet'+str(rand_)]
                ins3 += ['label setZero'+str(rand_)]
                ins3 += set(addr3, 0)
                ins3 += ['label afterSet'+str(rand_)]
                return ins1 + ins2 + ins3, addr3, heap
            elif label == "Not":
                rand_ = randint(0, 10000000)
                ins_, addr, heap = compileFormula(env, children[0], heap)
                ins = copy(addr, heap)
                ins += ['branch setZero'+str(rand_) + ' ' + str(heap)]
                ins += ['goto setOne'+str(rand_)]
                ins += ['label setZero'+str(rand_)]
                ins += set(heap, 0)
                ins += ['goto afterSet'+str(rand_)]
                ins += ['label setOne'+str(rand_)]
                ins += set(heap, 1)
                ins += ['label afterSet'+str(rand_)]
                return ins_ + ins, heap, heap + 1
            elif label == "Variable":
                if env[children[0]] is not None:
                    return [], env[children[0]], heap
                else:
                    ins, addr, heap = storeVal(children[0], heap)
                    return ins, addr, heap

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
                    if children[1] != "End":
                        env, g, heap = compileProgram(env, children[1], heap)
                        return env, ins + h + g, heap
                    else:
                        return env, ins + h, heap
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
            elif label == "If":
                ins, addr, heap = compileExpression(env, children[0], heap)
                rand_ = randint(0, 10000000)
                ins += ['branch startIf'+str(rand_) + ' ' + str(addr)]
                ins += ['goto afterIf'+str(rand_)]
                ins += ['label startIf'+str(rand_)]
                env, ins_, heap = compileProgram(env, children[1], heap)
                ins += ins_
                ins += ['label afterIf'+str(rand_)]
                # Children 2 will always be End
                if len(children) > 2:
                    env, ins_, heap = compileProgram(env, children[2], heap)
                    return env, ins + ins_, heap
                else:
                    return env, ins, heap
            elif label == "While":
                rand_ = randint(0, 10000000)
                ins = ['label whileStart'+str(rand_)]
                ins_, addr, heap = compileExpression(env, children[0], heap)
                ins += ins_
                ins += ['branch continueLoop'+str(rand_) + ' ' + str(addr)]
                ins += ['goto afterLoop'+str(rand_)]
                ins += ['label continueLoop']
                env, ins_, heap = compileProgram(env, children[1], heap)
                ins += ins_
                ins += ['goto whileStart'+str(rand_)]
                ins += ['label afterLoop'+str(rand_)]
                if children[2]:
                    env, ins_, heap = compileProgram(env, children[2], heap)
                    return env, ins + ins_, heap
                else:
                    return env, ins, heap
            elif label == "Procedure":
                name = children[0]['Variable'][0]
                env, body, heap = compileProgram(env, children[1], heap)
                ins = procedure(name, body)
                if children[2] is not None:
                    env, ins_, heap = compileProgram(env, children[2], heap)
                    return env, ins + ins_, heap
                else:
                    return env, ins, heap
            elif label == "Call":
                name = children[0]['Variable'][0]
                ins = call(name)
                if children[1] is not None:
                    env, ins_, heap = compileProgram(env, children[1], heap)
                    return env, ins + ins_, heap
                else:
                    return env, ins, heap

    if s == "End":
        return env, [], heap

def compile(s):
    (env, o, heap) = compileProgram({}, tokenizeAndParse(s), 8) # Ignore this error, it's in parse.py
    initial = set(7, 0)
    # Set call stack to -1 in mem[7]
    return initial + o


#simulate(compile("procedure example {print 4;} call example;"))
#simulate(set(7, 0) + call("Hi"))
