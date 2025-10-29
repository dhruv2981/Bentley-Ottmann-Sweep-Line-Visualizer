## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 29, 2025
## polygon_checker.py - Polygon self-intersection detection logic

from typing import List, Optional, Tuple
from bisect import insort

from geometry import Point, segment_intersection, EPS
from segment import Segment, Event
from sweep_line import SweepLine

class PolygonSweep(SweepLine):
    """
    Extends SweepLine to detect ALL self-intersections in a polygon.
    
    It ignores intersections between adjacent polygon edges.
    """
    def __init__(self, segments: List[Segment], log_fn=print):
        super().__init__(segments, log_fn)
        self.n = len(segments)
        self.non_adjacent_intersections: List[Point] = []

    def _are_adjacent(self, s1_id: int, s2_id: int) -> bool:
        """Checks if two segment IDs correspond to adjacent polygon edges."""
        diff = abs(s1_id - s2_id)
        return diff == 1 or diff == (self.n - 1)

    def _process_intersection(self, ev: Event) -> List[Event]:
        """
        Overrides the base method to check for non-adjacent intersections.
        """
        s1, s2 = ev.seg_ids
        if s1 is None or s2 is None: 
            return []

        if not self._are_adjacent(s1, s2):
            is_new = self._add_intersection(ev.x, ev.y)
            if is_new:
                self.log(f"FOUND SELF-INTERSECTION at ({ev.x:.2f}) between S{s1} and S{s2}")
                self.non_adjacent_intersections.append((ev.x, ev.y))

        # The rest of this method is identical to the base class,
        # required to perform the swap and find new neighbor intersections.
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

def check_polygon(vertices: List[Point], log_fn=print) -> List[Point]:
    """
    Runs the full sweep-line algorithm to find ALL self-intersections.
    
    Returns a list of all non-adjacent intersection points found.
    """
    if len(vertices) < 3:
        return []
        
    segments: List[Segment] = []
    event_queue: List[Event] = []
    n = len(vertices)
    
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        
        left_pt, right_pt = (p1, p2) if p1[0] < p2[0] else (p2, p1)
        
        seg = Segment(id=i, a=p1, b=p2, color="#000000") 
        segments.append(seg)
        
        event_queue.append(Event(left_pt[0], left_pt[1], 'L', (seg.id, None)))
        event_queue.append(Event(right_pt[0], right_pt[1], 'R', (seg.id, None)))

    event_queue.sort()
    
    sweep = PolygonSweep(segments, log_fn=log_fn)

    while event_queue:
        ev = event_queue.pop(0)
        new_events = sweep.process_event(ev)
        
        if new_events:
            for new_ev in new_events:
                if new_ev.x < sweep.sweep_x - EPS:
                    continue
                    
                is_duplicate = False
                for existing_ev in event_queue:
                    if existing_ev.type == 'I' and \
                       abs(existing_ev.x - new_ev.x) < EPS and \
                       abs(existing_ev.y - new_ev.y) < EPS and \
                       set(existing_ev.seg_ids) == set(new_ev.seg_ids):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    log_fn(f"SCHEDULING new: {new_ev.type} at ({new_ev.x:.2f}, {new_ev.y:.2f})")
                    insort(event_queue, new_ev)

    return sweep.non_adjacent_intersections
