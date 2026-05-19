# Rock Paper Scissors Multiplayer CLI

A multiplayer Rock Paper Scissors game built with Python sockets.

This project was created as a hands-on exercise in network programming. It lets two players connect to the same server from separate terminal sessions, send their moves over TCP, and play rounds until one player reaches three points.

## What I Built

- A TCP server that listens for two player connections
- A command-line client that can connect through localhost, LAN, or an ngrok TCP address
- Real-time message handling with separate threads for each connected player
- Round-based Rock Paper Scissors game logic
- Score tracking for both players
- Match-ending behavior when a player reaches three wins
- Basic connection handling for disconnects, exits, and server shutdowns

## Tech Stack

- Python
- `socket` for TCP networking
- `threading` for handling multiple clients at the same time
- CLI-based user interaction

## How It Works

The server opens a TCP socket on port `5002` and waits for player connections. Each client connection is handled in its own thread, so both players can send moves independently.

When both players have submitted a valid move, the server compares the choices, updates the score, and broadcasts the round result back to both clients. After each round, player moves are reset while scores are preserved. The match ends when either player reaches three points.

Clients run in the terminal and maintain a background listener thread so they can receive server messages while still accepting player input.

## Running the Project

Start the server:

```bash
python3 server.py
```

Start two clients in separate terminal windows:

```bash
python3 client.py
```

When prompted, enter the server address:

```text
localhost
```

If you expose the server with ngrok TCP, you can also enter an address like:

```text
0.tcp.eu.ngrok.io:15234
```

The client also accepts addresses prefixed with `tcp://`.

## Gameplay

Each player can enter:

```text
rock
paper
scissors
```

To leave the game:

```text
bye
```

If one player exits, the server closes the active game session.

## Project Structure

```text
.
├── client.py   # CLI client for connecting to the game server
├── server.py   # TCP server, player state, scoring, and game logic
└── README.md
```

## What I Practiced

This project helped me practice the fundamentals of socket-based communication, client-server architecture, concurrent connection handling, and simple state management across multiple users. I also focused on making the terminal experience practical by keeping the client responsive while server messages arrive in the background.
