import socket

def rps_client():
    host = socket.gethostname()
    port = 5002

    client_socket = socket.socket()
    client_socket.connect((host, port))

    game_loop = True
    while game_loop:
        print("Enter one of rock, paper, scissors or bye to end game.")
        msg = input("-> ")
        msg.lower().strip()

        if msg in ("rock", "paper", "scissors", "bye"):
            # turn string data into bytes type data package
            match msg:
                case "rock" | "paper" | "scissors":
                    client_socket.send(msg.encode())
                case "bye":
                    # player ends the connection
                    game_loop = False
                    client_socket.send("exit".encode()) # inform server about closing socket
                    client_socket.close() # close socket
        else:
            print("Not one of the valid options.")

if __name__ == '__main__':
    rps_client()