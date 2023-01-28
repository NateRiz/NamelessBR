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
