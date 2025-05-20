class State:
    def __init__(self):
        self.edges = {}  # {symbol: [states]}
        self.epsilon = []

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def build_nfa(postfix):
    stack = []

    for char in postfix:
        if char.isalnum():
            s1 = State()
            s2 = State()
            s1.edges[char] = [s2]
            stack.append(NFA(s1, s2))

        elif char == '.':
            n2 = stack.pop()
            n1 = stack.pop()
            n1.accept.epsilon.append(n2.start)
            stack.append(NFA(n1.start, n2.accept))

        elif char == '|':
            n2 = stack.pop()
            n1 = stack.pop()
            s = State()
            a = State()
            s.epsilon.extend([n1.start, n2.start])
            n1.accept.epsilon.append(a)
            n2.accept.epsilon.append(a)
            stack.append(NFA(s, a))

        elif char == '*':
            n = stack.pop()
            s = State()
            a = State()
            s.epsilon.extend([n.start, a])
            n.accept.epsilon.extend([n.start, a])
            stack.append(NFA(s, a))

    return stack[-1]
