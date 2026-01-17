# TinyDPLL

A DPLL algorithm implementation for solving Boolean satisfiability (SAT) problems.

Live link: [Render Deployment](https://tinydpll.onrender.com)

This app is deployed on Render using a Docker image.

## Local Run

Run the web interface locally:

```bash
make clean && make && python3 web/app.py
```

Open http://localhost:5000 in your browser.

Optional: Run with Docker locally

```bash
docker build -t tinydpll .
docker run -p 5000:5000 tinydpll
```

**Features:**

- Generate random k-SAT formulas with custom parameters
- Visualize CNF formulas in DIMACS format
- View solution assignments

## Running Tests

The test runner generates test cases dynamically and validates the solver:

```bash
python3 tests/tests.py
```

**What it tests:**

- Simple satisfiable and unsatisfiable formulas
- Empty formula (trivially SAT)
- Randomly generated 3-SAT instances

Exit code 0 if all tests pass, 1 if any fail.

## DIMACS CNF Format

The standard DIMACS format for CNF formulas:

```none
c Example: (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3)
p cnf 3 3
1 2 0
-1 3 0
-2 -3 0
```

**Format Rules:**

- `c` lines are comments (ignored)
- `p cnf <num_vars> <num_clauses>` declares the problem
- Each clause is a space-separated list of literals ending with `0`
- Positive integers = positive literals (e.g., `3` means x3)
- Negative integers = negated literals (e.g., `-3` means ¬x3)

## Project Structure

```none
tinydpll/
├── include/
│   ├── types.h             # Core type definitions
│   ├── dimacs.h            # DIMACS parser interface
│   └── dpll.h              # DPLL solver class declaration
├── src/
│   ├── main.cpp            # CLI entry point and result output
│   ├── dimacs.cpp          # DIMACS file parser implementation
│   └── dpll.cpp            # Core DPLL algorithm implementation
├── scripts/
│   └── generate.py         # Random DIMACS formula generator
├── tests/
│   └── tests.py            # Automated test runner
├── web/
│   ├── app.py              # Flask web server
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # UI styling
│   │   └── js/
│   │       └── app.js      # Frontend logic
│   └── templates/
│       └── index.html      # Web interface
├── Dockerfile              # Container build for Render
├── render.yaml             # Render service config
├── .gitignore              # Git ignore rules
└── README.md               # This file
```
