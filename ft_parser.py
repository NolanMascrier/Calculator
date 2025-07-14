"""Parsing functions. Uses regex to build the token list,
then adds missing symbols (like a * for 2x -> 2 * x).
Then it validates the input, and raises error should it not
be valid."""

import re

TOKEN_PATTERNS = [
    ("WHITESPACE", re.compile(r"\s")),
    ("MATRIX", re.compile(r"\[\[.*?\]\]")),
    ("COMPLEX", re.compile(r"-?(?:\d+(?:\.\d+)?|\.\d+)?i(?![\w.])")),
    ("DECIMAL", re.compile(r"-?\d+\.\d+")),
    ("FACT", re.compile(r"-?\d+!")),
    ("INTEGER", re.compile(r"-?\d+")),
    ("VAR", re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")),
    ("OP", re.compile(r"\+|\-|\*\*|\*|/|%|\^|=|\?")),
    ("PAREN", re.compile(r"[\(\)]")),
]

def parse(tokens):
    """Parse the token list and returns its mathematical type,
    a FUNC_DEF, a FUNC_CALL, an EQUATION, a VARIABLE_DISPLAY,
    an ASSIGNEMENT or an EXPRESSION. Returns EXPRESSION by
    default.
        
    Args:
        tokens (list): List of tokens.
        
    Returns:
        tuple: Filled list."""
    if isinstance(tokens, list) and len(tokens) == 1:
        tokens = tokens[0]
    if any(t[0] == "FUNC_DEF" for t in tokens):
        return {"type": "FUNC_DEF", "tokens": tokens}
    if (tokens.count(("OP", "=")) == 1 and tokens[0][0] == "VAR"\
                and tokens[1] == ("OP", "=")) and tokens[2] == ("OP", "?"):
        return {"type": "VARIABLE_DISPLAY", "tokens": tokens}
    if (tokens.count(("OP", "=")) == 1 and tokens[0][0] == "VAR"\
                and tokens[1] == ("OP", "=")):
        return {"type": "ASSIGNMENT", "tokens": tokens}
    if tokens.count(("OP", "=")) == 1:
        left, right = [], []
        split = False
        for t in tokens:
            if t == ("OP", "="):
                split = True
                continue
            (right if split else left).append(t)
        return {"type": "EQUATION", "tokens": tokens}
    return {"type": "EXPRESSION", "tokens": tokens}

def tokenize(input_value):
    """Takes the user input, parses it and creates a
    token list.
    
    Args:
        input_value (str): User input.
        
    Returns:
        list: A list of usable tokens."""
    tokens = []
    index = 0
    while index < len(input_value):
        match = None
        if re.match(r"[a-zA-Z_][a-zA-Z_0-9]*\(", input_value[index:]):
            name_match = re.match(r"[a-zA-Z_][a-zA-Z_0-9]*", input_value[index:])
            name = name_match.group(0)
            i = index + len(name)
            if input_value[i] != "(":
                raise ValueError(f"Expected '(' after function name at index {i}")
            i += 1
            depth = 1
            while i < len(input_value) and depth > 0:
                if input_value[i] == "(":
                    depth += 1
                elif input_value[i] == ")":
                    depth -= 1
                i += 1
            if depth != 0:
                raise ValueError(f"Unbalanced parentheses in function call starting at {index}")
            full = input_value[index:i]
            inner = full[len(name)+1:-1]
            token_type = "FUNC_DEF" if inner == "x" else "FUNC_CALL"
            tokens.append((token_type, full))
            index = i
            continue
        for token_type, pattern in TOKEN_PATTERNS:
            match = pattern.match(input_value, index)
            if match:
                value = match.group(0)
                if token_type == "WHITESPACE":
                    index += len(value)
                if token_type == "OP" and value == "-":
                    if not tokens or tokens[-1][0] in {"OP", "PAREN"}:
                        next_match = re.match(r"\d+(\.\d+)?", input_value[index + 1:])
                        if next_match:
                            value += next_match.group(0)
                            token_type = "DECIMAL" if "." in value else "INTEGER"
                            index += len(next_match.group(0))
                tokens.append((token_type, value))
                index += len(value)
                break
        if not match:
            raise ValueError(f"Unexpected character at index {index}: {input_value[index]}")
    return validate(group_parentheses(handle_implicit_multiplication((fill_missing(tokens)))))

def group_parentheses(tokens):
    """Regroup the list so that values between parenthesis are
    inside a sublist.
    
    Args:
        tokens (list): List of tokens.
        
    Returns:
        list: Regrouped list."""
    stack = [[]]
    for token in tokens:
        if token[0] == "PAREN" and token[1] == "(":
            stack.append([])
        elif token[0] == "PAREN" and token[1] == ")":
            group = stack.pop()
            stack[-1].append(group)
        else:
            stack[-1].append(token)
    if len(stack) != 1:
        raise ValueError("Mismatched parentheses in expression")
    if len(stack[0]) == 1 and isinstance(stack[0][0], list):
        return stack[0][0]
    return stack[0]

def handle_implicit_multiplication(tokens):
    """Detects cases like 3x or (x+1)2 and converts them into 3 * x or (x+1) * 2
        
    Args:
        tokens (list): List of tokens.
        
    Returns:
        list: Filled list."""
    new_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if i > 0 and tokens[i - 1][0] in ["INTEGER", "DECIMAL"] and token[0] == "VAR":
            new_tokens.append(("OP", "*"))
            new_tokens.append(token)
        elif i > 0 and tokens[i - 1][0] in ["INTEGER", "DECIMAL"] and token == ["PAREN", "("]:
            new_tokens.append(("OP", "*"))
            new_tokens.append(token)
        else:
            new_tokens.append(token)
        i += 1
    return new_tokens

def fill_missing(tokens):
    """Adds missing tokens ('OP', '+') in the equation. Also deletes
    uneeded whitespaces tokens.
    
    Args:
        tokens (list): List of tokens.
        
    Returns:
        list: Filled list.
    """
    new_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i][0] != "WHITESPACE":
            if tokens[i][0] not in ["OP", "FUNC_CALL", "FUNC_DEF", "VAR", "PAREN", "MATRIX"]\
                    and tokens[i][1][0] == '-'\
                    and tokens[i - 1] != ("OP", "*"):
                new_tokens.append(('OP', '-'))
                new_tokens.append((tokens[i][0], tokens[i][1][1:]))
            else:
                new_tokens.append(tokens[i])
        i += 1
    if new_tokens[0] == ('OP', '-'):
        new_tokens.insert(0, ('INTEGER', '0'))
    return new_tokens

def validate(tokens):
    """Checks the token list, and raises an error if needed.

    Args:
        tokens (list): Tokens to validate.

    Raises:
        SyntaxError: invalid syntax of the operation.
    
    Returns:
        list: unchange list.
    """
    for i, tok in enumerate(tokens):
        if isinstance(tok, list):
            validate(tok)
        elif i + 1 < len(tokens):
            if tok[0] != 'OP' and tokens[i + 1][0] != 'OP':
                raise SyntaxError("Two values, no operators !")
            if tok[0] == 'OP' and tokens[i + 1][0] == 'OP':
                raise SyntaxError("Two operators, no values !")
    return tokens
