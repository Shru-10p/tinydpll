import os
import subprocess
import tempfile
import sys
from pathlib import Path

# Allow importing from the 'scripts' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import generate

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
BINARY_PATH = (BASE_DIR / ".." / "build" / "tinydpll").resolve()


def _int_opt(value):
    if value is None or value == "":
        return None
    return int(value)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_formula():
    data = request.json or {}
    options = data.get('options', {})

    try:
        num_vars = _int_opt(options.get('num_vars')) or 50
        num_clauses = _int_opt(options.get('num_clauses')) or 200
        min_clause_length = _int_opt(options.get('min_clause_length')) or 2
        max_clause_length = _int_opt(options.get('max_clause_length')) or 4

        if min_clause_length < 1 or max_clause_length < min_clause_length:
            return jsonify({'error': 'Invalid clause length range'}), 400
        if num_vars < 1:
            return jsonify({'error': 'num_vars must be >= 1'}), 400

        cnf_content = generate.create_formula_string(
            num_vars=num_vars,
            num_clauses=num_clauses,
            min_clause_length=min_clause_length,
            max_clause_length=max_clause_length,
            seed=_int_opt(options.get('seed')),
        )
        return jsonify({'cnf': cnf_content})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/solve', methods=['POST'])
def solve_formula():
    cnf_content = (request.json or {}).get('cnf')

    if not cnf_content:
        return jsonify({'error': 'No CNF content provided'}), 400

    if not BINARY_PATH.exists() or not os.access(BINARY_PATH, os.X_OK):
        return jsonify({'error': f"Solver binary not found or not executable at {BINARY_PATH}"}), 500

    # 1. Write content to a temp file
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.cnf', delete=False) as temp:
        temp.write(cnf_content)
        temp_path = temp.name

    try:
        # 2. Run the C++ binary against the temp file
        result = subprocess.run(
            [str(BINARY_PATH), temp_path],
            capture_output=True,
            text=True,
            timeout=5  # Safety timeout
        )

        # 3. Return stdout/stderr
        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode
        })
    finally:
        # 4. Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)