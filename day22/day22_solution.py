import enum
import re
from collections.abc import Iterator
from typing import Self, Literal, NamedTuple

import numpy as np


example_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

def as_tuple(value: np.array) -> tuple:
    """Turn mutable numpy array into immutable and hashable tuple."""
    match len(value.shape):
        case 1:
            return tuple(value)
        case 2:
            return tuple(map(tuple, value))
        case _:
            raise NotImplementedError


@enum.verify(enum.UNIQUE)
class Rotation(enum.Enum):
    IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    X_90 = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
    X_180 = as_tuple(np.linalg.matrix_power(np.array(X_90), 2))
    X_270 = as_tuple(np.linalg.matrix_power(np.array(X_90), 3))

    Y_90 = ((0, 0, -1), (0, 1, 0), (1, 0, 0))
    Y_180 = as_tuple(np.linalg.matrix_power(np.array(Y_90), 2))
    Y_270 = as_tuple(np.linalg.matrix_power(np.array(Y_90), 3))

    Z_90 = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
    Z_180 = as_tuple(np.linalg.matrix_power(np.array(Z_90), 2))
    Z_270 = as_tuple(np.linalg.matrix_power(np.array(Z_90), 3))

    def inverse(self) -> Self:
        """Return inverse rotation."""
        return Rotation(as_tuple(np.array(self.value).transpose()))

    def __matmul__(self, other):
        if isinstance(other, Rotation):
            return Rotation(as_tuple(np.array(self.value) @ other.value))
        else:
            return NotImplemented


