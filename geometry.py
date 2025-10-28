## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## geometry.py - Geometry utility functions
 
from typing import Tuple, Optional

Point = Tuple[float, float]
EPS = 1e-9

def orient(a: Point, b: Point, c: Point) -> float:
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def on_segment(a: Point, b: Point, c: Point) -> bool:
    return min(a[0], c[0]) - EPS <= b[0] <= max(a[0], c[0]) + EPS and \
           min(a[1], c[1]) - EPS <= b[1] <= max(a[1], c[1]) + EPS

def segment_intersection(p1: Point, q1: Point, p2: Point, q2: Point) -> Optional[Point]:
    o1, o2 = orient(p1, q1, p2), orient(p1, q1, q2)
    o3, o4 = orient(p2, q2, p1), orient(p2, q2, q1)

    # general case
    if o1*o2 < -EPS and o3*o4 < -EPS:
        A1, B1, C1 = q1[1]-p1[1], p1[0]-q1[0], (q1[1]-p1[1])*p1[0] + (p1[0]-q1[0])*p1[1]
        A2, B2, C2 = q2[1]-p2[1], p2[0]-q2[0], (q2[1]-p2[1])*p2[0] + (p2[0]-q2[0])*p2[1]
        det = A1*B2 - A2*B1
        if abs(det) < EPS:
            return None
        x = (B2*C1 - B1*C2)/det
        y = (A1*C2 - A2*C1)/det
        return (x, y)

    # collinear cases
    if abs(o1) < EPS and on_segment(p1, p2, q1): return p2
    if abs(o2) < EPS and on_segment(p1, q2, q1): return q2
    if abs(o3) < EPS and on_segment(p2, p1, q2): return p1
    if abs(o4) < EPS and on_segment(p2, q1, q2): return q1
    return None

def y_at(seg: Tuple[Point, Point], x: float) -> float:
    (a, b) = seg
    if abs(a[0]-b[0]) < EPS:
        return min(a[1], b[1])
    t = (x - a[0]) / (b[0]-a[0])
    return a[1] + t*(b[1]-a[1])
