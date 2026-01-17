#!/usr/bin/env python3
"""
Generates random DIMACS CNF files.
"""

import argparse
import random
from pathlib import Path


def generate_random_cnf(num_vars, num_clauses, min_clause_length=2, max_clause_length=4, seed=None):
    """Generate a random CNF formula."""
    if seed is not None:
        random.seed(seed)

    formula = []
    for _ in range(num_clauses):
        clause_length = random.randint(min_clause_length, max_clause_length)
        variables = random.sample(range(1, num_vars + 1), min(clause_length, num_vars))
        clause = [v if random.random() > 0.5 else -v for v in variables]
        formula.append(clause)

    return formula



def format_dimacs_string(formula, num_vars, comments=None):
    """Convert a formula into a DIMACS CNF string."""
    header = []
    if comments:
        for c in comments:
            header.append(f"c {c}")
    header.append(f"p cnf {num_vars} {len(formula)}")

    body = [" ".join(map(str, clause)) + " 0" for clause in formula]
    return "\n".join(header + body) + "\n"


def create_formula_string(
    num_vars=50,
    num_clauses=200,
    min_clause_length=2,
    max_clause_length=3,
    seed=None,
):
    """Generate and return a random DIMACS CNF string."""
    formula = generate_random_cnf(num_vars, num_clauses, min_clause_length, max_clause_length, seed)
    comments = [f"Random {max_clause_length}-SAT", f"vars={num_vars} clauses={num_clauses}"]
    return format_dimacs_string(formula, num_vars, comments=comments)


def get_unique_filename(base_dir, base_name):
    """
    Generate a unique filename. If the file exists, append (counter) to the name.
    """
    filepath = Path(base_dir) / f"{base_name}.cnf"

    if not filepath.exists():
        return filepath

    counter = 1
    while True:
        new_name = f"{base_name} ({counter})"
        filepath = Path(base_dir) / f"{new_name}.cnf"
        if not filepath.exists():
            return filepath
        counter += 1


def write_dimacs(formula, num_vars, filepath, comments=None):
    """Write a formula in DIMACS CNF format."""
    dimacs = format_dimacs_string(formula, num_vars, comments=comments)
    with open(filepath, 'w') as f:
        f.write(dimacs)


def main():
    parser = argparse.ArgumentParser(description='Generate random DIMACS CNF files')
    parser.add_argument('--vars', type=int, default=50, help='Number of variables (default: 50)')
    parser.add_argument('--clauses', type=int, default=200, help='Number of clauses (default: 200)')
    parser.add_argument('--min-clause-length', type=int, default=2, help='Minimum clause length (default: 2)')
    parser.add_argument('--max-clause-length', type=int, default=4, help='Maximum clause length (default: 4)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output file path (overrides default naming)')
    parser.add_argument('--count', type=int, default=1, help='Number of files to generate (default: 1)')
    parser.add_argument('--output-dir', type=str, default='tests/cnf', help='Output directory (default: tests/cnf)')

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(args.count):
        if args.output and args.count == 1:
            filepath = Path(args.output)
        else:
            if args.count > 1:
                base_name = f"random_{args.vars}_{args.clauses}_{i+1}"
            else:
                base_name = f"random_{args.vars}_{args.clauses}"
            filepath = get_unique_filename(output_dir, base_name)

        formula = generate_random_cnf(
            args.vars,
            args.clauses,
            args.min_clause_length,
            args.max_clause_length,
            args.seed if args.seed is None else args.seed + i,
        )

        comments = [f"Random {args.max_clause_length}-SAT", f"vars={args.vars} clauses={args.clauses}"]
        write_dimacs(formula, args.vars, filepath, comments=comments)

        print(f"Generated: {filepath}")
        print(f"  Variables: {args.vars}, Clauses: {len(formula)}")


if __name__ == '__main__':
    main()

