import socket
import threading

BUFFER_SIZE = 1024


class ChatClient:
    def __init__(self, host="localhost", port=8384) -> None:
        self.HOST: str = host
        self.PORT: str = port

    def receive_msg(self, client_socket: socket.socket):
        """
        Receive and print msg from server
        """
        while True:
            try:
                msg = client_socket.recv(BUFFER_SIZE)
                print(msg.decode())
            except Exception as e:
                print(f"Error receiving msg: {e}")
                client_socket.close()
                break

    def send_msg(self, client_socket: socket.socket):
        """
        Send msg to server
        """
        while True:
            try:
                msg = input()
                client_socket.send(msg.encode())

            except KeyboardInterrupt:
                print("KeyboardInterrupt received. Quitting chat.")
                client_socket.close()
                print("Connection closed.")
                break

            except Exception as e:
                print(f"Error sending msg: {e}")
                client_socket.close()
                print("Connection closed.")
                break

        print("outside inf loop")

    def run(self):
        """
        Main program to run client
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST, self.PORT))

        receiver_thread = threading.Thread(target=self.receive_msg, args=(client_socket,))
        sender_thread = threading.Thread(target=self.send_msg, args=(client_socket,))

        try:
            receiver_thread.start()
            sender_thread.start()

            # must join, else program quits immediately
            receiver_thread.join()
            sender_thread.join()

        except Exception as e:
            print(f"Error: {e}")

        print("Quitting the chat.")
        client_socket.close()


if __name__ == "__main__":
    client = ChatClient()
    client.run()
