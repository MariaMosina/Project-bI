from environment.env_1d import *


def is_wall(pixel: np.array):
    """
    checks if pixel on map is wall or not
    """
    ray_color = np.array([90, 90, 0])
    if sum(pixel) > 250 * 3 or np.array_equal(pixel, ray_color):
        return False

    # if sum(pixel) > 250 * 3:
    #     return False

    return True


def cast_ray(plan: np.array, center: (float, float), angle: float, condition, display=False) -> np.array:
    """
    Casts a ray on *plan* from observer *center* point in direction defined by *angle*.
    Returns first pixel that matches provided *condition*.
    """
    x, y = center
    while not condition(plan[int(x), int(y)]):
        if display:
            plan[int(x), int(y)] = [90, 90, 0]
        x += np.cos(angle)
        y += np.sin(angle)
    return plan[int(x), int(y)]


def camera_1d(plan: np.array, center: (float, float), direction: float, view_angle: float, resolution: int, condition):
    """
    Represents 1d camera which scans *plan* from *center* point in given *direction*. 
    Camera has *view_angle* in radians and *resolution*. 
    Wall or obscure object is defined by *condition*. 
    Returns scan, which is numpy array with shape (resolution, 1).
    """
    scan = []
    for i in range(resolution):
        # display = True if any([i == 0, i == int(resolution/2), i == resolution - 1]) else False
        display = True
        ray_i_angle = direction - view_angle * (i / resolution - 0.5)
        scan.append(cast_ray(plan, center, ray_i_angle, condition, display))
    return np.array(scan)


def bresenham(x0, y0, x1, y1):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    Source: https://github.com/encukou/bresenham
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x * xx + y * yx, y0 + x * xy + y * yy
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
