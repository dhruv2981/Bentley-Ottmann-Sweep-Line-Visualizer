## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## sweep_line.py - Sweep line algorithm implementation

from typing import List, Optional, Tuple
from geometry import segment_intersection, y_at, EPS
from segment import Segment, Event

class SweepLine:
    def __init__(self, segments: List[Segment], log_fn=print):
        self.segments = segments
        self.events: List[Event] = []
        self.status_order: List[int] = []
        self.intersections: List[Tuple[float, float]] = []
        self.sweep_x = 0.0
        self.log = log_fn

    def insert_status(self, seg_id: int, x: float):
        seg = self.segments[seg_id]
        yv = y_at((seg.a, seg.b), x + 1e-6)
        pos = 0
        while pos < len(self.status_order):
            s2 = self.segments[self.status_order[pos]]
            y2 = y_at((s2.a, s2.b), x + 1e-6)
            if y2 > yv: break
            pos += 1
        self.status_order.insert(pos, seg_id)
        self.log(f"Inserted S{seg_id} at position {pos}")
        return pos

    def remove_status(self, seg_id: int):
        if seg_id not in self.status_order: return (None, None)
        pos = self.status_order.index(seg_id)
        left = self.status_order[pos-1] if pos-1 >= 0 else None
        right = self.status_order[pos+1] if pos+1 < len(self.status_order) else None
        self.status_order.pop(pos)
        self.log(f"Removed S{seg_id} from status")
        return (left, right)

    def swap(self, s1: int, s2: int):
        try:
            i1, i2 = self.status_order.index(s1), self.status_order.index(s2)
        except ValueError:
            return
        self.status_order[i1], self.status_order[i2] = self.status_order[i2], self.status_order[i1]
        self.log(f"Swapped S{s1} and S{s2}")

    def process_event(self, ev: Event):
        self.sweep_x = ev.x
        if ev.type == 'L':
            self._process_left(ev)
        elif ev.type == 'R':
            self._process_right(ev)
        elif ev.type == 'I':
            self._process_intersection(ev)

    def _add_intersection(self, a: int, b: int, x: float, y: float):
        if any(abs(x-x0) < 1e-6 and abs(y-y0) < 1e-6 for (x0,y0) in self.intersections):
            return
        self.intersections.append((x,y))
        self.log(f"Intersection between S{a} and S{b} at ({x:.2f}, {y:.2f})")

    def _process_left(self, ev: Event):
        sid = ev.seg_ids[0]
        pos = self.insert_status(sid, ev.x)
        left = self.status_order[pos-1] if pos > 0 else None
        right = self.status_order[pos+1] if pos+1 < len(self.status_order) else None
        for nb in (left, right):
            if nb is None: continue
            r = segment_intersection(self.segments[sid].a, self.segments[sid].b,
                                     self.segments[nb].a, self.segments[nb].b)
            if r: x,y = r; self._add_intersection(sid, nb, x, y)

    def _process_right(self, ev: Event):
        sid = ev.seg_ids[0]
        left, right = self.remove_status(sid)
        if left is not None and right is not None:
            r = segment_intersection(self.segments[left].a, self.segments[left].b,
                                     self.segments[right].a, self.segments[right].b)
            if r: x,y = r; self._add_intersection(left, right, x, y)

    def _process_intersection(self, ev: Event):
        s1, s2 = ev.seg_ids
        if s1 is None or s2 is None: return
        x,y = ev.x, ev.y
        self._add_intersection(s1, s2, x, y)
        self.swap(s1, s2)
