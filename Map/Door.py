import pygame

from Engine.Actor import Actor
from Engine.Debug import debug
from Engine.DrawLayer import DrawLayer
from MessageMapper import MessageMapper
from Serializable.ChangeRoomsRequest import ChangeRoomsRequest


class Door(Actor):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, surface, direction, connected_room_coordinates):
        super().__init__()
        self.set_draw_layer(DrawLayer.STRUCTURE)
        self.surface = surface
        self.direction = direction
        self.connecting_room_coordinates = connected_room_coordinates
        self.width = 80
        self.height = 10
        room_w, room_h = self.surface.get_size()
        self.rect = {
            Door.NORTH: pygame.rect.Rect(room_w // 2 - self.width // 2, 0, self.width, self.height),
            Door.SOUTH: pygame.rect.Rect(room_w // 2 - self.width // 2, room_h - self.height, self.width, self.height),
            Door.WEST: pygame.rect.Rect(0, room_h // 2 - self.width // 2, self.height, self.width),
            Door.EAST: pygame.rect.Rect(room_w - self.height, room_h // 2 - self.width // 2, self.height, self.width)
        }[self.direction]

    def _update(self):
        player = self.get_world().get_my_player()
        if not player:
            return
        if self.rect.colliderect(player.rect):
            self.send_to_server({MessageMapper.CHANGE_ROOMS_REQUEST: ChangeRoomsRequest(self.connecting_room_coordinates)})

    def _draw(self, screen):
        self._draw_doors()

    @debug
    def _poll_input(self, event):
        request = {MessageMapper.CHANGE_ROOMS_REQUEST: ChangeRoomsRequest(self.connecting_room_coordinates)}
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.direction == Door.SOUTH:
                self.send_to_server(request)
            if event.key == pygame.K_UP and self.direction == Door.NORTH:
                self.send_to_server(request)
            if event.key == pygame.K_RIGHT and self.direction == Door.EAST:
                self.send_to_server(request)
            if event.key == pygame.K_LEFT and self.direction == Door.WEST:
                self.send_to_server(request)

    def _draw_doors(self):
        pygame.draw.rect(self.surface, (200, 200, 200), self.rect)
