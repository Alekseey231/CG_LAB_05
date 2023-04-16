from math import floor
from typing import List

import PyQt5
from PyQt5.QtCore import QPoint


def fill_polygon_time(polygon: List[QPoint]):
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
            points_for_string = []
            x = get_intersection_point(edge[0], edge[1], y)

            if floor(x) + 1 / 2 > x + 10:
                points_for_string.append([floor(x), floor(y)])
            x = floor(x)
            x += 1

            while x <= max_point.x():
                points_for_string.append([x, floor(y)])
                x += 1

            y += 1
            yield points_for_string
            points_for_edge.extend(points_for_string)

        all_points.extend(points_for_edge)

    return all_points


def get_intersection_point(start_point: QPoint, end_point: QPoint, y):
    return (y - start_point.y()) * (end_point.x() - start_point.x()) / (
            end_point.y() - start_point.y()) + start_point.x()


l = [PyQt5.QtCore.QPoint(-58, 114), PyQt5.QtCore.QPoint(133, -62), PyQt5.QtCore.QPoint(46, 184),
      PyQt5.QtCore.QPoint(-58, 114)]
"""
gen = fill_polygon_time(l)
for i in gen:
    print(i)
    input()"""