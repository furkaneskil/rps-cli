import socket
import threading
import os

def check_connection(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\nServer shut down. Game over.")
                os._exit(0)
        except Exception:
            print("\n Connection lost. Game over.")
            os._exit(0)

def rps_client():
    host = socket.gethostname()
    port = 5002

    client_socket = socket.socket()
    client_socket.connect((host, port))

    recv_thread = threading.Thread(target = check_connection, args = (client_socket,), daemon = True)
    recv_thread.start()

    game_loop = True
    while game_loop:
        print("Enter one of rock, paper, scissors or bye to end game.")
        msg = input("-> ")
        msg = msg.lower().strip()

        if msg in ("rock", "paper", "scissors", "bye"):
            # turn string data into bytes type data package
            try:
                match msg:
                    case "rock" | "paper" | "scissors":
                        client_socket.send(msg.encode())
                    case "bye":
                        # player ends the connection
                        game_loop = False
                        client_socket.send("exit".encode()) # inform server about closing socket
            except Exception:
                pass
        else:
            print("Not one of the valid options.")

if __name__ == '__main__':
    rps_client()