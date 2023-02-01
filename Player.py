from math import sqrt, copysign, atan2, degrees
import pygame
from time import time

from PlayerBodyBuilder import PlayerBodyBuilder
from Engine.Actor import Actor
from Engine.Camera import Camera
from Engine.DrawLayer import DrawLayer
from Map.Door import Door
from MessageMapper import MessageMapper
from Projectile.Simple import Simple
from Serializable.Movement import Movement
from Serializable.ShootProjectileRequest import ShootProjectileRequest
from Utility import rot_center, normalize


class Player(Actor):
    def __init__(self, my_id, is_me):
        super().__init__()
        self.my_id: int = my_id  # ID of the current player
        self.is_me: bool = is_me  # Whether this is the actual player or someone else
        if self.is_me:
            self.set_draw_layer(DrawLayer.PLAYER)
        else:
            self.set_draw_layer(DrawLayer.ENEMY_PLAYER)
        self.camera = Camera()
        self.map_coordinates = (-1, -1)
        self.pos: list = [800, 500]  # Absolute position in room
        self.collision_size: list = [6, 6]  # Marked by small square inside the player
        self.input: list = [0, 0]  # WASD input. vector from -1,-1 to 1,1. 0,0 is standing still.
        self.velocity: list = [0, 0]
        self.max_speed: int = 10
        self.acceleration_rate: float = 1.8
        self.friction: float = 0.2
        self.angle = 0

        # Replace this with a surface that always looks where the mouse is pointing.
        self.surface = PlayerBodyBuilder().add_triangle_base().build()

        self.dash_cooldown: int = 2
        self.dash_impulse_force: int = 25
        self.dash_last_time = time()
        self.is_dashing: bool = False

        self.shoot_cooldown = 0.8
        self.last_shoot_time = time()
        self.is_shot_queued = False  # Signifies that next update should spawn a shot (Don't add logic to poll())

        ##############
        # Networking
        ##############
        # Track the diff between messages sent to the server to reduce traffic
        # Dummy numbers to ensure its updated first frame
        self.last_message_sent = Movement(self.my_id, [-1, -1], [-9, -9], -1)
        # Time since the last position was sent. Don't send it every frame. Reduce traffic
        self.time_last_position_sent: float = time()

    @property
    def rect(self):
        return pygame.rect.Rect(self.pos[0] - self.collision_size[0] // 2 + self.surface.get_width() // 2,
                                self.pos[1] - self.collision_size[1] // 2 + self.surface.get_height() // 2,
                                *self.collision_size)

    @property
    def offset_position(self):
        center_x = self.get_screen().get_size()[0] // 2
        center_y = self.get_screen().get_size()[1] // 2
        abs_x, abs_y = self.pos
        return center_x - abs_x - self.surface.get_width() // 2, center_y - abs_y - self.surface.get_height() // 2

    def get_current_room(self):
        return self.get_world().room

    def draw(self, screen):
        self.draw_player(screen)

    def draw_player(self, screen):
        # My player should always be drawn in the center of the screen. The room is drawn to offset me.
        center_x = self.get_screen().get_size()[0] // 2
        center_y = self.get_screen().get_size()[1] // 2

        if self.is_me:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            self.angle = degrees(atan2(mouse_x - center_x, mouse_y - center_y)) + 180
            rotated_surface, rect = rot_center(self.surface, self.angle, center_x, center_y)
            screen.blit(rotated_surface, (rect.x, rect.y))
        else:
            # Draw other players directly into the room to later be offset
            rotated_surface, rect = rot_center(self.surface, self.angle, *self.rect.center)
            self.get_current_room().get_surface().blit(rotated_surface, rect)

    def get_pressed_input(self, pressed):
        if not self.is_me:
            return

        self.input[0] = pressed[pygame.K_d] - pressed[pygame.K_a]
        self.input[1] = pressed[pygame.K_s] - pressed[pygame.K_w]

        if pygame.mouse.get_pressed()[0]:
            self.try_shoot()

    def poll_input(self, event):
        if not self.is_me:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.try_dash()
            if event.key == pygame.K_F12:
                self.get_world().toggle_debug()

    def update(self):
        self.move()
        self.shoot()
        self.send_movement_to_server()

    def move(self):
        normalized_input = normalize(tuple(self.input))
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

    def move_and_collide(self):
        walls = self.get_current_room().walls
        wall_collisions = [wall.rect for wall in walls]

        original_pos = list(self.pos)
        self.pos[0] += self.velocity[0]
        if self.rect.collidelist(wall_collisions) != -1:
            self.velocity[0] = 0
            self.pos = original_pos

        original_pos = list(self.pos)
        self.pos[1] += self.velocity[1]
        if self.rect.collidelist(wall_collisions) != -1:
            self.velocity[1] = 0
            self.pos = original_pos

    def send_movement_to_server(self):
        if not self.is_me:
            return

        should_send_message = False
        message = Movement(self.my_id)

        if self.input != self.last_message_sent.direction:
            message.direction = list(self.input)
            self.last_message_sent.direction = list(message.direction)
            should_send_message = True

        time_between_movement_updates = 0.01  # 100ms
        if time() - self.time_last_position_sent > time_between_movement_updates and (
                int(self.pos[0]) != self.last_message_sent.pos[0] or int(self.pos[1]) != self.last_message_sent.pos[1]):
            self.time_last_position_sent = time()
            message.pos = [int(self.pos[0]), int(self.pos[1])]
            self.last_message_sent.pos = list(message.pos)
            message.angle = self.angle
            self.last_message_sent.angle = int(self.angle)
            should_send_message = True

        if should_send_message:
            self.send_to_server({MessageMapper.MOVEMENT: message})

    def try_dash(self):
        if time() >= self.dash_last_time + self.dash_cooldown:
            self.dash_last_time = time()
            self.is_dashing = True

    def update_position_in_new_room(self, src, dest):
        """
        Moves player position from one door's to the opposite door's position when switching rooms.
        :param src: room player is leaving
        :param dest: room player is entering
        """
        if src is None:
            self.pos = [800, 500]
            return

        src_y, src_x = src
        dest_y, dest_x = dest
        buffer = 32
        current_room = self.get_current_room()
        if dest_y - src_y == 1:  # move down
            self.pos = list(current_room.doors[Door.NORTH].rect.center)
            self.pos[1] += buffer
            # self.direction = self.direction_lookup[(0, -1)]
        elif dest_y - src_y == -1:  # move up
            self.pos = list(current_room.doors[Door.SOUTH].rect.center)
            self.pos[1] -= buffer
            # self.direction = self.direction_lookup[(0, 1)]
        elif dest_x - src_x == 1:  # move right
            self.pos = list(current_room.doors[Door.WEST].rect.center)
            self.pos[0] += buffer
            # self.direction = self.direction_lookup[(1, 0)]
        elif dest_x - src_x == -1:  # move left
            self.pos = list(current_room.doors[Door.EAST].rect.center)
            self.pos[0] -= buffer
            # self.direction = self.direction_lookup[(-1, 0)]

    def try_shoot(self):
        if time() - self.last_shoot_time > self.shoot_cooldown:
            self.is_shot_queued = True
            self.last_shoot_time = time()

    def shoot(self):
        if not self.is_shot_queued:
            return
        self.is_shot_queued = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        center_x = self.get_screen().get_size()[0] // 2
        center_y = self.get_screen().get_size()[1] // 2
        direction = normalize((mouse_x - center_x, mouse_y - center_y))
        position = list(self.rect.center)
        bullet = Simple(position, direction, self.get_current_room())
        self.get_current_room().spawn_projectile(bullet)
        self.send_to_server({MessageMapper.SHOOT_PROJECTILE_REQUEST: ShootProjectileRequest(position, direction)})

    ############################
    # Below is called by server
    ############################
    def server_move_to(self, pos, input_direction, angle):
        if pos:
            self.pos = pos
        if input_direction:
            self.input = input_direction
        if angle:
            self.angle = angle
