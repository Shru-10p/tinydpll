# TinyDPLL - DPLL SAT Solver in C++

An mplementation of the DPLL algorithm for solving Boolean satisfiability (SAT) problems. Written in C++.

## Overview

TinyDPLL parses DIMACS CNF files and determines satisfiability using the DPLL algorithm with optimizations. The solver returns a satisfying assignment as a vector of 0's and 1's for SAT formulas

## Building

Build the project using the provided Makefile:

```bash
make
```

For debug builds with symbols:

```bash
make debug
```

Clean build artifacts:

```bash
make clean
```

## Usage

Run the solver with a DIMACS CNF file:

```bash
./build/tinydpll <file.cnf>
```

## Generating Test Cases

Use the included Python script to generate random DIMACS files:

```bash
# Generate with default parameters (50 vars, 200 clauses)
python3 scripts/generate.py

# Specify custom parameters
python3 scripts/generate.py --vars 100 --clauses 400

# Use a seed for reproducibility
python3 scripts/generate.py --vars 50 --clauses 200 --seed 42

# Control clause length
python3 scripts/generate.py --min-clause-length 3 --max-clause-length 6

# Custom output location
python3 scripts/generate.py -o tests/cnf/my_test.cnf --vars 75 --clauses 300
```

Then test the generated files:

```bash
./build/tinydpll tests/cnf/random_50_200.cnf
```

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
│   ├── types.h          # Core type definitions (SATResult, UNSAT, Formula)
│   ├── dimacs.h         # DIMACS parser interface
│   └── dpll.h           # DPLL solver class declaration
├── src/
│   ├── main.cpp         # CLI entry point and result output
│   ├── dimacs.cpp       # DIMACS file parser implementation
│   └── dpll.cpp         # Core DPLL algorithm implementation
├── scripts/
│   └── generate.py      # Random DIMACS file generator
├── tests/
│   ├── cnf/
│   │   └── *.cnf        # Test cases
│   └── check_all.py     # Check all test cases
├── build/               # Compiled binaries (created by make)
├── Makefile             # Build configuration
└── README.md            # This file
```
