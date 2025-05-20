from collections import deque

def epsilon_closure(states):
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for e in state.epsilon:
            if e not in closure:
                closure.add(e)
                stack.append(e)
    return closure

def move(states, symbol):
    result = set()
    for state in states:
        if symbol in state.edges:
            for next_state in state.edges[symbol]:
                result.add(next_state)
    return result

def nfa_to_dfa(nfa):
    dfa_states = {}
    symbols = set()

    def get_symbols(state, visited):
        for sym in state.edges:
            if sym not in visited:
                symbols.add(sym)
                visited.add(sym)
        for e in state.epsilon:
            get_symbols(e, visited)

    get_symbols(nfa.start, set())

    start_closure = frozenset(epsilon_closure([nfa.start]))
    queue = deque([start_closure])
    dfa_states[start_closure] = {}

    while queue:
        current = queue.popleft()
        for symbol in symbols:
            if symbol == 'ε':
                continue
            move_result = epsilon_closure(move(current, symbol))
            if not move_result:
                continue
            frozen_move = frozenset(move_result)
            if frozen_move not in dfa_states:
                dfa_states[frozen_move] = {}
                queue.append(frozen_move)
            dfa_states[current][symbol] = frozen_move

    return dfa_states, start_closure
