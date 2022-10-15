from dataclasses import dataclass


@dataclass
class Item:
    type: str
    x: int
    y: int

    def __eq__(self, __o: object):
        return isinstance(__o, Item) and all([
            self.x == __o.x,
            self.y == __o.y,
            self.type == __o.type
        ])

    def __hash__(self):
        return hash((self.type, self.x, self.y))
