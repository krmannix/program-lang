#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#

exec(open('interpret.py').read())
exec(open('compile.py').read())

def expressions(n):
    if n <= 0:
        []
    elif n == 1:
        return ['True', 'False', {'Number':[2]}] # Add base case(s) for Problem #5.
    else:
        es = expressions(n-1)
        esN = []
        esN += [{'Array':[{'Variable': ['a']}, {'Number':[2]}]} for e1 in es]
        return es + esN

def programs(n):
    if n <= 0:
        []
    elif n == 1:
        return ['End']
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{'Assign':[{'Variable':['a']}, e, e, e, p]} for p in ps for e in es]
        psN += [{'Print':[e, p]} for p in ps for e in es]
        
        return ps + psN

# We always add a default assignment to the program in case
# there are variables in the parse tree returned from programs().

def defaultAssigns(p):
    return \
      {'Assign':[\
        {'Variable':['a']}, {'Number':[1]}, {'Number':[1]}, {'Number':[1]}, p\
      ]}

# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most 4.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

for p in [defaultAssigns(p) for p in programs(4)]:
    try:
        if simulate(compileProgram({}, unrollLoops(p))[1]) != execute({}, p)[1]:
            print('\nIncorrect behavior on: ' + str(p))
    except:
        print('\nError on: ' + str(p))

#eof