@enum.verify(enum.UNIQUE)
class Direction(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __matmul__(self, other):
        if isinstance(other, Rotation):
            return Direction(as_tuple(self.value @ np.array(other.value)[:2, :2]))
        else:
            return NotImplemented


@enum.verify(enum.UNIQUE)
class CubeFace(enum.Enum):
    """
      D
    B A C
      E
      F
    """
    A_0 = (Rotation.IDENTITY, Rotation.IDENTITY)
    A_90 = (Rotation.IDENTITY, Rotation.Z_90)
    A_180 = (Rotation.IDENTITY, Rotation.Z_180)
    A_270 = (Rotation.IDENTITY, Rotation.Z_270)

    B_0 = (Rotation.Y_270, Rotation.IDENTITY)
    B_90 = (Rotation.Y_270, Rotation.Z_90)
    B_180 = (Rotation.Y_270, Rotation.Z_180)
    B_270 = (Rotation.Y_270, Rotation.Z_270)

    C_0 = (Rotation.Y_90, Rotation.IDENTITY)
    C_90 = (Rotation.Y_90, Rotation.Z_90)
    C_180 = (Rotation.Y_90, Rotation.Z_180)
    C_270 = (Rotation.Y_90, Rotation.Z_270)

    D_0 = (Rotation.X_270, Rotation.IDENTITY)
    D_90 = (Rotation.X_270, Rotation.Z_90)
    D_180 = (Rotation.X_270, Rotation.Z_180)
    D_270 = (Rotation.X_270, Rotation.Z_270)

    E_0 = (Rotation.X_90, Rotation.IDENTITY)
    E_90 = (Rotation.X_90, Rotation.Z_90)
    E_180 = (Rotation.X_90, Rotation.Z_180)
    E_270 = (Rotation.X_90, Rotation.Z_270)

    F_0 = (Rotation.X_180, Rotation.IDENTITY)
    F_90 = (Rotation.X_180, Rotation.Z_90)
    F_180 = (Rotation.X_180, Rotation.Z_180)
    F_270 = (Rotation.X_180, Rotation.Z_270)

    @property
    def identity(self) -> 'CubeFaceIdentity':
        return CubeFace(self._identity_value)

    def __new__(cls, identity, rotation):
        obj = object.__new__(cls)
        obj._value_ = as_tuple(np.array(identity.value) @ rotation.value)
        obj._identity_value = identity.value
        obj.rotation = rotation
        return obj

    def __matmul__(self, other):
        if isinstance(other, Rotation):
            return CubeFace(as_tuple(np.array(self.value) @ other.value))
        else:
            return NotImplemented


class Coordinate(NamedTuple):
    y: int
    x: int

    def translate(self, diff_x=0, diff_y=0) -> Self:
        """Move coordinate by `diff_x` and `diff_y`."""
        return Coordinate(x=self.x + diff_x, y=self.y + diff_y)


class CubeFaceProjection(NamedTuple):
    face: CubeFace
    min_coord: Coordinate
    face_size: int

    @property
    def max_coord(self):
        return Coordinate(x=self.min_coord.x + self.face_size - 1, y=self.min_coord.y + self.face_size - 1)

    def contains(self, coord):
        return self.min_coord.x <= coord.x < (self.min_coord.x + self.face_size) and\
            self.min_coord.y <= coord.y < (self.min_coord.y + self.face_size)

    def translate(self, projection: Self, coord: Coordinate, self_direct: Direction) -> tuple[Coordinate, Direction]:
        """Translate coordinate and direction from `projection` to self."""
        diff_rotation = self.face.rotation @ projection.face.rotation.inverse()

        rotation_origin = ((projection.face_size - 1) / 2, (projection.face_size - 1) / 2, 0)
        self_coord_raw = np.array((coord.x, coord.y, 0), dtype='float')
        self_coord_raw -= (projection.min_coord.x, projection.min_coord.y, 0)
        self_coord_raw -= rotation_origin
        self_coord_raw = self_coord_raw @ diff_rotation.value
        self_coord_raw += rotation_origin
        self_coord_raw += (self.min_coord.x, self.min_coord.y, 0)
        self_coord = Coordinate(x=int(self_coord_raw[0]), y=int(self_coord_raw[1]))

        self_direct = self_direct @ diff_rotation

        return self_coord, self_direct


CubeFaceIdentity = Literal[CubeFace.A_0, CubeFace.B_0, CubeFace.C_0, CubeFace.D_0, CubeFace.E_0, CubeFace.F_0]


class CaveMap:
    layout: np.array
    path: list[int | Literal['L', 'R']]
    projections: dict[CubeFaceIdentity, CubeFaceProjection]

    def __init__(self, input: str):
        lines = input.splitlines()

        layout_shape = (len(lines) - 2, max(map(len, lines[:-2])))
        self.layout = np.full(layout_shape, ' ', dtype='<U1')
        for y, line in enumerate(lines[:-2]):
            for x, char in enumerate(line):
                self.layout[Coordinate(x=x, y=y)] = char

        self.path = []
        for p in re.findall(r'\d+|L|R', lines[-1]):
            try:
                self.path.append(int(p))
            except ValueError:
                self.path.append(p)

        self.projections = {}
        cube_face_size = max(layout_shape) // 4
        seen_nodes: set[Coordinate] = set()
        nodes: list[tuple[Coordinate, CubeFace]] = [
            (
                Coordinate(x=next(i for i, char in enumerate(lines[0]) if char != ' '), y=0),
                CubeFace.A_0
            )
        ]
        while len(nodes):
            coord, face = nodes.pop()

            if coord in seen_nodes:
                continue

            seen_nodes.add(coord)

            self.projections[face.identity] = CubeFaceProjection(face, coord, cube_face_size)

            top_face_coord = coord.translate(diff_y=-cube_face_size)
            if top_face_coord.y >= 0 and self.layout[top_face_coord] != ' ':
                nodes.append((top_face_coord, face @ Rotation.X_270))

            left_face_coord = coord.translate(diff_x=-cube_face_size)
            if left_face_coord.x >= 0 and self.layout[left_face_coord] != ' ':
                nodes.append((left_face_coord, face @ Rotation.Y_270))

            bottom_face_coord = coord.translate(diff_y=cube_face_size)
            if bottom_face_coord.y < self.layout.shape[0] and self.layout[bottom_face_coord] != ' ':
                nodes.append((bottom_face_coord, face @ Rotation.X_90))

            right_face_coord = coord.translate(diff_x=cube_face_size)
            if right_face_coord.x < self.layout.shape[1] and self.layout[right_face_coord] != ' ':
                nodes.append((right_face_coord, face @ Rotation.Y_90))

    def wrap_coordinate(self, face: CubeFace, coord: Coordinate, direct: Direction) -> tuple[CubeFace, Coordinate, Direction]:
        """Wrap coordinate if needed."""
        projection = self.projections[face.identity]

        if coord.y < projection.min_coord.y:
            wouldbe_face = face @ Rotation.X_270
        elif coord.x < projection.min_coord.x:
            wouldbe_face = face @ Rotation.Y_270
        elif coord.y > projection.max_coord.y:
            wouldbe_face = face @ Rotation.X_90
        elif coord.x > projection.max_coord.x:
            wouldbe_face = face @ Rotation.Y_90
        else:
            # Still within current face, no wrapping needed.
            return face, coord, direct

        if 0 <= coord.x < self.layout.shape[1] and 0 <= coord.y < self.layout.shape[0] and self.layout[coord] != ' ':
            # "would be" face exists, no wrapping needed.
            return wouldbe_face, coord, direct

        wouldbe_projection = CubeFaceProjection(wouldbe_face,
                                                Coordinate(x=(coord.x // projection.face_size) * projection.face_size,
                                                           y=(coord.y // projection.face_size) * projection.face_size),
                                                projection.face_size)
        actual_projection = self.projections[wouldbe_face.identity]
        coord, direct = actual_projection.translate(wouldbe_projection, coord, direct)
        return actual_projection.face, coord, direct

    def walk_direction(self, face: CubeFace, coord: Coordinate, direct: Direction, steps_count: int) -> Iterator[CubeFace, Coordinate, Direction]:
        """Walk in given direction from a given coordinate on a given face."""
        cur_face, cur_coord, cur_direct = face, coord, direct

        step = 0
        while step < steps_count:
            next_coord = cur_coord.translate(*cur_direct.value)
            cur_face, cur_coord, cur_direct = self.wrap_coordinate(cur_face, next_coord, cur_direct)

            if self.layout[cur_coord] == '#':
                break

            yield cur_face, cur_coord, cur_direct
            step += 1

    def walk(self) -> Iterator[Coordinate, Direction]:
        cur_face = CubeFace.A_0
        cur_coord, cur_direct = self.projections[cur_face].min_coord, Direction.RIGHT
        yield cur_coord, cur_direct

        for p in self.path:
            match p:
                case int(steps_count):
                    for cur_face, cur_coord, cur_direct in self.walk_direction(cur_face, cur_coord, cur_direct, steps_count):
                        yield cur_coord, cur_direct
                case 'R':
                    cur_direct = cur_direct @ Rotation.Z_270
                    yield cur_coord, cur_direct
                case 'L':
                    cur_direct = cur_direct @ Rotation.Z_90
                    yield cur_coord, cur_direct
                case _:
                    raise RuntimeError

        yield cur_coord, cur_direct

    def visualize(self, footprints: list[tuple[Coordinate, Direction]] = None, cur_coord: Coordinate = None):
        layout: np.array = self.layout.copy()

        if footprints:
            for c, d in footprints:
                match d:
                    case Direction.UP:
                        layout[c] = '^'
                    case Direction.DOWN:
                        layout[c] = 'v'
                    case Direction.LEFT:
                        layout[c] = '<'
                    case Direction.RIGHT:
                        layout[c] = '>'
                    case _:
                        raise RuntimeError

        if cur_coord is not None:
            layout[cur_coord] = '@'

        return '\n'.join(''.join(line) for line in layout)


cave_map = CaveMap(example_input)

footprints: list[tuple[Coordinate, Direction]] = []
for c, d in cave_map.walk():
    footprints.append((c, d))

print(cave_map.visualize(footprints, c), end='\n')

final_c, final_d = footprints[-1]
password = (final_c.y + 1) * 1000 + (final_c.x + 1) * 4
match final_d:
    case Direction.UP:
        password += 3
    case Direction.LEFT:
        password += 2
    case Direction.DOWN:
        password += 1
    case Direction.RIGHT:
        password += 0

print(password)