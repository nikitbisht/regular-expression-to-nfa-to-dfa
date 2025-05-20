import graphviz

def draw_nfa(nfa, path):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', size='4,10', dpi='1000')

    visited = set()
    state_names = {}  # Map from state id to 'qX' label
    counter = 0

    def get_name(state):
        nonlocal counter
        sid = id(state)
        if sid not in state_names:
            state_names[sid] = f'q{counter}'
            counter += 1
        return state_names[sid]

    def visit(state):
        sid = id(state)
        if sid in visited:
            return
        visited.add(sid)

        label = get_name(state)
        shape = 'doublecircle' if state == nfa.accept else 'circle'
        dot.node(label, shape=shape)

        for symbol, targets in state.edges.items():
            for t in targets:
                dot.edge(label, get_name(t), label=symbol)
                visit(t)
        for t in state.epsilon:
            dot.edge(label, get_name(t), label='ε')
            visit(t)

    visit(nfa.start)
    dot.render(path, format='png', cleanup=True)

def draw_dfa(dfa_dict, start_state, path, nfa_accept):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', size='4,4', dpi='1000')

    state_names = {}
    counter = 0

    def get_name(state_set):
        key = frozenset(state_set)
        if key not in state_names:
            state_names[key] = f'q{len(state_names)}'
        return state_names[key]

    for state_set in dfa_dict:
        name = get_name(state_set)
        # Final state if NFA accept state is in the set
        is_final = nfa_accept in state_set
        dot.node(name, shape='doublecircle' if is_final else 'circle')

    for state_set, transitions in dfa_dict.items():
        from_name = get_name(state_set)
        for symbol, target_set in transitions.items():
            to_name = get_name(target_set)
            dot.edge(from_name, to_name, label=symbol)

    dot.render(path, format='png', cleanup=True)

