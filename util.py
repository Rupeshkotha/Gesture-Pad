import numpy as np


def get_angle(point1, point2, point3):
    radians = np.arctan2(point3[1] - point2[1], point3[0] - point2[0]) - np.arctan2(point1[1] - point2[1],
                                                                                    point1[0] - point2[0])
    angle = np.abs(np.degrees(radians))
    return angle


def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return

    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])
