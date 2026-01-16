#include "dimacs.h"
#include "dpll.h"
#include "types.h"
#include <iostream>
#include <variant>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <dimacs_file>" << std::endl;
        return 1;
    }

    std::string filename = argv[1];

    try {
        auto [formula, num_vars] = DIMACSParser::parse(filename);

        std::cout << "Parsed formula with " << num_vars << " variables and " << formula.size() << " clauses" << std::endl;

        DPLLSolver solver(formula, num_vars);
        SATResult result = solver.solve();

        if (std::holds_alternative<std::vector<int>>(result)) {
            const auto& assignment = std::get<std::vector<int>>(result);
            std::cout << "SAT: " << std::endl;
            std::cout << "Assignment: ";
            for (size_t i = 0; i < assignment.size(); i++) {
                std::cout << assignment[i];
                // if (i < assignment.size() - 1) std::cout << " ";
            }
            std::cout << std::endl;
        } else {
            std::cout << "UNSAT" << std::endl;
        }

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
