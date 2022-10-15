from dataclasses import dataclass


@dataclass
class FloorTile:

    x: int
    y: int
    _visited: bool


    def __hash__(self) -> int:
        return hash((self.x, self.y))


    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, v):
        self._visited = v