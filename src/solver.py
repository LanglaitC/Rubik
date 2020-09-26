from src.cubik import Cubik

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
        (_ROTATE_UP, _COUNTER_CLOCKWISE_AXE, 1),    #U'
        (_ROTATE_UP, _CLOCKWISE_AXE, 2),            #U2
        (_ROTATE_DOWN, _CLOCKWISE_AXE, 1),          #D
        (_ROTATE_DOWN, _COUNTER_CLOCKWISE_AXE, 1),  #D'
        (_ROTATE_DOWN, _CLOCKWISE_AXE, 2),          #D2
        (_ROTATE_FRONT, _CLOCKWISE_AXE, 1),         #F
        (_ROTATE_FRONT, _COUNTER_CLOCKWISE_AXE, 1), #F'
        (_ROTATE_FRONT, _CLOCKWISE_AXE, 2),         #F2
        (_ROTATE_BACK, _CLOCKWISE_AXE, 1),          #B
        (_ROTATE_BACK, _COUNTER_CLOCKWISE_AXE, 1),  #B'
        (_ROTATE_BACK, _CLOCKWISE_AXE, 2),          #B2
        (_ROTATE_LEFT, _CLOCKWISE_AXE, 1),          #L
        (_ROTATE_LEFT, _COUNTER_CLOCKWISE_AXE, 1),  #L'
        (_ROTATE_LEFT, _CLOCKWISE_AXE, 2),          #L2   
        (_ROTATE_RIGHT, _CLOCKWISE_AXE, 1),         #R
        (_ROTATE_RIGHT, _COUNTER_CLOCKWISE_AXE, 1), #R'
        (_ROTATE_RIGHT, _CLOCKWISE_AXE, 2),         #R2
    )


    _PHASES = (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            [0, 1, 2, 3, 4, 5, 8, 11, 12, 13, 14, 15, 16, 17],
            [0, 1, 2, 3, 4, 5, 8, 11, 14, 17],
            [2, 5, 8, 11, 14, 17]
    )
    
    _VALID_APPENDIXES = [
        _INVERT_ROTATION_APPENDIX,
        _DOUBLE_MOVEMENT_APPENDIX
    ]

    _stack = []
    _states = []
    _initial_commands = []

    def __init__(self, cubik, commands):
        self.cubik = cubik
        self.parseCommands(commands)
        self.executeInitialCommands()
        self.solve()

    def addInitialComand(self, operator: str, direction, time_to_execute: int):
        self._initial_commands.append((operator, direction, time_to_execute))

    def executeInitialCommands(self):
        for command in self._initial_commands:
            self.cubik.rotateState(command[0], command[1], command[2])

    def parseCommands(self, raw_commands):
        for raw_command in raw_commands.split():
            time_to_execute = 1
            direction = self._CLOCKWISE_AXE
            if len(raw_command) > 2 or raw_command[0] not in self._VALID_COMMANDS:
                raise Exception(self._COMMAND_IS_NOT_VALID_MESSAGE.format(raw_command))
            if len(raw_command) == 2:
                if raw_command[1] == self._INVERT_ROTATION_APPENDIX:
                    direction = self._COUNTER_CLOCKWISE_AXE
                if raw_commands[1] == self._DOUBLE_MOVEMENT_APPENDIX:
                    time_to_execute += 1
            self.addInitialComand(raw_command[0], direction, time_to_execute)

    def solve(self):
        current_phase = 0
        goal = Cubik(list(range(20)) + 20 * [0])
        queue = [self.cubik]
        queue_set = set([queue[0].canGoToNextPhase(current_phase)])
        while current_phase != self._GOAL_PHASE:
            goToNextPhase = False
            state_goal = goal.canGoToNextPhase(current_phase)
            if queue[0].canGoToNextPhase(current_phase) == state_goal:
                queue_set = set([queue[0].canGoToNextPhase(current_phase)])
                print(queue[0].state)
                current_phase += 1
                print("Solved phase {} with moves {}".format(current_phase, queue[0].parent_moves_string()))
            else:
                next_queue = []
                for current_cubik in queue:
                    for moveIdx in self._PHASES[current_phase]:
                        next_cubik = Cubik(current_cubik.state[:], current_cubik.parents[:])
                        command = self._ALL_STATE_MOVES_VARIATION[moveIdx]
                        next_cubik.rotateState(command[0], command[1], command[2])
                        next_cubik.parents.append(moveIdx)
                        next_id = next_cubik.canGoToNextPhase(current_phase)
                        if (current_phase and next_cubik.canGoToNextPhase(current_phase - 1) != goal.canGoToNextPhase(current_phase -1)):
                            print(current_phase - 1 ,command)
                            print("!!!!!!!!!!!!!!!!!")
                            while(True):
                                pass
                        if (next_id == state_goal):
                            queue_set.add(next_id)
                            goToNextPhase = True
                            next_queue = [next_cubik]
                            break
                        elif next_id not in queue_set:
                            queue_set.add(next_id)
                            next_queue.append(next_cubik)
                    if goToNextPhase:
                        break
                queue = next_queue
                print(len(queue))

        return