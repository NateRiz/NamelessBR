from math import sqrt, copysign
import pygame
from time import time
from collections import deque

from Engine.Actor import Actor
from Engine.Camera import Camera
from Engine.DrawLayer import DrawLayer
from Map.Door import Door
from MessageMapper import MessageMapper
from Serializable.Movement import Movement


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
        self.pos: list = [800, 500]  # Absolute position in room
        self.triangle_size: int = 10
        self.collision_size: list = [6, 6]  # Marked by small square inside the player
        self.input: list = [0, 0]  # WASD input. vector from -1,-1 to 1,1. 0,0 is standing still.
        self.velocity: list = [0, 0]
        self.max_speed: int = 10
        self.acceleration_rate: float = 1.8
        self.friction: float = 0.2
        self.direction_lookup = {
            (0, -1): ((0, -self.triangle_size), (-self.triangle_size, self.triangle_size // 2),
                      (self.triangle_size, self.triangle_size // 2)),  # N
            (1, -1): ((3 * self.triangle_size / 4, -3 * self.triangle_size / 4),
                      (-self.triangle_size, -3 * self.triangle_size / 4),
                      (3 * self.triangle_size / 4, self.triangle_size)),  # NE,
            (1, 0): ((self.triangle_size, 0), (-self.triangle_size // 2, -self.triangle_size),
                     (-self.triangle_size // 2, self.triangle_size)),  # E
            (1, 1): (
                (3 * self.triangle_size / 4, 3 * self.triangle_size / 4),
                (-self.triangle_size, 3 * self.triangle_size / 4),
                (3 * self.triangle_size / 4, -self.triangle_size)),  # SE
            (0, 1): ((0, self.triangle_size), (-self.triangle_size, -self.triangle_size // 2),
                     (self.triangle_size, -self.triangle_size // 2)),  # S,
            (-1, 1): (
                (-3 * self.triangle_size / 4, 3 * self.triangle_size / 4),
                (self.triangle_size, 3 * self.triangle_size / 4),
                (-3 * self.triangle_size / 4, -self.triangle_size)),  # SW,
            (-1, 0): ((-self.triangle_size, 0), (self.triangle_size // 2, -self.triangle_size),
                      (self.triangle_size // 2, self.triangle_size)),  # W,
            (-1, -1): ((-3 * self.triangle_size / 4, -3 * self.triangle_size / 4),
                       (self.triangle_size, -3 * self.triangle_size / 4),
                       (-3 * self.triangle_size / 4, self.triangle_size)),  # NW,
        }
        self.direction: tuple = self.direction_lookup[(0, -1)]

        self.move_trail = deque([], maxlen=15)
        self.move_trail_particle_cooldown: float = .02
        self.move_trail_last_record_time = time()

        self.dash_cooldown: int = 2
        self.dash_impulse_force: int = 25
        self.dash_last_time = time()
        self.is_dashing: bool = False

        ##############
        # Networking
        ##############
        # Track the diff between messages sent to the server to reduce traffic
        # Dummy numbers to ensure its updated first frame
        self.last_message_sent = Movement(self.my_id, [-1, -1], [-9, -9])
        # Time since the last position was sent. Don't send it every frame. Reduce traffic
        self.time_last_position_sent: float = time()

    @property
    def rect(self):
        return pygame.rect.Rect(self.pos[0] - self.collision_size[0] // 2, self.pos[1] - self.collision_size[1] // 2,
                                *self.collision_size)

    @property
    def offset_position(self):
        center_x = self.get_screen().get_size()[0] // 2
        center_y = self.get_screen().get_size()[1] // 2
        abs_x, abs_y = self.pos
        return center_x - abs_x, center_y - abs_y

    def get_current_room(self):
        return self.get_world().room

    def draw(self, screen):
        self.draw_particles(screen)
        self.draw_player(screen)

    def draw_player(self, screen):
        # My player should always be drawn in the center of the screen. The room is drawn to offset me.
        if self.is_me:
            center_x = self.get_screen().get_size()[0] // 2
            center_y = self.get_screen().get_size()[1] // 2
            pygame.draw.polygon(screen, (100, 255, 100), [(center_x + d[0], center_y + d[1]) for d in self.direction])
        else:
            # Draw other players directly into the room to later be offset
            pygame.draw.polygon(self.get_current_room().get_surface(), (100, 255, 100),
                                [(self.pos[0] + d[0], self.pos[1] + d[1]) for d in
                                 self.direction])

    def draw_particles(self, screen):
        for i, (pos, input_dir) in enumerate(self.move_trail):
            if input_dir[0] or input_dir[1]:
                direction = self.direction_lookup[input_dir]
                offset = self.offset_position
                if self.is_me:
                    coords = [(pos[0] + d[0] + offset[0], pos[1] + d[1] + offset[1]) for d in direction]
                    surface_to_blit = screen
                else:
                    coords = [(pos[0] + d[0], pos[1] + d[1]) for d in direction]
                    surface_to_blit = self.get_current_room().get_surface()
                lx, ly = zip(*coords)
                min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
                target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
                shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
                pygame.draw.polygon(shape_surf, (100, 255, 100, 200 / (len(self.move_trail) - i)),
                                    [(x - min_x, y - min_y) for x, y in coords])
                surface_to_blit.blit(shape_surf, target_rect)
                # pygame.draw.polygon(screen, (100, 255, 100), coords)

    def get_pressed_input(self, pressed):
        if not self.is_me:
            return

        self.input[0] = pressed[pygame.K_d] - pressed[pygame.K_a]
        self.input[1] = pressed[pygame.K_s] - pressed[pygame.K_w]

    def poll_input(self, event):
        if not self.is_me:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.try_dash()
            if event.key == pygame.K_F12:
                self.get_world().toggle_debug()


    def update(self):
        self.move()
        self.try_add_trail()
        self.send_updates_to_server()

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
        walls = self.get_current_room().walls
        wall_collisions= [wall.rect for wall in walls]

        pos = list(self.pos)
        pos[0] += self.velocity[0]
        if pygame.rect.Rect(*pos, *self.collision_size).collidelist(wall_collisions) != -1:
            self.velocity[0] = 0

        pos = list(self.pos)
        pos[1] += self.velocity[1]
        if pygame.rect.Rect(*pos, *self.collision_size).collidelist(wall_collisions) != -1:
            self.velocity[1] = 0

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def send_updates_to_server(self):
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
            should_send_message = True

        if should_send_message:
            self.send_to_server({MessageMapper.MOVEMENT: message})

    def try_add_trail(self):
        if time() >= self.move_trail_last_record_time + self.move_trail_particle_cooldown:
            self.move_trail_last_record_time = time()
            self.move_trail.append((tuple(self.pos), tuple(self.input)))

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
            self.direction = self.direction_lookup[(0, -1)]
        elif dest_y - src_y == -1:  # move up
            self.pos = list(current_room.doors[Door.SOUTH].rect.center)
            self.pos[1] -= buffer
            self.direction = self.direction_lookup[(0, 1)]
        elif dest_x - src_x == 1:  # move right
            self.pos = list(current_room.doors[Door.WEST].rect.center)
            self.pos[0] += buffer
            self.direction = self.direction_lookup[(1, 0)]
        elif dest_x - src_x == -1:  # move left
            self.pos = list(current_room.doors[Door.EAST].rect.center)
            self.pos[0] -= buffer
            self.direction = self.direction_lookup[(-1, 0)]

    ############################
    # Below is called by server
    ############################
    def server_move_to(self, pos, input_direction):
        if pos:
            self.pos = pos
        if input_direction:
            self.input = input_direction
