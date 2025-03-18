import re

# Define token types and their regex patterns
TOKEN_PATTERNS = [
    ("MATRIX", re.compile(r"\[\[.*?\]\]")),
    ("COMPLEX", re.compile(r"\d*i")),
    ("DECIMAL", re.compile(r"\d+\.\d+")),
    ("INTEGER", re.compile(r"\d+")),
    ("FUNC_DEF", re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*\(x\)")),
    ("FUNC_CALL", re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*\(.*?\)")), 
    ("VAR", re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")),
    ("OP", re.compile(r"\+|\-|\*\*|\*|/|%|\^|=")),
    ("PAREN", re.compile(r"[\(\)]")),
]

def parse(tokens):
    if isinstance(tokens, list) and len(tokens) == 1:
        tokens = tokens[0]
    if any(t[0] == "FUNC_DEF" for t in tokens):
        return {"type": "FUNC_DEF", "tokens": tokens}
    if (tokens.count(("OP", "=")) == 1 and tokens[0][0] == "VAR" and tokens[1] == ("OP", "=")):
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
    if any(t[0] == "FUNC_CALL" for t in tokens):
        return {"type": "FUNC_CALL", "tokens": tokens}
    return {"type": "EXPRESSION", "tokens": tokens}

def tokenize(input):
    tokens = []
    index = 0
    while index < len(input):
        match = None
        for token_type, pattern in TOKEN_PATTERNS:
            match = pattern.match(input, index)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                index += len(value)
                break
        if not match:
            raise ValueError(f"Unexpected character at index {index}: {input[index]}")
    return handle_implicit_multiplication(group_parentheses(tokens))

def group_parentheses(tokens):
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
    return stack[0]

def handle_implicit_multiplication(tokens):
    """ Detects cases like 3x and converts them into 3 * x """
    new_tokens = []
    for i in range(len(tokens)):
        if i > 0 and tokens[i - 1][0] == "INTEGER" and tokens[i][0] == "VAR":
            new_tokens.append(tokens[i - 1])
            new_tokens.append(("OP", "*"))  # Insert implicit multiplication
        else:
            new_tokens.append(tokens[i])
    return new_tokens