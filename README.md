# StaleMate
Two Piece Chess War Game - and AI game playing agents <br>Course Project for the course - Artificial Intelligence CSL3090

## About the Game
The goal of this project was to build an AI agent that can feasibly and optimally play a game of stalemate between 2 chess pieces that can be any of the following: Knight, Bishop, Queen and Rook. The 2-player game begins with both players deciding which piece they will be using. Each piece moves according to classic chess rules.

The players can be one of 4 types:
1. An AI that uses a minimax algorithm to determine its next move.
2. An AI that uses the alpha-beta pruning algorithm to determine its next move.
3. A Human Player (user inputs the position they want to move to)
4. A player that randomly selects a move from available legal moves. 

The game will then end when there are no possible moves left for a player to play (no valid moves), or a player is unable to make a move in the given time(forfeit). In either case, the player unable to make a move will lose.

## Running the project

First install all dependencies using the following command.
```
pip install -r requirements.txt

// if this does now work then you can try ***python -m pip install -r requirements.txt***
```

Now to play the game use the command:
```
python play.py
```
### Simulations

### Team

The project was made by :

Soumik Roy
<br>
Stuti Aswani
<br>
Yash Bhargava
