from __future__ import annotations


class Vec2:
    """ Represents vector of two integers """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    @classmethod
    def new(cls, fill: int = 0) -> Vec2:
        return cls(fill, fill)

    def __repr__(self) -> str:
        return f'{__name__}.{__class__.__name__}(x={self.x}, y={self.y})'

    def __mul__(self, other: int) -> Vec2:
        if isinstance(other, Vec2):
            return NotImplemented
        return Vec2(self.x * other, self.y * other)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other: int) -> Vec2:
        if isinstance(other, Vec2):
            return NotImplemented
        return Vec2(self.x // other, self.y // other)

    __truediv__ = __floordiv__

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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Vec2):
            return self.x != other.x or self.y != other.y
        return NotImplemented

