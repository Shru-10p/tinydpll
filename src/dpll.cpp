#include "dpll.h"
#include <algorithm>
#include <unordered_set>

DPLLSolver::DPLLSolver(const Formula& formula, int num_vars)
    : formula(formula), num_vars(num_vars) {
    assignment.resize(num_vars + 1, -1); // Index 0 unused, 1-indexed variables
}

SATResult DPLLSolver::solve() {
    Formula clauses = formula;

    if (dpll(clauses)) {
        // Convert assignment to vector of 0's and 1's
        std::vector<int> result;
        for (int i = 1; i <= num_vars; i++) {
            result.push_back(assignment[i]);
        }
        return result;
    } else {
        return UNSAT{};
    }
}

bool DPLLSolver::dpll(Formula& clauses) {
    if (is_satisfied(clauses)) {
        return true;
    }
    if (is_empty_clause(clauses)) {
        return false;
    }

    while (unit_propagate(clauses)) {
        if (is_satisfied(clauses)) {
            return true;
        }
        if (is_empty_clause(clauses)) {
            return false;
        }
    }

    while (pure_literal_eliminate(clauses)) {
        if (is_satisfied(clauses)) {
            return true;
        }
        if (is_empty_clause(clauses)) {
            return false;
        }
    }

    int var = choose_next_variable(clauses);
    if (var == -1) {
        return true;
    }

    // Try assigning true
    assignment[var] = 1;
    Formula simplified_true = simplify(clauses, var);
    if (dpll(simplified_true)) {
        return true;
    }

    // Try assigning false
    assignment[var] = 0;
    Formula simplified_false = simplify(clauses, -var);
    if (dpll(simplified_false)) {
        return true;
    }

    // Backtrack
    assignment[var] = -1;
    return false;
}

bool DPLLSolver::unit_propagate(Formula& clauses) {
    bool found_unit = false;

    for (const auto& clause : clauses) {
        if (clause.size() == 1) {
            Literal lit = clause[0];
            int v = var(lit);

            if (assignment[v] == -1) {
                assignment[v] = is_positive(lit) ? 1 : 0;
                clauses = simplify(clauses, lit);
                found_unit = true;
                break;
            }
        }
    }

    return found_unit;
}

bool DPLLSolver::pure_literal_eliminate(Formula& clauses) {
    std::unordered_set<Literal> literals;

    for (const auto& clause : clauses) {
        for (Literal lit : clause) {
            int v = var(lit);
            if (assignment[v] == -1) {
                literals.insert(lit);
            }
        }
    }

    for (Literal lit : literals) {
        if (literals.find(negate(lit)) == literals.end()) {
            // Pure literal found
            int v = var(lit);
            assignment[v] = is_positive(lit) ? 1 : 0;
            clauses = simplify(clauses, lit);
            return true;
        }
    }

    return false;
}

int DPLLSolver::choose_next_variable(const Formula& clauses) {
    // Choose first unassigned variable in clauses
    for (const auto& clause : clauses) {
        for (Literal lit : clause) {
            int v = var(lit);
            if (assignment[v] == -1) {
                return v;
            }
        }
    }
    return -1;
}

Formula DPLLSolver::simplify(const Formula& clauses, Literal lit) {
    Formula result;
    int v = var(lit);
    bool lit_value = is_positive(lit);

    for (const auto& clause : clauses) {
        bool satisfied = false;
        Clause new_clause;

        for (Literal l : clause) {
            if (var(l) == v) {
                // If literal matches assignment, clause is satisfied
                if (is_positive(l) == lit_value) {
                    satisfied = true;
                    break;
                }
                // Otherwise, just remove this literal from clause
            } else {
                new_clause.push_back(l);
            }
        }

        if (!satisfied) {
            result.push_back(new_clause);
        }
    }

    return result;
}

bool DPLLSolver::is_empty_clause(const Formula& clauses) {
    for (const auto& clause : clauses) {
        if (clause.empty()) {
            return true;
        }
    }
    return false;
}

bool DPLLSolver::is_satisfied(const Formula& clauses) {
    return clauses.empty();
}
