#!/usr/bin/env python3
"""
Test runner for TinyDPLL solver.
Generates random CNF formulas and tests the solver.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Add scripts directory to path for importing generate module
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
import generate


def run_solver(solver_path, cnf_content):
    """
    Run the solver on CNF content and return the result.
    Returns ('SAT'|'UNSAT'|'ERROR'|'TIMEOUT', output).
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
        f.write(cnf_content)
        temp_path = f.name

    try:
        result = subprocess.run(
            [str(solver_path), temp_path],
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
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_simple_sat():
    """Test a simple satisfiable formula."""
    cnf = """c Simple SAT test
p cnf 3 3
1 2 0
-1 3 0
-2 -3 0
"""
    return cnf, 'SAT', 'simple_sat'


def test_simple_unsat():
    """Test a simple unsatisfiable formula."""
    cnf = """c Simple UNSAT test
p cnf 1 2
1 0
-1 0
"""
    return cnf, 'UNSAT', 'simple_unsat'


def test_empty():
    """Test empty formula (trivially SAT)."""
    cnf = """c Empty formula
p cnf 0 0
"""
    return cnf, 'SAT', 'empty_formula'


def test_random_formulas(num_tests=5):
    """Generate random CNF formulas."""
    tests = []
    for i in range(num_tests):
        cnf = generate.create_formula_string(
            num_vars=10 + i * 10,
            num_clauses=30 + i * 20,
            min_clause_length=2,
            max_clause_length=3,
            # seed=42 + i # (Removed to increase randomness)
        )
        tests.append((cnf, None, f'random_{i+1}'))
    return tests


def main():
    solver_path = Path('build/tinydpll')

    if not solver_path.exists():
        print("Error: Solver binary not found at build/tinydpll")
        print("Please run 'make' to build the solver first.")
        sys.exit(1)

    # Collect test cases
    test_cases = [
        test_simple_sat(),
        test_simple_unsat(),
        test_empty(),
    ]
    test_cases.extend(test_random_formulas(5))

    print(f"Running TinyDPLL on {len(test_cases)} tests...\n")
    print("=" * 80)

    passed = 0
    failed = 0
    unknown = 0
    errors = 0

    results = []

    for cnf_content, expected, name in test_cases:
        actual, output = run_solver(solver_path, cnf_content)

        if actual in ['ERROR', 'TIMEOUT']:
            status = 'ERROR'
            errors += 1
            results.append((name, expected, actual, status, output))
        elif expected is None:
            status = 'UNKNOWN'
            unknown += 1
            results.append((name, expected, actual, status, None))
        elif expected == actual:
            status = 'PASS'
            passed += 1
            results.append((name, expected, actual, status, None))
        else:
            status = 'FAIL'
            failed += 1
            results.append((name, expected, actual, status, output))

    # Print results
    for name, expected, actual, status, details in results:
        expected_str = expected if expected else "?"
        print(f"{status:<12} {name:<40} Expected: {expected_str:<6} Got: {actual}")

        if status in ['FAIL', 'ERROR'] and details:
            print(f"  Details: {details[:200]}")
            if len(details) > 200:
                print("  ...")
            print()

    print("=" * 80)
    print(f"\nResults: {passed} passed, {failed} failed, {unknown} unknown, {errors} errors")
    print(f"Total: {len(test_cases)} tests")

    if failed > 0 or errors > 0:
        sys.exit(1)
    else:
        print(f"\nAll tests completed with no failures or errors.")
        sys.exit(0)


if __name__ == '__main__':
    main()
