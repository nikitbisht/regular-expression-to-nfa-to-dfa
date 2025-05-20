from flask import Flask, render_template, request
from regex_parser import infix_to_postfix
from nfa import build_nfa
from dfa import nfa_to_dfa
from draw import draw_nfa, draw_dfa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    regex = request.form['regex']
    try:
        postfix = infix_to_postfix(regex)
        nfa = build_nfa(postfix)

        draw_nfa(nfa, 'static/nfa')

        dfa_dict, start_state = nfa_to_dfa(nfa)
        draw_dfa(dfa_dict, start_state, 'static/dfa', nfa.accept)


        return render_template('result.html', regex=regex)
    except Exception as e:
        return f"Error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
