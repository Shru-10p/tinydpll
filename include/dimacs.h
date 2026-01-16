#ifndef DIMACS_H
#define DIMACS_H

#include "types.h"
#include <string>
#include <utility>

class DIMACSParser {
public:
    static std::pair<Formula, int> parse(const std::string& filename);
};

#endif
