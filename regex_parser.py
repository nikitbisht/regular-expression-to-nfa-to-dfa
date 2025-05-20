def precedence(op):
    return {'*': 3, '.': 2, '|': 1}.get(op, 0)

def infix_to_postfix(regex):
    output = []
    stack = []

    # Insert explicit concatenation operator '.'
    explicit = ""
    for i in range(len(regex)):
        c = regex[i]
        if i > 0:
            prev = regex[i - 1]
            if (prev.isalnum() or prev == ')' or prev == '*') and (c.isalnum() or c == '('):
                explicit += '.'
        explicit += c

    for char in explicit:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(char):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())
    return ''.join(output)
