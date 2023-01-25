from ClientLogic import ClientLogic
from Debugger import Debugger
from Engine import Actor
from Engine.Singleton import Singleton
from Map.Room import Room
from Menu.RoomFactory import RoomFactory
from MessageMapper import MessageMapper
from Player import Player
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse
from Serializable.InitialSyncResponse import InitialSyncResponse
from ServerLogic import ServerLogic


class World(metaclass=Singleton):
    """
    Object that controls all actors
    """

    def __init__(self, network):
        self.network = network
        self.room = None
        self.is_debug = False
        self.server_logic = ServerLogic()
        self.client_logic = ClientLogic()
        self.map = None
        self.debugger = Debugger()
        self.my_id = -1

    def on_start(self):
        """
        Immediately called once when the game starts
        """
        if self.network.server:
            self.server_logic.on_start()
        self.network.client.send({MessageMapper.INITIAL_SYNC_REQUEST: None})

    def on_initial_sync_response(self, initial_sync_response: InitialSyncResponse):
        """
        Server's response in the beginning of the game. Contains all needed parameters to start the game
        :param initial_sync_response: Parameters to start the game
        """
        self.my_id = initial_sync_response.my_id
        map_size = initial_sync_response.map_size
        self.map = [[None for _ in range(map_size)] for _ in range(map_size)]

    def get_my_player(self) -> Player | None:
        """
        Gets the local player.
        :return: local Player or None if game hasn't had initial sync yet.
        """
        if self.my_id in self.room.players:
            return self.room.players[self.my_id]
        return None

    def update_room(self, change_rooms_response: ChangeRoomsResponse):
        src = self.room.coordinates if self.room else None

        if src != change_rooms_response.room_coordinates:
            self.room = RoomFactory.create(change_rooms_response.room_coordinates)
        [self.room.try_add_player(player_id, player) for player_id, player in change_rooms_response.players.items()]
        if self.get_my_player() is not None:
            self.get_my_player().update_position_in_new_room(src, change_rooms_response.room_coordinates)

    def get_pressed_input(self, pressed):
        """
        Forward all pressed keys to all actors
        :param pressed: state of all keys
        """
        Actor.ActorManager.get_pressed_input_all(pressed)

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
