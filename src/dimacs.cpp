#include "dimacs.h"
#include <fstream>
#include <sstream>
#include <iostream>

std::pair<Formula, int> DIMACSParser::parse(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filename);
    }

    Formula formula;
    int num_vars = 0;
    int num_clauses = 0;
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == 'c') continue;

        if (line[0] == 'p') {
            std::istringstream iss(line);
            std::string p, cnf;
            iss >> p >> cnf >> num_vars >> num_clauses;
            continue;
        }

        std::istringstream iss(line);
        Clause clause;
        int lit;
        while (iss >> lit) {
            if (lit == 0) break;
            int var_num = abs(lit);
            if (var_num > num_vars || var_num < 1) {
                file.close();
                throw std::runtime_error("Literal " + std::to_string(lit) + " has variable " + std::to_string(var_num) + " out of range [1, " + std::to_string(num_vars) + "]");
            }
            clause.push_back(lit);
        }
        if (!clause.empty()) {
            formula.push_back(clause);
        }
    }

    file.close();
    return {formula, num_vars};
}
