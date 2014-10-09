import json
import re


def tokenize(input,s):
    #creates a tokenize string
    spch = ["\\", "^", "$", ":=", ">", "<", ".", "|", ";", "#", "@", ",", "?", "*", "+", "(", ")", "[", "]", "{", "}"]

    tstring = "\s+|[0-9]+"

    # Now add the special chars with backslashes in front
    for i in input:
        if i in spch:
            i = '\\' + i

            tstring += "|" + i

    tokens = [token for token in re.split(r"("+tstring+")", s)]

    # Throw out the spaces and return the result.
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
        return ({"Number": [int(tokens.pop(0))]}, tokens)
    else:
        return None


def variable(tokens):
    if re.match(r"^[A-Za-z]*$", tokens[0]):
        return ({"Variable": [tokens.pop(0)]}, tokens)
    else:
        return None


def term(tokens):
    tok = tokens.pop(0)
    if tok == "#":
        return number(tokens)
    elif tok == "@":
        return variable(tokens)
    elif tok == "plus" and tokens.pop(0) == "(":
        (r, tokens) = term(tokens)  # Get the first entry
        if tokens.pop(0) == ",": #  Check for right syntax
            (s, tokens) = term(tokens)
            if tokens.pop(0) == ")":
                return ({"Plus": [r, s]}, tokens)
    elif tok == "mult" and tokens.pop(0) == "(":
        (r, tokens) = term(tokens)  # Get the first entry
        if tokens.pop(0) == ",": #  Check for right syntax
            (s, tokens) = term(tokens)
            if tokens.pop(0) == ")":
                return ({"Mult": [r, s]}, tokens)
    elif tok == "log" and tokens.pop(0) == "(":
        (r, tokens) = term(tokens)
        if tokens.pop(0) == ")":
            return ({"Log": [r]}, tokens)
    elif tok == "(":
        (r, tokens) = term(tokens)
        if r is not None:
            tok = tokens.pop(0)
            if tok == "+":
                (s, tokens) = term(tokens)
                if tokens.pop(0) == ")":
                    return ({"Plus": [r, s]}, tokens)
            elif tok == "*":
                (s, tokens) = term(tokens)
                if tokens.pop(0) == ")":
                    return ({"Mult": [r, s]}, tokens)
    else:
        return None, None

    return None, None


def formula(tokens):
    formulas = ["&&", "||", "true", "false"]
    terms = ["==", "<", ">", "#", "@", "log"]
    tok = tokens.pop(0)
    if tok == "true":
        return "True", tokens
    elif tok == "false":
        return "False", tokens
    elif tok == "less" and tokens.pop(0) == "(":
        (r, tokens) = term(tokens)
        if tokens.pop(0) == ",":
            (s, tokens) = term(tokens)
            if tokens.pop(0) == ")":
                return ({"LessThan": [r, s]}, tokens)
    elif tok == "greater" and tokens.pop(0) == "(":
        (r, tokens) = term(tokens)
        if tokens.pop(0) == ",":
            (s, tokens) = term(tokens)
            if tokens.pop(0) == ")":
                return ({"GreaterThan": [r, s]}, tokens)
    elif tok == "equal" and tokens.pop(0) == "(":
        (r, tokens) = term(tokens)
        if tokens.pop(0) == ",":
            (s, tokens) = term(tokens)
            if tokens.pop(0) == ")":
                return ({"Equal": [r, s]}, tokens)
    elif tok == "and" and tokens.pop(0) == "(":
        (r, tokens) = formula(tokens)
        if tokens.pop(0) == ",":
            (s, tokens) = formula(tokens)
            if tokens.pop(0) == ")":
                return ({"And": [r, s]}, tokens)
    elif tok == "or" and tokens.pop(0) == "(":
        (r, tokens) = formula(tokens)
        if tokens.pop(0) == ",":
            (s, tokens) = formula(tokens)
            if tokens.pop(0) == ")":
                return ({"Or": [r, s]}, tokens)
    elif tok == "not" and tokens.pop(0) == "(":
        (r, tokens) = formula(tokens)
        if r is not None:
            if tokens.pop(0) == ")":
                    return ({"Not": [r]}, tokens)
    elif tok == "(":

        if tokens[0] in terms:
            (r, tokens) = term(tokens)
            tok = tokens.pop(0)
            if tok == "==":
                (s, tokens) = term(tokens)
                if tokens.pop(0) == ")":
                    return ({"Equal": [r, s]}, tokens)
            elif tok == "<":
                (s, tokens) = term(tokens)
                if tokens.pop(0) == ")":
                    return ({"LessThan": [r, s]}, tokens)
            elif tok == ">":
                (s, tokens) = term(tokens)
                if tokens.pop(0) == ")":
                    return ({"GreaterThan": [r, s]}, tokens)
        elif tokens[0] in formulas:
            (r, tokens) = formula(tokens)
            tok = tokens.pop(0)
            if tok == "||":
                (s, tokens) = formula(tokens)
                if tokens.pop(0) == ")":
                    return ({"Or": [r, s]}, tokens)
            elif tok == "&&":
                (s, tokens) = formula(tokens)
                if tokens.pop(0) == ")":
                    return ({"And": [r, s]}, tokens)
    else:
        return None, None

    return None, None


def program(tokens):
    formulas = ["true", "false", "not", "and", "or", "equal", "less", "greater"]
    programs = ["print", "assign", "end"]
    terms = ["plus", "mult", "log", "@", "#"]
    tok = tokens.pop(0)
    if tok == "end" and tokens.pop(0) == ";":
        return "End"
    elif tok == "assign" and tokens.pop(0) == "@":
        r, tokens = variable(tokens)
        if tokens.pop(0) == ":=":
            s, tokens = term(tokens)
            if tokens.pop(0) == ";":
                return ({"Assign": [r, s, program(tokens)]})
    elif tok == "print":
        tok = tokens[0]
        if tok in formulas:
            (r, tokens) = formula(tokens)
            if tokens.pop(0) == ";":
                return ({"Print":[r, program(tokens)]})
        elif tok in terms:
            (r, tokens) = term(tokens)
            if tokens.pop(0) == ";":
                return ({"Print":[r, program(tokens)]})
        else:
            org = tokens[0:] # This was giving me a bug for a while. Didn't realize it created a reference and not a copy
            (r, tokens) = formula(tokens)
            if r is not None and tokens.pop(0) == ";":
                return ({"Print":[r, program(tokens)]})
            else:
                (r, tokens) = term(org)
                if r != None:
                    if tokens.pop(0) == ";":
                        return ({"Print":[r, program(tokens)]})
    else:
        return None, None

    return None, None



def complete(input):

    tokens = tokenize(['print', 'assign', 'end', 'true', 'false',
                   'not', 'and', 'or', 'equal', 'less', 'than',
                   'greater', 'plus', 'mult', 'log', '@', '#', ';',
                   ':=', '(', ')', ',', '+', '*', '&&', "||",
                   "==", "<", ">"], input)

    programs = ["print", "assign", "end"]
    formulas = ["true", "false", "not", "and", "or", "equal", "less", "greater"]
    terms = ["plus", "mult", "log", "@", "#"]

    #  Get rid of all the "thans"
    while "than" in tokens: tokens.remove("than") # Get rid of all the extra "than" tokens

    if tokens[0] in programs:
        return program(tokens)
    elif tokens[0] in formulas:
        return formula(tokens)
    elif tokens[0] in terms:
        return term(tokens)
    else:
        return None

