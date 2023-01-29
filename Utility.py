from math import sqrt

import pygame


def clamp(num: int, min_value: int, max_value: int) -> int:
    return max(min(num, max_value), min_value)


def rot_center(image, angle, x, y):
    """
    Helper function - should remove from here
    https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


def normalize(vec2: tuple[float, float]) -> tuple[float, float]:
    input_magnitude = sqrt(vec2[0] ** 2 + vec2[1] ** 2)
    if input_magnitude == 0:
        return vec2
    return vec2[0] / input_magnitude, vec2[1] / input_magnitude
