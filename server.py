import socket

def rps_server():
    
    # host IP address as host name
    host = socket.gethostname()
    port = 5001

    # socket instance (default values: AF_INET -> IPv4, SOCK_STREAM -> TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host,port)) # bind socket to a address

    server_socket.listen(2) # set how many connections allowed
    
    # conn - a special socket object send or receive data
    # addr - address bound to the socket on the other end of connection
    conn, addr = server_socket.accept() 

    print(f"Connected device address: {str(addr)}")

    while True:
        # receive data stream (won't accept data packet (bytes type) greater than 1024 bytes)
        data = conn.recv(1024) # b"msg" -> "msg" (bytes type to string type)
        
        str_data = data.decode()
        print(f"Received message: {str_data}")

        # close connection
        if str_data == "bye":
            # close client connection
            conn.close()
            print("One of the players left, game over.")
            server_socket.close()

if __name__ == '__main__':
    rps_server()