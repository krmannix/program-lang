#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# analyze.py
# Modified by Kevin Mannix

exec(open("parse.py").read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'Boolean'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'Number'

            if label == 'Variable':
                [x, e]
                x = x['Variable'][0]
                if typeExpression(env, e) == 'Number':
                    return 'Number'

            elif label == 'Array':
                [x, e] = children
                x = x['Variable'][0]
                if x in env and env[x] == 'Array' and typeExpression(env, e) == 'Number':
                    return 'Number'

            elif label == 'Plus':
                [e0, e1] = children
                if typeExpression(env, e0) == 'Number' and\
                    typeExpression(env, e1) == 'Number':
                    return 'Number'

def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'Void'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                e_ = typeExpression(env, e)
                if typeProgram(env, p) == 'Void' and (e_ == 'Number' or e_ == 'Boolean'):
                    return 'Void'

            if label == 'Assign':
                [x, e0, e1, e2, p] = s[label]
                x = x['Variable'][0]
                if typeExpression(env, e0) == 'Number' and\
                   typeExpression(env, e1) == 'Number' and\
                   typeExpression(env, e2) == 'Number':
                     env[x] = 'Array'
                     if typeProgram(env, p) == 'Void':
                           return 'Void'

            if label == 'For':
                [x, p1, p2] = s[label]
                x = x['Variable'][0]
                if typeExpression(env, x) == 'Number' and typeProgram(env, p1) == 'Void' and typeProgram(env, p2) == 'Void':
                    return 'Void'

#eof