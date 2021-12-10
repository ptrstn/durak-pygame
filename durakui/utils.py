from collections.abc import Iterable

from pygame.math import Vector2
from pygame.surface import Surface


def elementwise_add(a: Iterable, b: Iterable):
    iterable_type = type(a)
    return iterable_type.__call__(map(sum, zip(a, b)))


def calculate_rotation_offset(surface: Surface, angle, pivot=(0, 0)):
    width, height = surface.get_size()

    corner_points = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height),
    ]

    pivot_vector = Vector2(pivot)

    corner_vectors = [Vector2(corner_point) for corner_point in corner_points]
    rotated_corner_vectors = [vector.rotate(-angle) for vector in corner_vectors]

    rotated_pivot_vector = pivot_vector.rotate(-angle)

    min_x = min([vector.x for vector in rotated_corner_vectors])
    min_y = min([vector.y for vector in rotated_corner_vectors])

    offset_x = -((rotated_pivot_vector.x - min_x) - pivot_vector.x)
    offset_y = -((rotated_pivot_vector.y - min_y) - pivot_vector.y)

    return offset_x, offset_y
