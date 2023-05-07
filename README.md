# Minesweeper CLI in Python

Minesweeper is a classic puzzle game where the objective is to clear a grid of hidden "mines" without detonating any of them. This implementation is a command-line interface (CLI) version of the game, written in Python.

### Game Rules

1. **Game Grid**: The game grid is presented with cells, and mines are randomly distributed in it. You cannot see the mines.

2. **Cell States**: Cells have two states: unopened & opened. 
   - **Unopened**: Blank and selectable.
   - **Opened**: Exposed. Displays count of adjacent (up, down, right, left or any diagonal) mines.

3. **Player Actions**: The player selects a cell to open.
   - If the selected cell has a mine, the player blows up the grid and loses the game.
   - If the selected cell does not have a mine, the clicked cell displays a number to indicate the count of mines diagonally and/or adjacent to it, or a blank tile ("0") if there are no adjacent mines.

4. **How to Win**: Open all non-mine cells without detonating any mines.

## How to Play

Run the Python script `play.py`. You will be prompted to enter the width and height of the grid. Then, the game will start for you to guess non-mine coordinate positions.

Good luck, and have fun!