import unittest
from src.cubik import Cubik

goal_state = [x for x in range(20)] + 20 * [0]

class TestStringMethods(unittest.TestCase):
    def test_F(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('F', cubik._CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [9, 1, 2, 3, 8, 5, 6, 7, 0, 4, 10, 11, 15, 13, 14, 17, 12, 16, 18, 19, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 2, 0, 0])

    def test_F2(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('F', cubik._CLOCKWISE_AXE, 2)
        self.assertEqual(cubik.state, [4, 1, 2, 3, 0, 5, 6, 7, 9, 8, 10, 11, 17, 13, 14, 16, 15, 12, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_FPRIME(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('F', cubik._COUNTER_CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [8, 1, 2, 3, 9, 5, 6, 7, 4, 0, 10, 11, 16, 13, 14, 12, 17, 15, 18, 19, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 2, 0, 0])
        
    def test_B(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('B', cubik._CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 1, 10, 3, 4, 5, 11, 7, 8, 9, 6, 2, 12, 19, 13, 15, 16, 17, 14, 18, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 0, 1, 2])

    def test_B2(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('B', cubik._CLOCKWISE_AXE, 2)
        self.assertEqual(cubik.state, [0, 1, 6, 3, 4, 5, 2, 7, 8, 9, 11, 10, 12, 18, 19, 15, 16, 17, 13, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_BPRIME(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('B', cubik._COUNTER_CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 1, 11, 3, 4, 5, 10, 7, 8, 9, 2, 6, 12, 14, 18, 15, 16, 17, 19, 13, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 0, 1, 2])

    def test_L(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('L', cubik._CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 1, 2, 11, 4, 5, 6, 9, 8, 3, 10, 7, 12, 13, 18, 14, 16, 15, 17, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0])

    def test_L2(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('L', cubik._CLOCKWISE_AXE, 2)
        self.assertEqual(cubik.state, [0, 1, 2, 7, 4, 5, 6, 3, 8, 11, 10, 9, 12, 13, 17, 18, 16, 14, 15, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_LPRIME(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('L', cubik._COUNTER_CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 1, 2, 9, 4, 5, 6, 11, 8, 7, 10, 3, 12, 13, 15, 17, 16, 18, 14, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0])
        
    def test_R(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('R', cubik._CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 8, 2, 3, 4, 10, 6, 7, 5, 9, 1, 11, 16, 12, 14, 15, 19, 17, 18, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 0, 0, 1])

    def test_R2(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('R', cubik._CLOCKWISE_AXE, 2)
        self.assertEqual(cubik.state, [0, 5, 2, 3, 4, 1, 6, 7, 10, 9, 8, 11, 19, 16, 14, 15, 13, 17, 18, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_RPRIME(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('R', cubik._COUNTER_CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 10, 2, 3, 4, 8, 6, 7, 1, 9, 5, 11, 13, 19, 14, 15, 12, 17, 18, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 0, 0, 1])

    def test_U(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('U', cubik._CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 12, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_U2(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('U', cubik._CLOCKWISE_AXE, 2)
        self.assertEqual(cubik.state, [2, 3, 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 12, 13, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_UPRIME(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('U', cubik._COUNTER_CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 15, 12, 13, 14, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_D(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('D', cubik._CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_D2(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('D', cubik._CLOCKWISE_AXE, 2)
        self.assertEqual(cubik.state, [0, 1, 2, 3, 6, 7, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 16, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_DPRIME(self):
        cubik = Cubik(goal_state[:])
        cubik.rotateState('D', cubik._COUNTER_CLOCKWISE_AXE, 1)
        self.assertEqual(cubik.state, [0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 19, 16, 17, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    

    



if __name__ == '__main__':
    unittest.main()