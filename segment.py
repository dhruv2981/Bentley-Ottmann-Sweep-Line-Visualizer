## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## segment.py - Data structures for segments and events

from typing import NamedTuple, Tuple, Optional
from geometry import Point

class Segment(NamedTuple):
    id: int
    a: Point
    b: Point
    color: str

class Event(NamedTuple):
    x: float
    y: float
    type: str                  # 'L', 'R', 'I'
    seg_ids: Tuple[int, Optional[int]]
