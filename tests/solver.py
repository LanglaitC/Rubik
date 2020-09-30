import unittest
import math
import random
from src.solver import Solver
from src.cubik import Cubik

goal_state = [x for x in range(20)] + 20 * [0]
MOVES_STRING = [
    "U",
    "U2",
    "U'",
    "D",
    "D2",
    "D'",
    "F",
    "F2",
    "F'",
    "B",
    "B2",
    "B'",
    "L",
    "L2",
    "L'",
    "R",
    "R2",
    "R'",
]

class SolverMethods(unittest.TestCase):
    def testFirstSolution(self):
        shuffle = "F R B L"
        found_solution = "L B R' F R U B2 L2 U' R L2 U F2 U' F2 U R2 D' B2 F2 L2 U2 D2 B2 R2 F2 R2 U2"
        cubik = Cubik(goal_state[:])
        solver = Solver(cubik, shuffle + " " + found_solution)
        self.assertEqual(solver.cubik.state, goal_state)

    def testSecondSolution(self):
        shuffle = "B' L U D2 B R L U D B2 U"
        cubik = Cubik()
        solver = Solver(cubik, shuffle)
        solution = solver.solve()
        cubik = Cubik()
        solver = Solver(cubik, shuffle + " " + solution)
        self.assertEqual(solver.cubik.state, goal_state)

    def testRandomShortScramble(self):
        for _ in range(20):
            cubik = Cubik()
            shuffle = ' '.join([MOVES_STRING[random.randrange(0, 18)] for x in range(30)])
            solver = Solver(cubik, shuffle)
            solution = solver.solve()
            cubik = Cubik()
            solver = Solver(cubik, shuffle + " " + solution)
            self.assertEqual(solver.cubik.state, goal_state)

    def testRandomLongScramble(self):
        for _ in range(20):
            cubik = Cubik()
            shuffle = ' '.join([MOVES_STRING[random.randrange(0, 18)] for x in range(30)])
            solver = Solver(cubik, shuffle)
            solution = solver.solve()
            cubik = Cubik()
            solver = Solver(cubik, shuffle + " " + solution)
            self.assertEqual(solver.cubik.state, goal_state)

    def testParsing(self):
        shuffle = "U U2 U' D D2 D' F F2 F' B B2 B' L L2 L' R R2 R'"
        cubik = Cubik(goal_state[:])
        solver = Solver(cubik, shuffle)
        moves_indexes = [solver._ALL_STATE_MOVES_VARIATION.index(move) for move in solver._initial_commands]
        self.assertEqual(moves_indexes, list(range(18)))

    

    



if __name__ == '__main__':
    unittest.main()