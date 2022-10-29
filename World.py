from Engine import Actor
from Engine.Singleton import Singleton
import Map.Room as Room
import Player as Player


class World(metaclass=Singleton):
    def __init__(self):
        self.player = Player.Player()
        self.room = Room.Room(self.player)
        self.is_debug = False

    def poll_input(self, event):
        Actor.ActorManager.poll_input_all(event)

    def update(self):
        Actor.ActorManager.update_all()

    def draw(self):
        Actor.ActorManager.draw_all()

    def toggle_debug(self):
        self.is_debug = not self.is_debug