#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4 (skeleton code)
# interpret.py
#

exec(open("parse.py").read())
Node = dict
LeafS = str
LeafI = int

def subst(s, a):
    if type(a) is dict:
        for label in a:
            children = a[label]
            if label == "Variable":
                # Check if s contains variable
                if children[0] in s:
                    key = list(s[children[0]])[0]
                    del a[label]
                    if len(children) > 1:
                        a_ = subst(s, children[1:])
                        a[key] = s[children[0]][key] + a_
                        return a
                    else:
                        a[key] = s[children[0]][key]
                        return a
                else:
                    return a

            else:
                #for child in children:
                for idx, child in enumerate(children):
                    g = subst(s, child)
                    children[idx] = g
                a[label] = children
                return a
                    #children[child]

def unify(a, b):
    v = type(a)
    if (type(a) == LeafS or type(a) == LeafI) and (type(b) == LeafS or type(b) == LeafI):
        return {}
    elif list(a.keys())[0] == "Variable":
        return {a["Variable"][0]: b}
    elif list(b.keys())[0] == "Variable":
        return {b["Variable"][0]: a}
    else:
        ac = a[list(a.keys())[0]]
        bc = b[list(b.keys())[0]]
        s = {}
        for idx, child in enumerate(ac):
            a_ = ac[idx]
            b_ = bc[idx]
            s_ = unify(a_, b_)
            for label in s_:
                if label in s:
                    return {}
            s = dict(s.items() + s_.items())
        return s


def build(m, d):
    pass # Complete for Problem #2, part (a).
  
def evaluate(m, env, e):
    pass # Complete for Problem #2, part (b).

def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof
#
# k = unify(parser(grammar, 'expression')("5"), parser(grammar, 'expression')("5"))
# print(k)