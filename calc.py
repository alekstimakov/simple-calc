"""
Этот файл должен содержать:
- Функцию calc(raw_expression).
- Любые вспомогательные функции.
"""
priority = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}

def calc(raw_expression):
    if not raw_expression:
        return None

    tokens = []
    number = ''
    dot_used = False
    prev_type = None  # operand, operator, open_paren, close_paren

    for char in raw_expression:
        if char.isdigit():
            number += char
            prev_type = "NUMBER"

        elif char == '.':
            if dot_used:
                return None
            dot_used = True
            number += char
            prev_type = "NUMBER"

        elif char in '+-*/':
            if prev_type != "NUMBER" and prev_type != "close_paren":
                return None

            if prev_type == "NUMBER":
                tokens.append({
                    "type": "operand",
                    "value": float(number)
                })
                number = ''
                dot_used = False

            tokens.append({
                "type": "operator",
                "value": char
            })
            prev_type = "operator"

        elif char == '(':
            if prev_type in ("NUMBER", "close_paren"):
                return None

            tokens.append({
                "type": "parenthesis",
                "value": '('
            })
            prev_type = "open_paren"

        elif char == ')':
            if prev_type not in ("NUMBER", "close_paren"):
                return None

            if prev_type == "NUMBER":
                tokens.append({
                    "type": "operand",
                    "value": float(number)
                })
                number = ''
                dot_used = False

            tokens.append({
                "type": "parenthesis",
                "value": ')'
            })
            prev_type = "close_paren"

        else:
            return None

    if prev_type == "NUMBER":
        tokens.append({
            "type": "operand",
            "value": float(number)
        })
    elif prev_type in ("operator", "open_paren"):
        return None

    if not tokens:
        return None

    return evaluate(tokens)


def apply_op(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return None
        return a / b


def evaluate(tokens):
    values = []
    ops = []

    for token in tokens:
        if token["type"] == "operand":
            values.append(token["value"])

        elif token["type"] == "operator":
            while (
                ops and
                ops[-1] != '(' and
                priority[ops[-1]] >= priority[token["value"]]
            ):
                if len(values) < 2:
                    return None
                b = values.pop()
                a = values.pop()
                op = ops.pop()
                result = apply_op(a, b, op)
                if result is None:
                    return None
                values.append(result)

            ops.append(token["value"])

        elif token["type"] == "parenthesis":
            if token["value"] == '(':
                ops.append('(')
            else:
                while ops and ops[-1] != '(':
                    if len(values) < 2:
                        return None
                    b = values.pop()
                    a = values.pop()
                    op = ops.pop()
                    result = apply_op(a, b, op)
                    if result is None:
                        return None
                    values.append(result)

                if not ops:
                    return None

                ops.pop()

    while ops:
        if ops[-1] == '(':
            return None
        if len(values) < 2:
            return None
        b = values.pop()
        a = values.pop()
        op = ops.pop()
        result = apply_op(a, b, op)
        if result is None:
            return None
        values.append(result)

    if len(values) == 1:
        return values[0]

    return None