CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -Iinclude
SRC_DIR = src
BUILD_DIR = build
INCLUDE_DIR = include
TARGET = $(BUILD_DIR)/tinydpll
OBJS = $(BUILD_DIR)/main.o $(BUILD_DIR)/dpll.o $(BUILD_DIR)/dimacs.o

all: $(BUILD_DIR) $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp $(INCLUDE_DIR)/dpll.h $(INCLUDE_DIR)/dimacs.h $(INCLUDE_DIR)/types.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/main.cpp -o $(BUILD_DIR)/main.o

$(BUILD_DIR)/dpll.o: $(SRC_DIR)/dpll.cpp $(INCLUDE_DIR)/dpll.h $(INCLUDE_DIR)/types.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/dpll.cpp -o $(BUILD_DIR)/dpll.o

$(BUILD_DIR)/dimacs.o: $(SRC_DIR)/dimacs.cpp $(INCLUDE_DIR)/dimacs.h $(INCLUDE_DIR)/types.h
	$(CXX) $(CXXFLAGS) -c $(SRC_DIR)/dimacs.cpp -o $(BUILD_DIR)/dimacs.o

clean:
	rm -rf $(BUILD_DIR)

# Build with debug symbols
debug: CXXFLAGS = -std=c++17 -Wall -Wextra -g -Iinclude
debug: all

.PHONY: all clean debug
