import numpy as np

class Cubik():
    _COMMAND_IS_NOT_VALID_MESSAGE = 'Invalid command : {}'
    _INVERT_ROTATION_APPENDIX = '\''
    _DOUBLE_MOVEMENT_APPENDIX = '2'
    _FRONT_FACE_INDEX = 0
    _RIGHT_FACE_INDEX = 1
    _BACK_FACE_INDEX = 2
    _LEFT_FACE_INDEX = 3
    _UPPER_FACE_INDEX = 4
    _BOTTOM_FACE_INDEX = 5
    _CLOCKWISE_AXE = (0, 1)
    _COUNTER_CLOCKWISE_AXE = (1, 0)
    _ROTATE_FRONT = 'F'
    _ROTATE_RIGHT = 'R'
    _ROTATE_UP = 'U'
    _ROTATE_BACK = 'B'
    _ROTATE_LEFT = 'L'
    _ROTATE_DOWN = 'D'
    _CUBE_DIMENSION = 3
    _FACE_ROTATION = (
        ((0, 0), (1, 0), (2, 0)),
        ((0, 0), (0, 1), (0, 2)),
        ((0, 2), (1, 2), (2, 2)),
        ((2, 0), (2, 1), (2, 2)),
    )

    _COLORS = [
        '#ff0000', # Red
        '#00ff00', # Blue
        '#ffa500', # Orange
        '#0000ff', # Green
        '#ffffff', # White
        '#ffff00', # Yellow
    ]
    _ANSI_COLORS = [
        '\033[31m',
        '\033[34m',
        '\033[35m',
        '\033[32m',
        '\033[0m',
        '\033[33m',
    ]
    _faces = []

    _VALID_COMMANDS = {
        _ROTATE_FRONT: (
            _FRONT_FACE_INDEX,
            (
                _RIGHT_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _LEFT_FACE_INDEX,
                _UPPER_FACE_INDEX,
            )
        ),
        _ROTATE_RIGHT: (
            _RIGHT_FACE_INDEX,
            (
                _BACK_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _FRONT_FACE_INDEX,
                _UPPER_FACE_INDEX,
            )
        ),
        _ROTATE_UP: (
            _UPPER_FACE_INDEX,
            (
                _RIGHT_FACE_INDEX,
                _FRONT_FACE_INDEX,
                _LEFT_FACE_INDEX,
                _BACK_FACE_INDEX,
            )
        ),
        _ROTATE_DOWN: (
            _BOTTOM_FACE_INDEX,
            (
                _LEFT_FACE_INDEX,
                _FRONT_FACE_INDEX,
                _RIGHT_FACE_INDEX,
                _BACK_FACE_INDEX,
            )
        ),
        _ROTATE_LEFT: (
            _LEFT_FACE_INDEX,
            (
                _FRONT_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _BACK_FACE_INDEX,
                _UPPER_FACE_INDEX,
            )
        ),
        _ROTATE_BACK: (
            _BACK_FACE_INDEX,
            (
                _LEFT_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _RIGHT_FACE_INDEX,
                _UPPER_FACE_INDEX,
            )
        )
    }
    
    _VALID_APPENDIXES = [
        _INVERT_ROTATION_APPENDIX,
        _DOUBLE_MOVEMENT_APPENDIX
    ]


    _commands = []

    def __init__(self, raw_commands):
        self.fillFaces()
        self.parseCommands(raw_commands)
        self.executeCommands()

    def fillFaces(self):
        for color in self._COLORS:
            face = [[color for col in range(self._CUBE_DIMENSION)] for row in range(self._CUBE_DIMENSION)]
            self._faces.append(face)

    def addComand(self, operator, direction):
        self._commands.append((operator, direction))

    def getRow(self, faceIdx, coordinates):
        result = list()
        for coordinate in coordinates:
            result.append(self._faces[faceIdx][coordinate[0]][coordinate[1]])
        return result

    def executeCommands(self):
        for command in self._commands:
            self.rotate(command[0], command[1])

    def replaceRow(self, row: tuple, faceIdx: int, coordinates):
        for idx, rowElement in enumerate(row):
            self._faces[faceIdx][coordinates[idx][0]][coordinates[idx][1]] = rowElement

    def rotate(self, command: str, direction: int):
        faceToRotateIdx = self._VALID_COMMANDS[command][0]
        np.rot90(self._faces[faceToRotateIdx], axes=direction)
        neighbours = self._VALID_COMMANDS[command][1]
        firstRow = self.getRow(neighbours[0], self._FACE_ROTATION[0])
        for faceRotationIdx, faceIdx in enumerate(neighbours[0:-1]):
            tmp = self.getRow(neighbours[faceRotationIdx + 1], self._FACE_ROTATION[faceRotationIdx + 1])
            self.replaceRow(tmp, faceIdx, self._FACE_ROTATION[faceRotationIdx])
        self.replaceRow(firstRow, neighbours[len(neighbours) - 1], self._FACE_ROTATION[len(neighbours) - 1])
        return


    def parseCommands(self, raw_commands):
        for raw_command in raw_commands.split():
            direction = self._CLOCKWISE_AXE
            if len(raw_command) > 2 or raw_command[0] not in self._VALID_COMMANDS:
                raise Exception(self._COMMAND_IS_NOT_VALID_MESSAGE.format(raw_command))
            if len(raw_command) == 2:
                if raw_command[1] == self._INVERT_ROTATION_APPENDIX:
                    direction = self._COUNTER_CLOCKWISE_AXE
                if raw_commands[1] == self._DOUBLE_MOVEMENT_APPENDIX:
                    self.addComand(raw_command[0], direction)
            self.addComand(raw_command[0], direction)
        
    def debug(self):
        for faceIdx in range(len(self._COLORS)):
            for row in range(self._CUBE_DIMENSION):
                for col in range(self._CUBE_DIMENSION):
                    colorIdx = self._COLORS.index(self._faces[faceIdx][row][col])
                    print(self._ANSI_COLORS[colorIdx] + 'O', end='\033[0m ')
                print('\n', end='')
            print('\n', end='')