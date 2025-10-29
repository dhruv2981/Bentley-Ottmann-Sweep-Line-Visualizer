## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## sweep_line.py - Sweep line algorithm implementation

from typing import List, Optional, Tuple
from geometry import segment_intersection, y_at, EPS
from segment import Segment, Event

class SweepLine:
    def __init__(self, segments: List[Segment], log_fn=print):
        self.segments = segments
        self.status_order: List[int] = []
        self.intersections: List[Tuple[float, float]] = []
        self.sweep_x = 0.0
        self.log = log_fn

    def insert_status(self, seg_id: int, x: float):
        seg = self.segments[seg_id]
        yv = y_at((seg.a, seg.b), x + EPS) 
        pos = 0
        while pos < len(self.status_order):
            s2 = self.segments[self.status_order[pos]]
            y2 = y_at((s2.a, s2.b), x + EPS)
            if y2 > yv: break
            pos += 1
        self.status_order.insert(pos, seg_id)
        self.log(f"Inserted S{seg_id} at pos {pos}. Status: {self.status_order}")
        return pos

    def remove_status(self, seg_id: int):
        if seg_id not in self.status_order: 
            self.log(f"Warning: S{seg_id} not in status for removal.")
            return (None, None)
        pos = self.status_order.index(seg_id)
        left = self.status_order[pos-1] if pos-1 >= 0 else None
        right = self.status_order[pos+1] if pos+1 < len(self.status_order) else None
        self.status_order.pop(pos)
        self.log(f"Removed S{seg_id}. Status: {self.status_order}")
        return (left, right)

    def swap(self, s1: int, s2: int):
        try:
            i1, i2 = self.status_order.index(s1), self.status_order.index(s2)
        except ValueError:
            self.log(f"Warning: Tried to swap S{s1}, S{s2} but one not in status.")
            return
        # Ensure i1 is always the lower index
        if i1 > i2:
            i1, i2 = i2, i1
            s1, s2 = s2, s1
            
        self.status_order[i1], self.status_order[i2] = self.status_order[i2], self.status_order[i1]
        self.log(f"Swapped S{s1} and S{s2}. Status: {self.status_order}")


    def process_event(self, ev: Event) -> List[Event]:
        self.sweep_x = ev.x
        new_events: List[Event] = []
        
        if ev.type == 'L':
            new_events = self._process_left(ev)
        elif ev.type == 'R':
            new_events = self._process_right(ev)
        elif ev.type == 'I':
            new_events = self._process_intersection(ev)

        return [e for e in new_events if e.x > self.sweep_x + EPS]

    def _add_intersection(self, x: float, y: float) -> bool:
        for (x0, y0) in self.intersections:
            if abs(x-x0) < EPS and abs(y-y0) < EPS:
                return False
        self.intersections.append((x,y))
        return True

    def _process_left(self, ev: Event) -> List[Event]:
        sid = ev.seg_ids[0]
        pos = self.insert_status(sid, ev.x)
        left = self.status_order[pos-1] if pos > 0 else None
        right = self.status_order[pos+1] if pos+1 < len(self.status_order) else None
        
        new_events: List[Event] = []
        for nb_id in (left, right):
            if nb_id is None: continue
            
            r = segment_intersection(self.segments[sid].a, self.segments[sid].b,
                                     self.segments[nb_id].a, self.segments[nb_id].b)
            if r: 
                x, y = r
                self.log(f"Found new intersection: S{sid} and S{nb_id}")
                new_events.append(Event(x, y, 'I', (sid, nb_id)))
        return new_events

    def _process_right(self, ev: Event) -> List[Event]:
        sid = ev.seg_ids[0]
        left, right = self.remove_status(sid)
        
        new_events: List[Event] = []
        if left is not None and right is not None:
            r = segment_intersection(self.segments[left].a, self.segments[left].b,
                                     self.segments[right].a, self.segments[right].b)
            if r:
                x, y = r
                self.log(f"Found new intersection: S{left} and S{right}")
                new_events.append(Event(x, y, 'I', (left, right)))
        return new_events

    def _process_intersection(self, ev: Event) -> List[Event]:
        s1, s2 = ev.seg_ids
        if s1 is None or s2 is None: return []

        if self._add_intersection(ev.x, ev.y):
             self.log(f"INTERSECTION at ({ev.x:.2f}, {ev.y:.2f}) between S{s1} and S{s2}")

        try:
            i1 = self.status_order.index(s1)
            i2 = self.status_order.index(s2)
        except ValueError:
            self.log(f"Warning: S{s1} or S{s2} not in status for intersection.")
            return []
        if i1 < i2:
            i1, i2 = i2, i1
            s1, s2 = s2, s1
        self.swap(s1, s2)
        
        s1_below = self.status_order[i2 - 1] if i2 > 0 else None
        s2_above = self.status_order[i1 + 1] if i1 + 1 < len(self.status_order) else None

        new_events: List[Event] = []
        
        if s1_below is not None:
            r = segment_intersection(self.segments[s1].a, self.segments[s1].b,
                                     self.segments[s1_below].a, self.segments[s1_below].b)
            if r: 
                self.log(f"Found new intersection: S{s1} and S{s1_below}")
                new_events.append(Event(r[0], r[1], 'I', (s1_below, s1)))

        if s2_above is not None:
            r = segment_intersection(self.segments[s2].a, self.segments[s2].b,
                                     self.segments[s2_above].a, self.segments[s2_above].b)
            if r:
                self.log(f"Found new intersection: S{s2} and S{s2_above}")
                new_events.append(Event(r[0], r[1], 'I', (s2, s2_above)))
            
        return new_events
    