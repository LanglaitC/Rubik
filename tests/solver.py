import unittest
from src.solver import Solver
from src.cubik import Cubik

goal_state = [x for x in range(20)] + 20 * [0]

class SolverMethods(unittest.TestCase):
    def testFirstSolution(self):
        shuffle = "F R B L"
        found_solution = "L B R' F R U B2 L2 U' R L2 U F2 U' F2 U R2 D' B2 F2 L2 U2 D2 B2 R2 F2 R2 U2"
        cubik = Cubik(goal_state[:])
        solver = Solver(cubik, shuffle + " " + found_solution)
        print(solver.cubik.state)
        self.assertEqual(solver.cubik.state, goal_state)

    def testSecondSolution(self):
        shuffle = "F R B L"
        found_solution = "F B D2 F2 D L' D' L"
        cubik = Cubik(goal_state)
        self.assertEqual(cubik.state, goal_state)
    

    



if __name__ == '__main__':
    unittest.main()