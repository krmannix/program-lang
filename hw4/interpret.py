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
    else:
        return a

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
            # if type(s_)
            if len(s_) > 0:
                if len(s) == 0:
                    s = s_
                else:
                    s = dict(list(s.items()) + list(s_.items()))
        return s
#
# def pattern(p):
#     if type(p) is Node:
#         for label in p:
#             children = p[label]
#             if label == "ConBase":
#                 return p
#             elif label == "Number":
#                 return p
#             elif


def build(m, d):
    if type(d) is Node:
        for label in d:
            children = d[label]
            if label == "Function":
                var = children[0]["Variable"][0]
                p = children[1]
                e = children[2]
                if var in m:
                    m[var] += [(p, e)]
                else:
                    m[var] = [(p, e)]
                if len(children) > 3:
                    m = build(m, children[3])
                    return m
                else:
                    return m
            else:
                return m
    else:
        return m
  
def evaluate(m, env, e):
    if type(e) is Node:
        for label in e:
            children = e[label]
            if label == "Apply":
                var = children[0]['Variable'][0]
                if var in m:
                    v_ = m[var] # v_ is a (program, expression) tuple
                    for idx, child in enumerate(v_):
                        p = v_[idx][0]
                        c_key = list(children[1])[0]
                        p_key = list(p)[0]
                        if c_key == p_key:
                            if len(children[1][c_key]) > 1 and len(children[1][c_key]) == len(p[p_key]):
                                env = unify(p, children[1])
                                a = subst(env, p)
                                return evaluate(m, env, a)
                            else:
                                if children[1][c_key] == p[p_key]:

                                    env = unify(p, children[1])
                                    return evaluate(m, env, v_[idx][1])
            elif label == "ConInd":
                e1 = evaluate(m, env, children[1])
                e2 = evaluate(m, env, children[2])
                #print(t)
            elif label == "ConBase":
                return e
            elif label == "Number":
                return e
            else:
                return e


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

# #eof
# j = parser(grammar, 'declaration')("f(x) = Test;")
# print(j)
# k = build({}, j)
# print(k)
evaluate(build({}, parser(grammar, 'declaration')("f(x) = Test;")), {}, parser(grammar, 'expression')("f(Test)"))