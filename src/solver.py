from src.cubik import Cubik
import time
from concurrent.futures import ThreadPoolExecutor

class Solver():
    _COMMAND_IS_NOT_VALID_MESSAGE = 'Invalid command : {}'
    _INVERT_ROTATION_APPENDIX = '\''
    _DOUBLE_MOVEMENT_APPENDIX = '2'
    _CLOCKWISE_AXE = (0, 1)
    _COUNTER_CLOCKWISE_AXE = (1, 0)
    _ROTATE_FRONT = 'F'
    _ROTATE_RIGHT = 'R'
    _ROTATE_UP = 'U'
    _ROTATE_BACK = 'B'
    _ROTATE_LEFT = 'L'
    _ROTATE_DOWN = 'D'
    _GOAL_PHASE = 4
    _VALID_COMMANDS = ('F', 'R', 'U', 'B', 'L', 'D')
    _CUBE_DIMENSION = 3
    _ALL_STATE_MOVES_VARIATION = (
        (_ROTATE_UP, _CLOCKWISE_AXE, 1),            #U
        (_ROTATE_UP, _CLOCKWISE_AXE, 2),            #U2
        (_ROTATE_UP, _COUNTER_CLOCKWISE_AXE, 1),    #U'
        (_ROTATE_DOWN, _CLOCKWISE_AXE, 1),          #D
        (_ROTATE_DOWN, _CLOCKWISE_AXE, 2),          #D2
        (_ROTATE_DOWN, _COUNTER_CLOCKWISE_AXE, 1),  #D'
        (_ROTATE_FRONT, _CLOCKWISE_AXE, 1),         #F
        (_ROTATE_FRONT, _CLOCKWISE_AXE, 2),         #F2
        (_ROTATE_FRONT, _COUNTER_CLOCKWISE_AXE, 1), #F'
        (_ROTATE_BACK, _CLOCKWISE_AXE, 1),          #B
        (_ROTATE_BACK, _CLOCKWISE_AXE, 2),          #B2
        (_ROTATE_BACK, _COUNTER_CLOCKWISE_AXE, 1),  #B'
        (_ROTATE_LEFT, _CLOCKWISE_AXE, 1),          #L
        (_ROTATE_LEFT, _CLOCKWISE_AXE, 2),          #L2   
        (_ROTATE_LEFT, _COUNTER_CLOCKWISE_AXE, 1),  #L'
        (_ROTATE_RIGHT, _CLOCKWISE_AXE, 1),         #R
        (_ROTATE_RIGHT, _CLOCKWISE_AXE, 2),         #R2
        (_ROTATE_RIGHT, _COUNTER_CLOCKWISE_AXE, 1), #R'
    )

    _MOVES_STRING = [
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

    _PHASES = (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            [0, 1, 2, 3, 4, 5, 7, 10, 12, 13, 14, 15, 16, 17],
            [0, 1, 2, 3, 4, 5, 7, 10, 13, 16],
            [1, 4, 7, 10, 13, 16],
    )
    
    _VALID_APPENDIXES = [
        _INVERT_ROTATION_APPENDIX,
        _DOUBLE_MOVEMENT_APPENDIX
    ]

    _stack = []
    _states = []
    _initial_commands = []

    def __init__(self, cubik, commands, verbose=False):
        self.cubik = cubik
        self.verbose = verbose
        self._initial_commands = self.parseCommands(commands)
        self.executeInitialCommands()

    def moveToMoveString(self, move):
        return self._MOVES_STRING[self._ALL_STATE_MOVES_VARIATION.index(move)]

    def executeInitialCommands(self):
        for command in self._initial_commands:
            self.cubik.rotateState(command[0], command[1], command[2])

    def parseCommands(self, raw_commands):
        commands = []
        for raw_command in raw_commands.split():
            time_to_execute = 1
            direction = self._CLOCKWISE_AXE
            if len(raw_command) > 2 or raw_command[0] not in self._VALID_COMMANDS:
                raise Exception(self._COMMAND_IS_NOT_VALID_MESSAGE.format(raw_command))
            if len(raw_command) == 2:
                if raw_command[1] == self._INVERT_ROTATION_APPENDIX:
                    direction = self._COUNTER_CLOCKWISE_AXE
                if raw_command[1] == self._DOUBLE_MOVEMENT_APPENDIX:
                    time_to_execute += 1
            commands.append((raw_command[0], direction, time_to_execute))
        return commands

    def rebuild_moves_string(self, moves):
        return " ".join([self._MOVES_STRING[move] for move in moves])

    def old_displayAdditionnalInformation(self, number_of_states, startTime, current_phase, cubik):
        print("Solved phase {} with {} moves: {}".format(current_phase, len(cubik.parents), cubik.parent_moves_string()))
        print("{} configuration where saved at the same time to resolve this phase".format(number_of_states))
        print("It took {} seconds".format(time.time() - startTime))
        print("------------------------------------------------------------------------------")

    def old_executeMovesForConfig(self, current_phase, current_cubik, queue_set, next_queue, state_goal):
        for moveIdx in self._PHASES[current_phase]:
            next_cubik = Cubik(current_cubik.state[:], current_cubik.parents[:])
            command = self._ALL_STATE_MOVES_VARIATION[moveIdx]
            next_cubik.rotateState(command[0], command[1], command[2])
            next_cubik.parents.append(moveIdx)
            next_id = next_cubik.canGoToNextPhase(current_phase)
            if (next_id == state_goal):
                queue_set.add(next_id)
                next_queue = [next_cubik]
                return True, next_queue
            elif next_id not in queue_set:
                queue_set.add(next_id)
                next_queue.append(next_cubik)
        return False, next_queue

    def old_solve(self):
        current_phase = 0
        goal = Cubik(list(range(20)) + 20 * [0])
        queue = [self.cubik]
        queue_set = set([queue[0].canGoToNextPhase(current_phase)])
        startTime = time.time()
        while current_phase != self._GOAL_PHASE:
            goToNextPhase = False
            state_goal = goal.canGoToNextPhase(current_phase)
            if queue[0].canGoToNextPhase(current_phase) == state_goal:
                current_phase += 1
                if (self.verbose):
                    self.old_displayAdditionnalInformation(len(queue_set), startTime, current_phase, queue[0])
                startTime = time.time()
                queue_set = set([queue[0].canGoToNextPhase(current_phase)])
            else:
                next_queue = []
                for current_cubik in queue:
                    goToNextPhase, next_queue = self.old_executeMovesForConfig(current_phase, current_cubik, queue_set, next_queue, state_goal)
                    if goToNextPhase:
                        break
                queue = next_queue
        return queue[0].parent_moves_string()

    def inverse(self, index):
        return index + 2 - 2 * (index % 3)

    def displayAdditionnalInformation(self, phase, moves, startTime, number_of_states):
        print("Solved phase {} with {} moves: {}".format(phase, len(moves), self.rebuild_moves_string(moves)))
        print("{} configuration where saved at the same time to resolve this phase".format(number_of_states))
        print("It took {} seconds".format(time.time() - startTime))
        print("------------------------------------------------------------------------------")

    def solve(self):
        moves = []
        current_cubik = self.cubik
        for phase in range(5):
            moves += self.solve_phase(phase, current_cubik)
            current_cubik = Cubik()
            for move in self._initial_commands:
                current_cubik.rotateState(move[0], move[1], move[2])
            for move in moves:
                command = self._ALL_STATE_MOVES_VARIATION[move]
                current_cubik.rotateState(command[0], command[1], command[2])
        return self.rebuild_moves_string(moves)

    def rebuild_algorithm(self, move, oldDir, newId, oldId, currentId, predecessor, goalId, lastMove):
        if oldDir > 1:
            temp = newId
            newId = oldId
            oldId = temp
            move = self.inverse(move)
        algorithm = [move]
        while oldId != currentId:
            algorithm.insert(0, lastMove[oldId])
            oldId = predecessor[oldId]
        while newId != goalId:
            algorithm.append(self.inverse(lastMove[newId]))
            newId = predecessor[newId]
        return algorithm

    def solve_phase(self, current_phase, current_cubik):
        startTime = time.time()
        goal_cubik = Cubik()
        queue = [current_cubik, goal_cubik]
        predecessor = {}
        lastMove = {}
        direction = {}
        currentId = current_cubik.canGoToNextPhase(current_phase)
        goalId = goal_cubik.canGoToNextPhase(current_phase)
        if (currentId == goalId):
            if (self.verbose):
                self.displayAdditionnalInformation(current_phase, [], startTime, 0)
            return []
        direction[currentId] = 1
        direction[goalId] = 2
        while True:
            oldState = queue.pop(0)
            oldId = oldState.canGoToNextPhase(current_phase)
            oldDir = direction[oldId]
            for move in self._PHASES[current_phase]:
                command = self._ALL_STATE_MOVES_VARIATION[move]
                newState = Cubik(oldState.state[:])
                newState.rotateState(command[0], command[1], command[2])
                newId = newState.canGoToNextPhase(current_phase)
                newDir = direction[newId] if newId in direction else None
                if (newDir and newDir != oldDir):
                    algoritm = self.rebuild_algorithm(move, oldDir, newId, oldId, currentId, predecessor, goalId, lastMove)
                    if (self.verbose):
                        self.displayAdditionnalInformation(current_phase, algoritm, startTime, len(direction))
                    return algoritm
                if (not newDir):
                    queue.append(newState)
                    direction[newId] = direction[oldId]
                    lastMove[newId] = move
                    predecessor[newId] = oldId