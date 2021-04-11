# santorini

## Introduction
The game rules of the game Santorini can be found here: 
https://cdn.1j1ju.com/medias/fc/ec/5d-santorini-rulebook.pdf

This version of the game only enables the 2-player feature and human role 
instead of Gods (so only the first page of the rulebook is relevant).

Summary of the rules: each player has 2 pawns. 
Each turn, the player choose one pawn to move, then build. 
You can move to the eight adjacent spaces around you 
(including moving diagonally) and build on one of the adjacent eight spaces 
at the location that you have moved into 
(provided that there is no other pawns on it). 
The winner is the first player who has one of his pawn moved 
onto a level three building. 

## How to run the game

**Download Santorini**

Clone this project to create a local copy on your computer.

**Run the game**

Navigate to the directory of this project on your terminal. 
Run `__main__.py <player_type> <player_type>` to start the game.
`<player_type>` allows you choose a type of player to play with.
Note that you have to enter the path to the player python file. There are three
types of players that you can choose from.
Input `players/others/humanPlayer.py` to select a human player which 
enables you to choose the moves, `players/others/humanPlayer.py` to select 
a random player who choose moves randomly, and `players/valerie/valeriePlayer.py` 
to select an AI bot that uses minimax algorithm to choose the moves. 

Note that the order at which you input `<player_type>` determines the order
at which the players will play by.

You can also run `__main__.py -h` for help.

**How to select moves during the game 
(if you are using `humanPlayer.py` as a player)**

The board is printed with coordinates 0 to 4 on both 
the x-axis (horizontal axis) and the y-axis (vertical axis). 

After starting the game, you have to pick two locations 
as the starting locations for your pawns. When prompted, input four numbers from 
0 to 4, with a space in between each number and no leading or trailing whitespaces. 
The first pair of numbers is the coordinates of the first chosen location, 
and the second pair is that of the second chosen location. 

During the game, when prompted to enter a move, input six numbers from 0 to 4, 
with a space in between each number and no leading or trailing whitespaces.
The first pair of numbers is the coordinates of the chosen pawn, the second pair
is the location that you want that pawn to move to, and the third pair is
the location that you want to build on.
