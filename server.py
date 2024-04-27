from collections import namedtuple
from enum import Enum
import socket
from typing import List

BUFFER_SIZE = 1024

ClientInstance = namedtuple("ClientInstance", ["socket", "nickname"])


class TextColor(Enum):
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    WHITE = "\033[39m"


def fmt_text(text: str, color: TextColor):
    return color + text + TextColor.WHITE.value


class ChatServer:
    def __init__(self, host="localhost", port=8384) -> None:
        self.clients: List[ClientInstance] = []
        self.HOST: str = host
        self.PORT: str = port

    def ask_for_nickname(self, client_socket: socket.socket) -> str:
        """
        Request user to identify themselves
        """
        client_socket.send("Introduce yourself: ".encode())
        encoded_nickname = client_socket.recv(BUFFER_SIZE)

        if encoded_nickname:
            resp = "Hello ".encode() + encoded_nickname
            client_socket.send(resp)

        return encoded_nickname.decode().strip()

    def server_msg(self, msg: str):
        """
        Send server notification to all connections
        """
        msg = fmt_text(msg, TextColor.ORANGE.value)
        print(f"Sending server msg: {msg}")

        for client in self.clients:
            client.socket.send(msg.encode())
        print("Finished sending server msg.")

    def broadcast(self, msg: bytes, sender: ClientInstance):
        """
        Broadcast a sender's msg to all other participants
        """
        msg = fmt_text(f"<{sender.nickname}> {msg.decode()}", TextColor.GREEN.value).encode()
        print(f"Broadcasting a msg: {msg}")

        for client in self.clients:
            if client != sender:
                client.socket.send(msg)
        print("Finished broadcasting")

    def add_client(self, client: ClientInstance):
        """
        Add client to list of connections
        """
        print(f"Currently {len(self.clients)} clients in chat. Adding new client..")
        self.clients.append(client)
        print(f"New client added. Currently {len(self.clients)} clients in chat.")

    def remove_client(self, client: ClientInstance):
        """
        Remove client from list of connections
        """
        print(f"Currently {len(self.clients)} clients in chat. Removing {client.nickname}..")

        if client in self.clients:
            print("client in list")
            self.clients.remove(client)
            print("client removed from list")
            client.socket.close()
            print("client conn closed")

            self.server_msg(f"{client.nickname} quit the chat.")

        print(f"{client.nickname} removed. Currently {len(self.clients)} clients in chat.")

    def handle_client(self, client_socket: socket.socket):
        """
        Handles new client connection
        """
        nickname = self.ask_for_nickname(client_socket)
        self.server_msg(f"\n{nickname} has joined the chat.\n")

        client = ClientInstance(socket=client_socket, nickname=nickname)
        self.add_client(client)

        while True:
            try:
                msg = client_socket.recv(BUFFER_SIZE)
                if msg:
                    self.broadcast(msg, client)
                else:
                    self.remove_client(client)
                    break

            except Exception as e:
                print(f"Error: {e}")
                self.remove_client(client)
                break

    def run(self):
        """
        Main method to run server
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen()

        print(f"Server listening on {self.HOST}:{self.PORT}")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"New connection from {client_address}")

                self.handle_client(client_socket)

            except KeyboardInterrupt:
                print("KeyboardInterrupt received. Stopping server.")
                break

            except Exception as e:
                print(f"Unkown exception: {e}")
                break

        print(f"Closing client connections. Total {len(self.clients)}")
        for client in self.clients:
            client.socket.close()
        print("Client connections closed.")

        server_socket.close()
        print("Server stopped.")


if __name__ == "__main__":
    server = ChatServer()
    server.run()
