from __future__ import annotations


class Vec2:
    """ Represents vector of two integers """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def xyiter(self, other: Vec2):

        smaller_x = min(self.x, other.x)
        smaller_y = min(self.y, other.y)
        x_space = abs(self.x - other.x) + smaller_x
        y_space = abs(self.y - other.y) + smaller_y

        for x in range(smaller_x, x_space):
            for y in range(smaller_y, y_space):
                yield (x, y)
    
    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    @classmethod
    def new(cls, fill: int = 0) -> Vec2:
        return cls(fill, fill)
    
    def __repr__(self) -> str:
        return f'{__name__}.{__class__.__name__}(x={self.x}, y={self.y})'

    def __mul__(self, other: Vec2) -> Vec2:
        return Vec2(self.x * other.x, self.y * other.y)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __truediv__(self, other: Vec2) -> Vec2:
        return Vec2(self.x // other.x, self.y // other.y)

    __div__ = __truediv__

    def __imul__(self, other: Vec2) -> Vec2:
        self.x *= other.x
        self.y *= other.y
        return self

    def __iadd__(self, other: Vec2) -> Vec2:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: Vec2) -> Vec2:
        self.x -= other.x
        self.y -= other.y
        return self

    def __itruediv__(self, other: Vec2) -> Vec2:
        self.x //= other.x
        self.y //= other.y
        return self

    __idiv__ = __itruediv__ 

    def __abs__(self) -> Vec2:
        return Vec2(abs(self.x), abs(self.y))

    def __eq__(self, other: Vec2) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Vec2) -> bool:
        return self.x != other.x or self.y != other.y