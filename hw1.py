import json
import re

def tokenize(tlist, inputs, *args):
    spchars = ['\\', '+', '*', '(', ')']
    tstring = "\s+"

    for term in tlist:
        # Special chars cause run-time errors, don't include them at this point
        if term not in spchars:
            tstring += "|" + term

    # Now add the special chars with backslashes in front
    for ch in spchars:
        if ch in tlist:
            tstring += "|\\" + ch

    # We should now have the full terminal list
    tokens = [t for t in re.split(r'('+tstring+')', inputs)]

    return [t for t in tokens if not t.isspace() and not t == ""]

def directions(dirs):
    while "turn" in dirs: dirs.remove("turn") # Get rid of all the extra "turn" tokens
    while ";" in dirs: dirs.remove(";") # Get rid of all the extra ";" tokens

    if len(dirs) > 2:
        parent = dirs.pop(0).strip()
        child = directions(dirs)
        if parent == 'forward':
            return {'Forward': [child]}
        elif parent == 'reverse':
            return {'Reverse': [child]}
        elif parent == 'left':
            return {'LeftTurn': [child]}
        elif parent == 'right':
            return {'RightTurn': [child]}
    else:
        # Base case. Just return the one object in a JSON form
        if dirs[0].strip() == 'forward':
            return {'Forward': ["Stop"]}
        elif dirs[0].strip() == 'reverse':
            return {'Reverse': ["Stop"]}
        elif dirs[0].strip() == 'left':
            return {'LeftTurn': ["Stop"]}
        elif dirs[0].strip() == 'right':
            return {'RightTurn': ["Stop"]}
        elif dirs[0].strip() == 'stop':
            return "Stop"

def number(tokens):
    if re.match(r"^([1-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens):
    if re.match(r"^[A-Za-z]*$", tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

def term(tokens):
    goodterms = ["log", "mult", "plus", "#", "@", "(", ")"]
    if tokens[0] in goodterms:
        token = tokens.pop(0)
        if token is not 0: # Make sure input has been good
            if token == "mult":
                return {'Mult': term(tokens)}
            elif token == "log":
                return {'Mult': term(tokens)}
            elif token == "(":
                tokens.pop(0)
                rarray = []
                for index, t in enumerate(tokens):
                    if t is "#":
                        rarray.append(number(t)[0])
                    elif t is "@":
                        rarray.append(variable(t)[0])
                    elif t is "mult" or "log":
                        rarray.append(term(tokens))
        else:
            return 0
    else:
        return 0

def formula(tokens):
    goodterms = ["true", "false", "not", "and", "or", "equal", "less", "than", "greater"]
    token = tokens.pop(0)
    if token in goodterms:
        if token == "less":
            return {"LessThan": formula(tokens)}
        elif token == "greater":
            return {"GreaterThan": formula(tokens)}
        elif token == "true":
            return {"True": formula(tokens)}
        elif token == "false":
            return {"False": formula(tokens)}
        elif token == "not":
            return {"Not": formula(tokens)}
        elif token == "or":
            return {"Or": formula(tokens)}
        elif token == "than"
            return formula(tokens)
    else:
        return 0

#def program(tokens):

