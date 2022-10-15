from dataclasses import dataclass

@dataclass
class Wall:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
