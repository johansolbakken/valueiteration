class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()


class Spec:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.blocks: list[Position] = []
        self.values: dict[Position, float] = {}

    def __str__(self):
        return f"Spec(width={self.width}, height={self.height}, blocks={self.blocks}, values={self.values})"

    def __repr__(self):
        return self.__str__()

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def add_block(self, x, y):
        self.blocks.append(Position(x, y))

    def add_value(self, x, y, value):
        self.values[Position(x, y)] = value
