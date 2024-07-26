from typing import Callable
from pyee import EventEmitter
from enum import Enum, auto


class Sign(Enum):
    WALL = auto()
    SNACK_HEAD = auto()
    SNACK_BODY = auto()
    POINT = auto()


class SnakeGame:
    def __init__(self, snack_length=4, width=32, height=32):
        self.__emitter = EventEmitter()
        self.__event_update = "update"
        self.__width = width
        self.__height = height
        self.__snack_length = snack_length
        self.__current_snack_length = snack_length

    def width(self):
        return self.__width
    
    def height(self):
        return self.__height
    
    def register_update(self, listener: Callable[[int, int, Sign], None]):
        self.__emitter.on(self.__event_update, listener)

    def start(self):
        self.__current_snack_length = self.__snack_length

        for row in [0, self.__height - 1]:
            for column in range(self.__width):
                self.__emitter.emit(self.__event_update, column, row, Sign.WALL)

        for row in range(1, self.__height - 1):
            self.__emitter.emit(self.__event_update, 0, row, Sign.WALL)
            self.__emitter.emit(self.__event_update, self.__width - 1, row, Sign.WALL)

        for i in range(self.__snack_length - 1):
            self.__emitter.emit(self.__event_update, 3 + i, self.__height - 4, Sign.SNACK_BODY)

        self.__emitter.emit(self.__event_update, 3 + self.__snack_length - 1, self.__height - 4, Sign.SNACK_HEAD)
        
        
