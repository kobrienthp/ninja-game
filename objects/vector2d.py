from typing import List, Tuple


class Vector2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector2D(x=self.x + v.x, y=self.y + v.y)

    def __sub__(self, v):
        return Vector2D(x=self.x - v.x, y=self.y - v.y)

    def __mul__(self, v):
        if isinstance(v, Vector2D):
            return Vector2D(x=self.x * v.x, y=self.y * v.y)
        elif isinstance(v, (int, float)):
            return Vector2D(x=self.x * v, y=self.y * v)

    def __IADD__(self, v):
        return self + v

    def __ISUB__(self, v):
        return self - v

    def __mod__(self, v):
        return Vector2D(x=self.x % v.x, y=self.y % v.y)

    def to_list(self) -> List:
        return [self.x, self.y]

    def to_tuple(self) -> Tuple:
        return (self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    @classmethod
    def from_list(cls, v: list):
        return Vector2D(x=v[0], y=v[1])

    @classmethod
    def from_tuple(cls, v: tuple):
        return Vector2D(x=v[0], y=v[1])
