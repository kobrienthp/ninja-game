from typing import Tuple


class Vector:
    def __init__(self, *coordinates) -> None:
        self.coordinates = list(coordinates)

    @property
    def dimension(self) -> int:
        return len(self.coordinates)

    def round(self):
        return type(self)(*[int(coord) for coord in self.coordinates])

    def __add__(self, v):
        assert v.dimension == self.dimension, "vectors must be of the same dimension"
        return type(self)(*[u_i + v_i for u_i, v_i in zip(self.coordinates, v.coordinates)])

    def __sub__(self, v):
        assert v.dimension == self.dimension, "vectors must be of the same dimension"
        return type(self)(*[u_i - v_i for u_i, v_i in zip(self.coordinates, v.coordinates)])

    def __mul__(self, v):
        if isinstance(v, type(self)):
            assert v.dimension == self.dimension, "vectors must be of the same dimension"
            return type(self)(*[u_i * v_i for u_i, v_i in zip(self.coordinates, v.coordinates)])
        elif isinstance(v, (int, float)):
            return type(self)(*[u_i * v for u_i in self.coordinates])

    def __truediv__(self, scalar):
        return type(self)(*[u_i / scalar for u_i in self.coordinates])

    def __IADD__(self, v):
        return self + v

    def __ISUB__(self, v):
        return self - v

    def __mod__(self, v):
        if isinstance(v, type(self)):
            assert v.dimension == self.dimension, "vectors must be of the same dimension"
            return type(self)(*[u_i % v_i for u_i, v_i in zip(self.coordinates, v.coordinates)])
        elif isinstance(v, (int, float)):
            return type(self)(*[u_i % v for u_i in self.coordinates])

    def __floordiv__(self, v):
        if isinstance(v, type(self)):
            assert v.dimension == self.dimension, "vectors must be of the same dimension"
            return type(self)(*[u_i // v_i for u_i, v_i in zip(self.coordinates, v.coordinates)])
        elif isinstance(v, (int, float)):
            return type(self)(*[u_i // v for u_i in self.coordinates])

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __hash__(self) -> int:
        return hash(self.to_tuple)

    def __str__(self) -> str:
        return str(self.to_tuple())

    def __repr__(self) -> str:
        return str(self.to_tuple())

    def to_tuple(self) -> Tuple:
        return tuple(self.coordinates)

    def __iter__(self):
        return iter(self.coordinates)


class Vector2D(Vector):
    def __init__(self, *coordinates) -> None:
        assert len(coordinates) == 2, ValueError("must specify exactly two coordinates")
        super().__init__(*coordinates)

    @property
    def x(self) -> float:
        return self.coordinates[0]

    @x.setter
    def x(self, value):
        self.coordinates[0] = value

    @property
    def y(self) -> float:
        return self.coordinates[1]

    @y.setter
    def y(self, value):
        self.coordinates[1] = value
