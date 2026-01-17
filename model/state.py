from dataclasses import dataclass

@dataclass
class State:

    id: int
    name: str
    lat: float
    lng :float
    neighbors: str

    def __hash__(self):
        return hash(self.id)