#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4 (skeleton code)
# interpret.py
#

exec(open("parse.py").read())

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


    pass # Complete for Problem #1, part (a).

def unify(a, b):
    pass # Complete for Problem #1, part (b).

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