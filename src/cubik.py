import numpy as np
import math

class Cubik():
    _CLOCKWISE_AXE = (0, 1)
    _COUNTER_CLOCKWISE_AXE = (1, 0)
    _ROTATE_FRONT = 'F'
    _ROTATE_RIGHT = 'R'
    _ROTATE_UP = 'U'
    _ROTATE_BACK = 'B'
    _ROTATE_LEFT = 'L'
    _ROTATE_DOWN = 'D'
    _CUBE_DIMENSION = 3

    _FRONT_FACE_INDEX = 1
    _RIGHT_FACE_INDEX = 2
    _BACK_FACE_INDEX = 3
    _LEFT_FACE_INDEX = 0
    _UPPER_FACE_INDEX = 4
    _BOTTOM_FACE_INDEX = 5

    _COLORS = [
        '#ff0000', # Red
        '#00ff00', # Blue
        '#ffa500', # Orange
        '#0000ff', # Green
        '#ffffff', # White
        '#ffff00', # Yellow
    ]
    _ANSI_COLORS = [
        '\033[31m', # Red
        '\033[34m', # Blue
        '\033[35m', # Orange
        '\033[32m', # Green
        '\033[0m',  # White
        '\033[33m', # Yellow
    ]

    _STATE_MOVES = {
        _ROTATE_FRONT:  ((0, 9, 4, 8), (0, 3, 5, 4)), # Moves are : 4 rotating edges, 4 rotating corners
        _ROTATE_RIGHT: ((1 , 8, 5, 10), (1, 0, 4, 7)),
        _ROTATE_BACK: ((2, 10, 6, 11), (2, 1, 7, 6)),
        _ROTATE_LEFT: ((3, 11, 7 , 9), (3, 2, 6 , 5)),
        _ROTATE_UP: ((0, 1, 2, 3), (0, 1, 2, 3)),
        _ROTATE_DOWN: ((4, 7, 6, 5), (4, 5, 6, 7))
    }

    _VALID_COMMANDS = {
        _ROTATE_FRONT: (
            _FRONT_FACE_INDEX,
            (
                _RIGHT_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _LEFT_FACE_INDEX,
                _UPPER_FACE_INDEX,
            ),
            (
                ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (0, 1), (0, 0)),
                ((2, 0), (2, 1), (2, 2)),
                ((2, 0), (2, 1), (2, 2)),
            )
        ),
        _ROTATE_RIGHT: (
            _RIGHT_FACE_INDEX,
            (
                _UPPER_FACE_INDEX,
                _BACK_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _FRONT_FACE_INDEX,
            ),
            (
                ((0, 2), (1, 2), (2, 2)),
                ((0, 2), (1, 2), (2, 2)),
                ((0, 2), (1, 2), (2, 2)),
                ((0, 2), (1, 2), (2, 2))
            )
        ),
        _ROTATE_UP: (
            _UPPER_FACE_INDEX,
            (
                _RIGHT_FACE_INDEX,
                _FRONT_FACE_INDEX,
                _LEFT_FACE_INDEX,
                _BACK_FACE_INDEX,
            ),
            (
                ((0, 0), (1, 0), (2, 0)),
                ((0, 2), (0, 1), (0, 0)),
                ((2, 2), (1, 2), (0, 2)),
                ((2, 0), (2, 1), (2, 2)),
            )
        ),
        _ROTATE_DOWN: (
            _BOTTOM_FACE_INDEX,
            (
                _LEFT_FACE_INDEX,
                _FRONT_FACE_INDEX,
                _RIGHT_FACE_INDEX,
                _BACK_FACE_INDEX,
            ),
            (
                ((0, 0), (1, 0), (2, 0)),
                ((2, 0), (2, 1), (2, 2)),
                ((2, 2), (1, 2), (0, 2)),
                ((0, 2), (0, 1), (0, 0)),
            )
        ),
        _ROTATE_LEFT: (
            _LEFT_FACE_INDEX,
            (
                _BACK_FACE_INDEX,
                _UPPER_FACE_INDEX,
                _FRONT_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
            ),
            (
                ((0, 0), (1, 0), (2, 0)),
                ((0, 0), (1, 0), (2, 0)),
                ((0, 0), (1, 0), (2, 0)),
                ((0, 0), (1, 0), (2, 0))
            )
        ),
        _ROTATE_BACK: (
            _BACK_FACE_INDEX,
            (
                _LEFT_FACE_INDEX,
                _BOTTOM_FACE_INDEX,
                _RIGHT_FACE_INDEX,
                _UPPER_FACE_INDEX,
            ),
            (
                ((0, 0), (0, 1), (0, 2)),
                ((2, 2), (2, 1), (2, 0)),
                ((0, 0), (0, 1), (0, 2)),
                ((0, 0), (0, 1), (0, 2)),
            )
        )
    }

    _faces = []
    _goal = list(range(20)) + 20 * [0]
    state = list(range(20)) + 20 * [0]

    def __init__(self, state=_goal, parents=list(), fill_faces=False):
        self.state = state[:]
        self.parents = parents
        if (fill_faces):
            self.fillFaces()

    def fillFaces(self):
        for color in self._COLORS:
            face = [[color for col in range(self._CUBE_DIMENSION)] for row in range(self._CUBE_DIMENSION)]
            self._faces.append(face)

    def getRow(self, faceIdx, coordinates):
        result = list()
        for coordinate in coordinates:
            result.append(self._faces[faceIdx][coordinate[0]][coordinate[1]])
        return result

    def replaceRow(self, row: tuple, faceIdx: int, coordinates):
        for idx, rowElement in enumerate(row):
            self._faces[faceIdx][coordinates[idx][0]][coordinates[idx][1]] = rowElement
    
    def getEdgeOrientation(self, command, number):
        if command == self._ROTATE_FRONT or command == self._ROTATE_BACK:
            return 0 if number == 1 else 1
        return number

    def canGoToNextPhase(self, currentPhase):
        if currentPhase == 0:
            return tuple(self.state[20:32])
        if currentPhase == 1:
            result = self.state[31:40]
            for e in range(12):
                result[0] |= (math.floor(self.state[e] / 8)) << e
            return tuple(result)
        if currentPhase == 2:
            result = [0,0,0]
            for e in range(12):
                result[0] |= (2 if (self.state[e] > 7) else (self.state[e] & 1)) << (2*e)
            for c in range(8):
                result[1] |= ((self.state[c+12]-12) & 5) << (3*c)
            for i in range(12, 20):
                for j in range(i+1, 20):
                    result[2] ^= int(self.state[i] > self.state[j])
            return tuple(result)
        else:
            return tuple(self.state)

    def rotateState(self, command, direction, time_to_execute):
        direction = 1 if direction == self._CLOCKWISE_AXE else -1
        for turn in range(time_to_execute):
            old_state = list(self.state)
            cubies = self._STATE_MOVES[command]
            edges = cubies[0]
            corners = cubies[1]
            for edgeIdx, edge in enumerate(edges):
                newValue = old_state[edges[(edgeIdx + direction) % len(edges)]]
                newOrientation = self.getEdgeOrientation(command, old_state[edges[(edgeIdx + direction) % len(edges)] + 20])
                self.state[edge] = newValue
                self.state[edge + 20] = newOrientation
            for cornerIdx, corner in enumerate(corners):
                newValue = old_state[corners[(cornerIdx + direction) % len(corners)] + 12]
                orientationDelta = 0 if command == self._ROTATE_UP or command == self._ROTATE_DOWN else 2 - ((cornerIdx + 4) & 1)
                self.state[corner + 12] = newValue
                self.state[corner + 12 + 20] = old_state[corners[(cornerIdx + direction) % len(corners)] + 12 + 20] + orientationDelta
                if turn == time_to_execute -1:
                    self.state[corner + 12 + 20] %= 2 + 1

    def rotate(self, command: str, direction, time_to_execute):
        for _ in range(time_to_execute):
            faceToRotateIdx = self._VALID_COMMANDS[command][0]
            self._faces[faceToRotateIdx] = np.rot90(self._faces[faceToRotateIdx], axes=direction, k=-1)
            neighbours = self._VALID_COMMANDS[command][1]
            facesRotation = self._VALID_COMMANDS[command][2]
            if direction == self._CLOCKWISE_AXE:
                neighbours = tuple(reversed(neighbours))
                facesRotation = tuple(reversed(facesRotation))
            firstRow = self.getRow(neighbours[0], facesRotation[0])
            for faceRotationIdx, faceIdx in enumerate(neighbours[0:-1]):
                tmp = self.getRow(neighbours[faceRotationIdx + 1], facesRotation[faceRotationIdx + 1])
                self.replaceRow(tmp, faceIdx, facesRotation[faceRotationIdx])
            self.replaceRow(firstRow, neighbours[len(neighbours) - 1], facesRotation[len(neighbours) - 1])

    def print_single_face(self, faces, display_all_three=False):
        for row in range(3):
            for faceIdx, face in enumerate(faces):
                for col in range(3):
                    if (display_all_three or faceIdx == 1):
                        colorIdx = self._COLORS.index(face[row][col])
                        print(self._ANSI_COLORS[colorIdx] + 'O', end='\033[0m ')
                    else:
                        print(" ", end=" ")
            print("")
        
    def debug(self):
        empty_face = [[' ' for x in range(3)] for y in range(3)]
        self.print_single_face([empty_face, self._faces[self._BACK_FACE_INDEX], empty_face])
        self.print_single_face([self._faces[self._LEFT_FACE_INDEX], self._faces[self._UPPER_FACE_INDEX], self._faces[self._RIGHT_FACE_INDEX]], True)
        self.print_single_face([empty_face, self._faces[self._FRONT_FACE_INDEX], empty_face])
        self.print_single_face([empty_face, self._faces[self._BOTTOM_FACE_INDEX], empty_face])