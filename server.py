import socket
import threading
import os

game_loop = True
client_connections = []
server_socket = None
players = {}

def handle_client(conn, addr):
    print(f"New connection from: {addr}")
    
    global game_loop, client_connections, server_socket, players
    while game_loop:
        try:
            # receive data stream (won't accept data packet (bytes type) greater than 1024 bytes)
            data = conn.recv(1024) 
            
            if not data:
                print(f"[{addr}] disconnected abruptly.")
                break
            
            str_data = data.decode() # b"msg" -> "msg" (bytes type to string type)
            print(f"[{addr}] played: {str_data}")

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
            elif str_data in ["rock", "paper", "scissors"]:
                players[addr]["move"] = str_data
                print(f"[{addr}] Current move: {players[addr]['move']}, Score: {players[addr]['score']}")

                # if both players are connected and sent their play
                if len(players) == 2:
                    addrs = list(players.keys())
                    addr1, addr2 = addrs[0], addrs[1]
                    move1, move2 = players[addr1]["move"], players[addr2]["move"]

                    if move1 and move2:
                        # Game Logic
                        if move1 == move2:
                            result = "Tie!"
                        elif (move1 == "rock" and move2 == "scissors") or \
                             (move1 == "paper" and move2 == "rock") or \
                             (move1 == "scissors" and move2 == "paper"):
                            players[addr1]["score"] += 1
                            result = f"Player 1 WON! ({move1} beats {move2})"
                        else:
                            players[addr2]["score"] += 1
                            result = f"Player 2 WON! ({move2} beats {move1})"
                        # Round result message
                        final_msg = f"\n--- RESULT ---\n{result}\nScore -> P1: {players[addr1]['score']} | P2: {players[addr2]['score']}\n"
                        
                        for client in client_connections:
                            try:
                                client.send(final_msg.encode())
                            except Exception:
                                pass

                        # End game when one of the scores is three 
                        if players[addr1]["score"] == 3 or players[addr2]["score"] == 3:
                            winner = "Player 1" if players[addr1]["score"] == 3 else "Player 2"
                            game_over_msg = f"\n*** OYUN BİTTİ! {winner} maçı kazandı! ***\n"
                            
                            for client in client_connections:
                                try:
                                    client.send(game_over_msg.encode())
                                    client.close()
                                except Exception:
                                    pass
                            
                            print(f"Match over. {winner} won.")
                            game_loop = False
                            if server_socket:
                                server_socket.close()
                            break

                        # reset moves of both players
                        players[addr1]["move"] = None
                        players[addr2]["move"] = None

        except Exception as e:
            print(f"Error with connection from {addr}: {e}")
            break

def rps_server():
    global server_socket, client_connections, players
    # 0.0.0.0 yaparak sunucunun localhost, LAN ve ngrok üzerinden gelen bağlantıları dinlemesini sağlıyoruz
    host = '0.0.0.0'
    port = 5002

    # socket instance (default parameters: AF_INET -> IPv4, SOCK_STREAM -> TCP)
    server_socket = socket.socket()
    server_socket.bind((host,port)) # bind socket to a address

    server_socket.listen(2) # set how many connections allowed
    while game_loop:
        try:
            # conn - a special socket object send or receive data
            # addr - address bound to the socket on the other end of connection
            conn, addr = server_socket.accept() 
            client_connections.append(conn)

            players[addr] = {"score": 0, "move": None}
            
            thread = threading.Thread(target = handle_client, args = (conn, addr), daemon=True)
            thread.start()
            
            print(f"Active connections: {threading.active_count() - 1}")
            
        # when server_socket closes in handle_client(), it throws an exception
        except Exception:
            break


if __name__ == '__main__':
    try:
        rps_server()
    except KeyboardInterrupt:
        print("\nServer shut down by user.")
        os._exit(0)