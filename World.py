from ClientLogic import ClientLogic
from Debugger import Debugger
from Engine import Actor
from Engine.Singleton import Singleton
from Map.Room import Room
from MessageMapper import MessageMapper
from Player import Player
from Serializable.InitialSyncResponse import InitialSyncResponse
from ServerLogic import ServerLogic


class World(metaclass=Singleton):
    def __init__(self, network):
        self.network = network
        self.room = None
        self.players = {}
        self.is_debug = False
        self.server_logic = ServerLogic()
        self.client_logic = ClientLogic()
        self.debugger = Debugger()
        self.my_id = -1

    def initial_sync(self):
        self.network.client.send({MessageMapper.INITIAL_SYNC_REQUEST: None})
        # self.room = Room.Room(self.player)

    def on_initial_sync_response(self, initial_sync_response: InitialSyncResponse):
        self.my_id = initial_sync_response.my_id
        for p in initial_sync_response.players:
            self.players[p] = Player(p, p == self.my_id)
        self.room = Room(self.players[self.my_id])


    def poll_input(self, event):
        Actor.ActorManager.poll_input_all(event)

    def update(self):
        Actor.ActorManager.update_all()

    def draw(self):
        Actor.ActorManager.draw_all()

    def toggle_debug(self):
        self.is_debug = not self.is_debug
