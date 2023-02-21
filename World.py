from ClientLogic import ClientLogic
from Debugger import Debugger
from Engine import Actor
from Engine.Singleton import Singleton
from HUD import HUD
from Map.RoomFactory import RoomFactory
from MessageMapper import MessageMapper
from Player import Player
from Serializable.ChangeRoomsResponse import ChangeRoomsResponse
from Serializable.InitialSyncResponse import InitialSyncResponse


class World(metaclass=Singleton):
    """
    Object that controls all actors
    """

    def __init__(self, client):
        self.client = client
        self.room = None
        self.is_debug = False
        self.client_logic = None
        self.map = None
        self.debugger = None
        self.my_id = -1
        self.hud = None

    def on_start(self):
        """
        Immediately called once when the game starts
        """
        self.client_logic = ClientLogic.new()
        self.debugger = Debugger.new()
        self.hud = HUD.new()
        self.client.send({MessageMapper.INITIAL_SYNC_REQUEST: None})

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
        if self.room and self.my_id in self.room.players:
            return self.room.players[self.my_id]
        return None

    def update_room(self, change_rooms_response: ChangeRoomsResponse):
        src = None
        if self.room is not None:
            src = self.room.coordinates
        if src != change_rooms_response.room_coordinates:
            if self.room:
                self.room.free()
            self.room = RoomFactory.create(change_rooms_response.room_coordinates)
            RoomFactory.update_with_change_room_response(self.room, change_rooms_response)
        [self.room.try_add_player(player_id, player) for player_id, player in change_rooms_response.players.items()]
        if player := self.get_my_player():
            player.update_position_in_new_room(src, change_rooms_response.room_coordinates)

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
        # Actor.ActorManager.check_collisions_all()
        Actor.ActorManager.clean_all()

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
