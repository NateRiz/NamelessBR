from multiprocessing import Process

import pygame

from MessageMapper import MessageMapper
from Networking.Server import Server
from Serializable.Empty import Empty
from Serializable.ListClientsResponse import ListClientsResponse
from ServerLogic import ServerLogic


class MainServer:
    def __init__(self):
        self.server = Server()
        self.server_logic = ServerLogic(self.server)
        self.clock = pygame.time.Clock()
        self.MAX_FPS = 60

    def start_server(self):
        while True:
            message = self.server.get_next_message()
            if message:
                if MessageMapper.LIST_CLIENTS_REQUEST in message.message:
                    self.server.send_all({MessageMapper.LIST_CLIENTS_RESPONSE: ListClientsResponse(
                        list(self.server.clients.keys()))})
                if MessageMapper.START in message.message:
                    self.server_logic.on_start()
                    self.server.send_all({MessageMapper.START: Empty()})
                    break
        self._start_game()

    def _start_game(self):
        while 1:
            self.clock.tick(self.MAX_FPS)
            self.server_logic.update()


def _create_server():
    MainServer().start_server()


def create_server(should_start_new_process):
    if should_start_new_process:
        Process(target=_create_server).start()
        return
    _create_server()


def main():
    create_server(False)
    # No way to click start from here.


if __name__ == '__main__':
    main()
