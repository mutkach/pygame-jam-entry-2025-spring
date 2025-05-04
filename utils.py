from typing import Iterable, Iterator


class Linspace(Iterator):
    def __init__(self, lbound, rbound, steps):
        self.pos = lbound
        self.rbound = rbound
        self.lbound = lbound
        self.step = (rbound-lbound)/steps
        
    def __iter__(self):
        return self

    def __next__(self):
        self.pos += self.step
        if self.pos > self.rbound:
            raise StopIteration
        return self.pos
            

def on_segment(p, q, r):
    """Check if point q lies on segment pr"""
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and \
       min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True
    return False

def orientation(p, q, r):
    """Return orientation of ordered triplet (p, q, r):
    0 -> collinear, 1 -> clockwise, 2 -> counterclockwise"""
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def segments_intersect(x1, y1, x2, y2):
    """Check if segments (x1,y1) and (x2,y2) intersect"""
    o1 = orientation(x1, y1, x2)
    o2 = orientation(x1, y1, y2)
    o3 = orientation(x2, y2, x1)
    o4 = orientation(x2, y2, y1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Sxecial cases
    if o1 == 0 and on_segment(x1, x2, y1): return True
    if o2 == 0 and on_segment(x1, y2, y1): return True
    if o3 == 0 and on_segment(x2, x1, y2): return True
    if o4 == 0 and on_segment(x2, y1, y2): return True

    return False

def intersection_point(p1, q1, p2, q2):
    """Return intersection point if it exists, else None"""
    if not segments_intersect(p1, q1, p2, q2):
        return None

    # Convert points to line equations: A1x + B1y = C1
    A1 = q1[1] - p1[1]
    B1 = p1[0] - q1[0]
    C1 = A1 * p1[0] + B1 * p1[1]

    A2 = q2[1] - p2[1]
    B2 = p2[0] - q2[0]
    C2 = A2 * p2[0] + B2 * p2[1]

    det = A1 * B2 - A2 * B1
    if det == 0:
        # Lines are parallel (could be collinear)
        return None

    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det

    if on_segment(p1, (x, y), q1) and on_segment(p2, (x, y), q2):
        return (x, y)
    return None
