#!/usr/bin/env python3
"""
Test runner for TinyDPLL solver.
Runs the solver on all CNF files in tests/cnf/ and checks results against expected outcomes.
"""

import subprocess
import sys
from pathlib import Path

def parse_expected_result(cnf_file):
    """
    Parse the expected result (SAT/UNSAT) from comments in the CNF file.
    Returns 'SAT', 'UNSAT', or None if not specified.
    """
    try:
        with open(cnf_file, 'r') as f:
            for line in f:
                if line.startswith('c'):
                    # Look for "SAT" or "UNSAT" in comment
                    if 'Expected:' in line:
                        if 'UNSAT' in line:
                            return 'UNSAT'
                        elif 'SAT' in line:
                            return 'SAT'
                    # Also check for direct mentions
                    elif 'UNSAT' in line.upper() and 'EXPECTED' not in line.upper():
                        return 'UNSAT'
                    elif 'SAT' in line.upper() and 'UNSAT' not in line.upper():
                        return 'SAT'
                elif line.startswith('p'):
                    # Stop at problem line
                    break
    except Exception as e:
        print(f"Warning: Could not parse {cnf_file}: {e}")

    return None


def run_solver(solver_path, cnf_file):
    """
    Run the solver on a CNF file and return the result.
    Returns 'SAT', 'UNSAT', or 'ERROR' with error message.
    """
    try:
        result = subprocess.run(
            [solver_path, str(cnf_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout

        if 'UNSAT' in output:
            return 'UNSAT', output
        elif 'SAT' in output:
            return 'SAT', output
        else:
            return 'ERROR', f"Could not determine result from output:\n{output}"

    except subprocess.TimeoutExpired:
        return 'TIMEOUT', "Solver timed out after 30 seconds"
    except Exception as e:
        return 'ERROR', str(e)


def main():
    # Find solver binary
    solver_path = Path('build/tinydpll')

    if not solver_path.exists():
        print("Error: Solver binary not found at build/tinydpll")
        print("Please run 'make' to build the solver first.")
        sys.exit(1)

    # Find all CNF files
    cnf_dir = Path('tests/cnf')

    if not cnf_dir.exists():
        print(f"Error: Test directory {cnf_dir} does not exist")
        sys.exit(1)

    cnf_files = sorted(cnf_dir.glob('*.cnf'))

    if not cnf_files:
        print(f"No CNF files found in {cnf_dir}")
        sys.exit(0)

    print(f"Running TinyDPLL on {len(cnf_files)} test files...\n")
    print("=" * 80)

    passed = 0
    failed = 0
    unknown = 0
    errors = 0

    results = []

    for cnf_file in cnf_files:
        expected = parse_expected_result(cnf_file)
        actual, output = run_solver(solver_path, cnf_file)

        filename = cnf_file.name

        if actual in ['ERROR', 'TIMEOUT']:
            status = 'ERROR'
            errors += 1
            results.append((filename, expected, actual, status, output))
        elif expected is None:
            status = 'UNKNOWN'
            unknown += 1
            results.append((filename, expected, actual, status, None))
        elif expected == actual:
            status = 'PASS'
            passed += 1
            results.append((filename, expected, actual, status, None))
        else:
            status = 'FAIL'
            failed += 1
            results.append((filename, expected, actual, status, output))

    # Print results
    for filename, expected, actual, status, details in results:
        expected_str = expected if expected else "?"
        print(f"{status:<12} {filename:<40} Expected: {expected_str:<6} Got: {actual}")

        # Print details for failures and errors
        if status in ['FAIL', 'ERROR'] and details:
            print(f"  Details: {details[:200]}")
            if len(details) > 200:
                print("  ...")
            print()

    print("=" * 80)
    print(f"\nResults: {passed} passed, {failed} failed, {unknown} unknown, {errors} errors")
    print(f"Total: {len(cnf_files)} tests")

    if failed > 0 or errors > 0:
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
