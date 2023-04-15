from collections import Counter
from math import floor
from typing import List, Union

from PyQt5.QtCore import QPoint


# TODO два клика в 1 точку

def fill_polygon(polygon: List[QPoint]):
    max_point = max(polygon, key=lambda point: point.x())

    # print(max_point)

    edges = []
    for i in range(1, len(polygon)):
        edges.append([polygon[i - 1], polygon[i]])

    all_points = []
    for edge in edges:
        points_for_edge = []
        if edge[0].y() > edge[1].y():
            edge[0], edge[1] = edge[1], edge[0]

        y = edge[0].y() + 1 / 2

        while y < edge[1].y():
            x = get_intersection_point(edge[0], edge[1], y)

            if floor(x) + 1 / 2 > x:
                points_for_edge.append([floor(x), floor(y)])
            x = floor(x)
            x += 1

            while x <= max_point.x():
                points_for_edge.append([x, floor(y)])
                x += 1

            y += 1

        all_points.extend(points_for_edge)

    return all_points


def get_intersection_point(start_point: QPoint, end_point: QPoint, y):
    return (y - start_point.y()) * (end_point.x() - start_point.x()) / (
            end_point.y() - start_point.y()) + start_point.x()


def f(l):
    res = []
    for item in l:
        if item in res:
            print(item)
        else:
            res.append(item)


def sign(x: float) -> int:
    ret = 0
    if x > 0:
        ret = 1
    elif x < 0:
        ret = -1
    return ret


def brezenhem_int(start_point: QPoint, end_point: QPoint, is_step: bool = False) -> Union[list, int]:
    pointed_list = []
    steps = 0

    if start_point == end_point:
        pointed_list.append(start_point)
    else:
        dx = end_point.x() - start_point.x()
        dy = end_point.y() - start_point.y()

        sign_x = sign(dx)
        sign_y = sign(dy)

        dx = abs(dx)
        dy = abs(dy)

        is_swap = 0

        if dy > dx:
            dy, dx = dx, dy
            is_swap = 1

        error = 2 * dy - dx

        x0 = start_point.x()
        y0 = start_point.y()

        old_x = x0
        old_y = y0

        for i in range(0, int(dx) + 1):
            pointed_list.append([x0, y0])

            if error >= 0:
                if is_swap:
                    x0 += sign_x
                else:
                    y0 += sign_y
                error -= 2 * dx

            if error <= 0:
                if is_swap:
                    y0 += sign_y
                else:
                    x0 += sign_x
                error += 2 * dy

            if is_step and old_x != x0 and old_y != y0:
                steps += 1
            old_x = x0
            old_y = y0

    if is_step:
        return steps

    return pointed_list
