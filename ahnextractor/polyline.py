from typing import List, Tuple
from pydantic import BaseModel

class Polyline(BaseModel):    
    """
    Object to hold points through which a line runs.

    The points are held in a list (self.points_list), where the points are defined as tuples of (x, y) coordinates.
    E.g.:
    print(self.points_list) >> [(0, 1), (1, 1), (2, 2)]
    """
    points: List[Tuple[float, float]] = []

    @classmethod
    def from_points(cls, *args) -> 'Polyline':
        return cls(points = [a for a in args])

    