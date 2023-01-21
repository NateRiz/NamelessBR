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
    """
    Object that controls all actors
    """

    def __init__(self, network):
        self.network = network
        self.room = Room()
        self.players = {}
        self.is_debug = False
        self.server_logic = ServerLogic()
        self.client_logic = ClientLogic()
        self.debugger = Debugger()
        self.my_id = -1

    def initial_sync(self):
        """
        Immediately called when the game starts to get all starting parameters
        """
        self.network.client.send({MessageMapper.INITIAL_SYNC_REQUEST: None})
        # self.room = Room.Room(self.player)

    def on_initial_sync_response(self, initial_sync_response: InitialSyncResponse):
        """
        Server's response in the beginning of the game. Contains all needed parameters to start the game
        :param initial_sync_response: Parameters to start the game
        """
        self.my_id = initial_sync_response.my_id
        for p in initial_sync_response.players:
            self.players[p] = Player(p, p == self.my_id)

    def get_my_player(self) -> Player | None:
        """
        Gets the local player.
        :return: local Player or None if game hasn't had initial sync yet.
        """
        if self.my_id in self.players:
            return self.players[self.my_id]
        return None

    def poll_input(self, event):
        """
        Forward polling event to all actors
        :param event: Single poll event
        """
        Actor.ActorManager.poll_input_all(event)

    def update(self):
        """
        Call all actor updates
        """
        Actor.ActorManager.update_all()

    def draw(self):
        """
        Draw all actors
        """
        Actor.ActorManager.draw_all()

    def toggle_debug(self):
        """
        toggles whether the global debug is enabled
        """
        self.is_debug = not self.is_debug
