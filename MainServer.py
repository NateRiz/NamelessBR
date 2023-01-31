from multiprocessing import Process

from Engine.Game import Game
from MessageMapper import MessageMapper
from Networking.Server import Server
from Serializable.Empty import Empty
from Serializable.ListClientsResponse import ListClientsResponse
from World import World


class MainServer:
    def __init__(self):
        self.process = Process(target=self._start_server)
        self.server = None

    def start_process(self):
        self.process.start()

    def _start_server(self):
        self.server = Server()

        while True:
            message = self.server.get_next_message()
            if message:
                if MessageMapper.LIST_CLIENTS_REQUEST in message.message:
                    self.server.send_all({MessageMapper.LIST_CLIENTS_RESPONSE: ListClientsResponse(
                        list(self.server.clients.keys()))})
                if MessageMapper.START in message.message:
                    self.server.send_all({MessageMapper.START: Empty()})
                    break
        self._start_game()

    def _start_game(self):
        game = Game(None, self.server)
        world = World(None, self.server)
        game.main_loop(world)


def main():
    #Start as main process. Dont create a new one.
    pass


if __name__ == '__main__':
    main()
