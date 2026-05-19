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
            
            # Sunucudan gelen oyun sonucunu ekrana yazdır (flush=True ile anında bastırıyoruz)
            print(f"{data.decode()}\n-> ", end="", flush=True)
        except Exception:
            print("\n Connection lost. Game over.")
            os._exit(0)

def rps_client():
    # enter the ngrok address to set server
    address = input("Enter the server address (localhost or 0.tcp.eu.ngrok.io:15234): ")
    
    if ":" in address:
        host, port_str = address.split(":")
        port = int(port_str)
    else:
        host = address
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
    try:
        rps_client()
    except KeyboardInterrupt:
        print("\nGame exited by user.")
        os._exit(0)