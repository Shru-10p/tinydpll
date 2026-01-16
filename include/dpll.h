#ifndef DPLL_H
#define DPLL_H

#include "types.h"
#include <unordered_map>
#include <vector>

class DPLLSolver {
public:
    DPLLSolver(const Formula& formula, int num_vars);

    SATResult solve();

private:
    Formula formula;
    int num_vars;
    std::vector<int> assignment;

    bool dpll(Formula& clauses);

    bool unit_propagate(Formula& clauses);

    bool pure_literal_eliminate(Formula& clauses);

    int choose_next_variable(const Formula& clauses);

    Formula simplify(const Formula& clauses, Literal lit);
    bool is_empty_clause(const Formula& clauses);
    bool is_satisfied(const Formula& clauses);
};

#endif