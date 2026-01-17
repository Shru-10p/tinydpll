#include "dimacs.h"
#include "dpll.h"
#include "types.h"
#include <iostream>
#include <variant>
#include <chrono>
#include <iomanip>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <dimacs_file>" << std::endl;
        return 1;
    }

    std::string filename = argv[1];

    try {
        auto [formula, num_vars] = DIMACSParser::parse(filename);

        // std::cout << "Parsed formula with " << num_vars << " variables and " << formula.size() << " clauses" << std::endl;

        DPLLSolver solver(formula, num_vars);

        auto start_time = std::chrono::high_resolution_clock::now();
        SATResult result = solver.solve();
        auto end_time = std::chrono::high_resolution_clock::now();

        auto duration = std::chrono::duration<double>(end_time - start_time);
        double cpu_time = duration.count();

        if (std::holds_alternative<std::vector<int>>(result)) {
            const auto& assignment = std::get<std::vector<int>>(result);
            std::cout << "SAT: ";
            for (size_t i = 0; i < assignment.size(); i++) {
                std::cout << assignment[i];
                // if (i < assignment.size() - 1) std::cout << " ";
            }
            std::cout << std::endl;
            std::cout << std::fixed << std::setprecision(3) << "CPU Time: " << cpu_time << "s" << std::endl;
        } else {
            std::cout << "UNSAT" << std::endl;
            std::cout << std::fixed << std::setprecision(3) << "CPU Time: " << cpu_time << "s" << std::endl;
        }

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
