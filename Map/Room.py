import pygame

from Engine.Actor import Actor
from Engine.Layer import Layer
from Map.Door import Door
from Map.Ground import Ground


class Room(Actor):
    """
    Contains a player and other entities
    """

    def __init__(self):
        super().__init__()
        self.set_draw_layer(Layer.ROOM)
        self.width = 2500
        self.height = 1500
        self.surface = pygame.Surface((self.width, self.height))
        self.ground = Ground(self.surface)
        self.doors = [Door(self.surface, Door.NORTH), Door(self.surface, Door.EAST), Door(self.surface, Door.SOUTH),
                      Door(self.surface, Door.WEST)]

    def draw(self, screen):
        """
        Draw the room in relation to the players offset position.
        Current player should always be in the center.
        Everything in the room is drawn to this surface which is also offset
        :param screen: Screen to draw the surface to
        """
        player = self.get_world().get_my_player()
        if not player:
            return
        screen.blit(self.surface, player.offset_position)

    def draw_to_room(self, surface, position):
        """
        Draw an entity to the surface which will be offset by the players position
        :param surface: Offset surface
        :param position: Position relative to the room to draw at
        """
        self.surface.blit(surface, position)

    def get_surface(self):
        """
        Get the offset surface to draw directly to
        :return: Offset surface
        """
        return self.surface
