from typing import Callable, Tuple, List
from pyee import EventEmitter
from enum import Enum, auto
from random import randint


class Sign(Enum):
    NONE = auto()
    WALL = auto()
    SNACK_HEAD = auto()
    SNACK_BODY = auto()
    POINT = auto()


class Direction(Enum):
    LEFT = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()


class SnakeGame:
    @staticmethod
    def __calc_pos(pos: Tuple[int, int], dir: Direction) -> Tuple[int, int]:
        x = pos[0]
        y = pos[1]
        if (dir == Direction.LEFT):
            return (x - 1, y)
        elif (dir == Direction.UP):
            return (x, y - 1)
        elif (dir == Direction.RIGHT):
            return (x + 1, y)
        else:
            return (x, y + 1)

    @staticmethod
    def __reverse_dir(dir: Direction) -> Direction:
        if (dir == Direction.LEFT):
            return Direction.RIGHT
        elif (dir == Direction.UP):
            return Direction.DOWN
        elif (dir == Direction.RIGHT):
            return Direction.LEFT
        else:
            return Direction.UP

    def __init__(self, cell_size=20, snack_length=4, width=32, height=32, num_of_points=3):
        self.__cell_size = cell_size
        self.__snack_length = snack_length
        self.__width = width
        self.__height = height
        self.__num_of_points = num_of_points

        self.__is_start = False
        self.__is_end = False
        self.__enable_send_dir = False
        self.__emitter = EventEmitter()
        self.__event_update = "update"
        self.__event_end = "end"
        self.__next_dir = Direction.RIGHT

    def __raise_update(self, pos: Tuple[int, int], sign: Sign) -> None:
        self.__emitter.emit(self.__event_update, pos[0], pos[1], sign)

    def __raise_end(self) -> None:
        self.__is_end = True
        self.__emitter.emit(self.__event_end)

    def register_update(self, listener: Callable[[int, int, Sign], None]):
        self.__emitter.on(self.__event_update, listener)

    def register_end(self, listener: Callable[[], None]):
        self.__emitter.on(self.__event_end, listener)

    def cell_size(self) -> int:
        return self.__cell_size

    def width(self) -> int:
        return self.__width

    def height(self) -> int:
        return self.__height

    def is_start(self) -> bool:
        return self.__is_start

    def is_end(self) -> bool:
        return self.__is_end

    def __get_walls(self) -> set[Tuple[int, int]]:
        result = set()
        for row in [0, self.__height - 1]:
            for column in range(self.__width):
                result.add((column, row))

        for row in range(1, self.__height - 1):
            result.add((0, row))
            result.add((self.__width - 1, row))
        return result

    def __get_bodys(self) -> List[Tuple[int, int]]:
        list = []
        pos = self.__current_pos
        for dir in self.__current_body:
            pos = SnakeGame.__calc_pos(pos, dir)
            list.append(pos)
        return list

    def __create_wall(self):
        for pos in self.__current_walls:
            self.__raise_update(pos, Sign.WALL)

    def __create_snack(self):
        pos = self.__current_pos
        self.__raise_update(pos, Sign.SNACK_HEAD)
        for pos in self.__get_bodys():
            self.__raise_update(pos, Sign.SNACK_BODY)

    def __create_point(self):
        remain = set()
        for x in range(self.__width):
            for y in range(self.__height):
                remain.add((x, y))

        remain = remain - {self.__current_pos} - set(self.__get_bodys()) - \
            self.__current_walls - self.__current_points

        index = randint(0, len(remain) - 1)
        pos = list(remain)[index]
        self.__current_points.add(pos)
        self.__raise_update(pos, Sign.POINT)

    def __move_snack(self, dir: Direction):
        newPos = SnakeGame.__calc_pos(self.__current_pos, dir)
        self.__raise_update(newPos, Sign.SNACK_HEAD)
        self.__raise_update(self.__current_pos, Sign.SNACK_BODY)
        self.__current_body.insert(0, SnakeGame.__reverse_dir(dir))
        self.__current_pos = newPos

    def __pop_snack(self):
        body = self.__get_bodys()
        self.__raise_update(body[len(body) - 1], Sign.NONE)
        self.__current_body.pop()

    def start(self):
        self.__current_pos = (self.__snack_length + 2, self.__height - 4)
        self.__current_body = []
        self.__current_points = set()
        self.__current_dir = Direction.RIGHT
        self.__current_walls = self.__get_walls()
        self.__next_dir = Direction.RIGHT
        for _ in range(self.__snack_length - 1):
            self.__current_body.append(Direction.LEFT)

        self.__create_wall()
        self.__create_snack()
        for _ in range(self.__num_of_points):
            self.__create_point()

        self.__enable_send_dir = True
        self.__is_end = False
        self.__is_start = True

    def next(self):
        if (not self.__is_start or self.__is_end):
            return
        self.__move_snack(self.__next_dir)
        self.__current_dir = self.__next_dir
        if (self.__current_pos in self.__current_points):
            self.__current_points.remove(self.__current_pos)
            self.__create_point()
        elif (self.__current_pos in self.__current_walls
              or self.__current_pos in self.__get_bodys()):
            self.__raise_end()
        else:
            self.__pop_snack()

    def send_dir(self, dir: Direction) -> bool:
        if (not self.__is_start or self.__is_end or not self.__enable_send_dir):
            return False
        if (dir == SnakeGame.__reverse_dir(self.__current_dir)):
            return False
        self.__next_dir = dir
        return True
