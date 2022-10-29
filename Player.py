from math import sqrt, copysign
import pygame
from time import time
from collections import deque

from Engine.Actor import Actor
from Engine.Camera import Camera
from Engine.Layer import Layer
from MessageMapper import MessageMapper


class Player(Actor):
    def __init__(self):
        super().__init__()
        self.set_draw_layer(Layer.PLAYER)
        self.camera = Camera()
        self.pos = [800, 500]
        self.triangle_size = 10
        self.collision_size = [6, 6]
        self.input = [0, 0]
        self.velocity = [0, 0]
        self.max_speed = 10
        self.acceleration_rate = 1.8
        self.friction = 0.2
        self.direction_lookup = {
            (0, -1): ((0, -self.triangle_size), (-10, 5), (10, 5)),  # N
            (1, -1): ((7.5, -7.5), (-10, -7.5), (7.5, 10)),  # NE,
            (1, 0): ((10, 0), (-5, -10), (-5, 10)),  # E
            (1, 1): ((7.5, 7.5), (-10, 7.5), (7.5, -10)),  # SE
            (0, 1): ((0, 10), (-10, -5), (10, -5)),  # S,
            (-1, 1): ((-7.5, 7.5), (10, 7.5), (-7.5, -10)),  # SW,
            (-1, 0): ((-10, 0), (5, -10), (5, 10)),  # W,
            (-1, -1): ((-7.5, -7.5), (10, -7.5), (-7.5, 10)),  # NW,
        }
        self.direction = self.direction_lookup[(0, -1)]

        self.move_trail = deque([], maxlen=15)
        self.move_trail_particle_cooldown = .02
        self.move_trail_last_record_time = time()

        self.dash_cooldown = 2
        self.dash_impulse_force = 25
        self.dash_last_time = time()
        self.is_dashing = False

    @property
    def rect(self):
        return pygame.rect.Rect(*self.pos, *self.collision_size)

    @property
    def offset_position(self):
        center_x = self.get_screen().get_size()[0] // 2
        center_y = self.get_screen().get_size()[1] // 2
        abs_x, abs_y = self.pos
        return center_x - abs_x, center_y - abs_y

    def draw(self, screen):
        self.draw_particles(screen)
        center_x = self.get_screen().get_size()[0] // 2
        center_y = self.get_screen().get_size()[1] // 2
        pygame.draw.polygon(screen, (100, 255, 100), [(center_x + d[0], center_y + d[1]) for d in self.direction])

    def draw_particles(self, screen):
        for i, (pos, input_dir) in enumerate(self.move_trail):
            if input_dir[0] or input_dir[1]:
                direction = self.direction_lookup[input_dir]
                offset = self.offset_position
                coords = [(pos[0] + d[0] + offset[0], pos[1] + d[1] + offset[1]) for d in direction]
                lx, ly = zip(*coords)
                min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
                target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
                shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
                pygame.draw.polygon(shape_surf, (100, 255, 100, 200 / (len(self.move_trail) - i)),
                                    [(x - min_x, y - min_y) for x, y in coords])
                screen.blit(shape_surf, target_rect)
                # pygame.draw.polygon(screen, (100, 255, 100), coords)

    def poll_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.input[1] -= 1
            if event.key == pygame.K_s:
                self.input[1] += 1
            if event.key == pygame.K_a:
                self.input[0] -= 1
            if event.key == pygame.K_d:
                self.input[0] += 1
            if event.key == pygame.K_j:
                self.try_dash()
            if event.key == pygame.K_F12:
                self.get_world().toggle_debug()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.input[1] += 1
            if event.key == pygame.K_s:
                self.input[1] -= 1
            if event.key == pygame.K_a:
                self.input[0] += 1
            if event.key == pygame.K_d:
                self.input[0] -= 1

    def update(self):
        self.move()
        self.try_add_trail()

    def move(self):
        normalized_input = [0, 0]
        input_magnitude = sqrt(self.input[0] ** 2 + self.input[1] ** 2)
        if input_magnitude != 0:
            normalized_input = [self.input[0] / input_magnitude, self.input[1] / input_magnitude]
        self.velocity[0] = self.velocity[0] + (
                normalized_input[0] * self.acceleration_rate - (self.friction * self.velocity[0]))
        self.velocity[1] = self.velocity[1] + (
                normalized_input[1] * self.acceleration_rate - (self.friction * self.velocity[1]))
        if self.is_dashing:
            self.is_dashing = False
            if self.input[0]:
                self.velocity[0] += copysign(self.dash_impulse_force, self.input[0])
            if self.input[1]:
                self.velocity[1] += copysign(self.dash_impulse_force, self.input[1])

        if abs(self.velocity[0]) < .1:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < .1:
            self.velocity[1] = 0

        self.move_and_collide()

        input_direction = tuple(self.input)
        if input_direction[0] or input_direction[1]:
            self.direction = self.direction_lookup[input_direction]

    def move_and_collide(self):
        """
        walls = self.get_world().room.walls

        pos = list(self.pos)
        pos[0] += self.velocity[0]
        if pygame.rect.Rect(*pos, *self.collision_size).collidelist(walls) != -1:
            self.velocity[0] = 0

        pos = list(self.pos)
        pos[1] += self.velocity[1]
        if pygame.rect.Rect(*pos, *self.collision_size).collidelist(walls) != -1:
            self.velocity[1] = 0
"""
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if any(self.velocity):
            self.send_to_server({MessageMapper.MOVEMENT: [int(self.pos[0]), int(self.pos[1])]})

    def try_add_trail(self):
        if time() >= self.move_trail_last_record_time + self.move_trail_particle_cooldown:
            self.move_trail_last_record_time = time()
            self.move_trail.append((tuple(self.pos), tuple(self.input)))

    def try_dash(self):
        if time() >= self.dash_last_time + self.dash_cooldown:
            self.dash_last_time = time()
            self.is_dashing = True
