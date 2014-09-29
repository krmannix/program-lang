from math import log, floor

def variable(ts):
    if type(ts[0]) is str:
        try:
            float(ts[0][0])
            return None
        except ValueError:
            if ts[0][0].islower():
                return ts[0], []
    else:
        return None


def number(ts):
    if type(ts[0]) is int:
        return ts[0], []
    else:
        try:
            return float(ts[0]), []
        except ValueError:
            return None


def formula(tokens):
    
    # This is so our xor fill have two "children"
    if len(tokens) > 1:
        if (tokens[1] == 'xor'):
            holder = tokens[0]
            tokens[0] = tokens[1]
            tokens[1] = holder

    if len(tokens) > 0:
        token = tokens.pop(0)
        if token == 'true':
            return 'True', formula(tokens)
        elif token == 'false':
            return 'False', formula(tokens)
        elif token == 'xor' and len(tokens) > 1:
            r, t1 = formula([tokens[0]])
            s, t2 = formula([tokens[1]])
            return {"Xor": [r, s]}#, formula(tokens[2:])
        elif token == 'not':
            return 'Not', formula(tokens)
        elif token == '(':

            return {'Parens': [formula(tokens[0:tokens.index(')')])]}, formula(tokens[(tokens.index(')')+1):])
        else:  # This is for variables
            if variable(token) is None:
                return None
            return variable(token), formula(tokens)
    else:
        return []