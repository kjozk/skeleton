import math
from typing import List, Tuple

Point = Tuple[float, float]
Segment = Tuple[Point, Point]


def cross(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])


def mul(a: Point, s: float) -> Point:
    return (a[0] * s, a[1] * s)


def norm(a: Point) -> float:
    return math.hypot(a[0], a[1])


def normalize(a: Point) -> Point:
    n = norm(a)
    if n == 0:
        return (0.0, 0.0)
    return (a[0] / n, a[1] / n)


def is_ccw(polygon: List[Point]) -> bool:
    area = 0.0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        area += (x2 - x1) * (y2 + y1)
    return area < 0


def concave_vertices(polygon: List[Point]) -> List[int]:
    """凹頂点のインデックスを返す（CCW前提）"""
    indices = []
    n = len(polygon)
    for i in range(n):
        p0 = polygon[(i - 1) % n]
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        v1 = sub(p1, p0)
        v2 = sub(p2, p1)
        if cross(v1, v2) < 0:
            indices.append(i)
    return indices


def bounding_box_center_line(polygon: List[Point]) -> Segment:
    """凸形状向け：bbox長辺方向の中心線"""
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2

    if width >= height:
        return ((min_x, cy), (max_x, cy))
    else:
        return ((cx, min_y), (cx, max_y))


def concave_skeleton(polygon: List[Point]) -> List[Segment]:
    """凹形状向け：凹頂点の内角二等分線"""
    result = []
    n = len(polygon)

    for i in concave_vertices(polygon):
        p_prev = polygon[(i - 1) % n]
        p = polygon[i]
        p_next = polygon[(i + 1) % n]

        e1 = normalize(sub(p_prev, p))
        e2 = normalize(sub(p_next, p))

        d = normalize(add(e1, e2))
        if norm(d) == 0:
            continue

        # 仮にポリゴンの中心まで延ばす（設備用近似）
        cx = sum(pt[0] for pt in polygon) / n
        cy = sum(pt[1] for pt in polygon) / n
        center = (cx, cy)

        result.append((p, center))

    return result


def generate_skeleton(polygon: List[Point]) -> List[Segment]:
    if not is_ccw(polygon):
        polygon = list(reversed(polygon))

    concave = concave_vertices(polygon)

    if not concave:
        # 凸
        return [bounding_box_center_line(polygon)]
    else:
        # 凹
        return concave_skeleton(polygon)
