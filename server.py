import socket
import threading

game_loop = True
client_connections = []
server_socket = None

def handle_client(conn, addr):
    print(f"New connection from: {addr}")
    
    global game_loop, client_connections, server_socket
    while game_loop:
        try:
            # receive data stream (won't accept data packet (bytes type) greater than 1024 bytes)
            data = conn.recv(1024) 
            
            str_data = data.decode() # b"msg" -> "msg" (bytes type to string type)
            print(f"Received message: {str_data}")

            # close connection
            if str_data == "exit":
                print("One of the players left, game over.")
                game_loop = False
                
                for client in client_connections:
                    try:
                        client.close()
                    except Exception:
                        pass
                
                if server_socket:
                    server_socket.close()
                break

        except Exception as e:
            print(f"Error with connection from {addr}: {e}")
            break

def rps_server():
    global server_socket, client_connections
    # host IP address as host name
    host = socket.gethostname()
    port = 5002

    # socket instance (default values: AF_INET -> IPv4, SOCK_STREAM -> TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host,port)) # bind socket to a address

    server_socket.listen(2) # set how many connections allowed
    while game_loop:
        try:
            # conn - a special socket object send or receive data
            # addr - address bound to the socket on the other end of connection
            conn, addr = server_socket.accept() 
            client_connections.append(conn)
            thread = threading.Thread(target = handle_client, args = (conn, addr), daemon=True)
            thread.start()
            print(f"Active connections: {threading.active_count()}")
            
        # when server_socket closes in handle_client(), it throws an exception
        except Exception:
            break


if __name__ == '__main__':
    rps_server()