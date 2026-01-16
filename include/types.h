#ifndef TYPES_H
#define TYPES_H

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <optional>
#include <variant>

typedef int Literal;
typedef std::vector<Literal> Clause;
typedef std::vector<Clause> Formula;

struct UNSAT {
    bool operator==(const UNSAT&) const { return true; }
};

typedef std::variant<std::vector<int>, UNSAT> SATResult;

inline int var(Literal lit) { return abs(lit); }
inline bool is_positive(Literal lit) { return lit > 0; }
inline Literal negate(Literal lit) { return -lit; }

#endif
