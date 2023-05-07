"""
Minesweeper CLI

This module contains the classes and logic for Minesweeper. To play the game, create an instance of the Minesweeper
class and call the `play()` method. For more information, see the README file.
"""

import random
from typing import List, Tuple
from collections import namedtuple

# noinspection PyTypeChecker
Coordinate = namedtuple("Coordinate", "row column")


class Cell:
    def __init__(self, has_mine: bool, adjacent_mines_count: int, is_open=False):
        self.has_mine = has_mine
        self.adjacent_mines_count = adjacent_mines_count
        self.is_open = is_open

    def open(self):
        self.is_open = True

    def unopened_non_mine(self):
        return self.is_open is False and self.has_mine is False

    def __str__(self):
        """will be called when we try to print a cell object, making it easier to print the grid"""
        if self.is_open:
            # once opened, can only be 0 or count of adjacent mines; can't display mine object
            return str(self.adjacent_mines_count) if self.adjacent_mines_count != 0 else "0"
        else:
            return " "


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = self._create_empty_cells()
        # arbitrary rule that ~1/5 or less of the grid is mines
        self.mine_count = (self.width * self.height) // 4
        self._set_cell_mines_and_adjacent_counts()

    def has_unopened_non_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.unopened_non_mine():
                    return True
        return False

    def _create_empty_cells(self) -> List[List[Cell]]:
        return [[Cell(has_mine=False, adjacent_mines_count=0) for _ in range(self.width)] for _ in range(self.height)]

    def _set_cell_mines_and_adjacent_counts(self):
        coordinate_positions = self._generate_grid_coordinate_positions()
        mine_positions = self._generate_mine_positions(coordinate_positions)
        self._place_mines(mine_positions)
        non_mine_positions = self._identify_non_mine_positions(coordinate_positions, mine_positions)
        self._set_adjacent_mine_count(non_mine_positions)

    def _generate_grid_coordinate_positions(self):
        return [(row, col) for row in range(self.height) for col in range(self.width)]

    def _generate_mine_positions(self, coordinate_positions) -> List[Tuple[int, int]]:
        """Generates mine positions like [(0, 1), (0, 2)]"""
        return random.sample(coordinate_positions, self.mine_count)

    def _identify_non_mine_positions(self, coordinate_positions, mine_positions):
        return set(coordinate_positions) - set(mine_positions)

    def _place_mines(self, mine_positions):
        """Randomly places mines on cells"""
        for row_index, column_index in mine_positions:
            self.cells[row_index][column_index].has_mine = True
        return self.cells

    def _is_valid_position(self, row_index: int, column_index: int) -> bool:
        return 0 <= row_index < self.height and 0 <= column_index < self.width

    def _set_adjacent_mine_count(self, non_mine_positions):
        for empty_row_index, empty_column_index in non_mine_positions:
            count = 0
            # row+2 on upper end b/c exclusive
            for row_index in range(empty_row_index-1, empty_row_index+2):
                for column_index in range(empty_column_index-1, empty_column_index+2):
                    if self._is_valid_position(row_index, column_index) and self.cells[row_index][column_index].has_mine:
                        count += 1
            self.cells[empty_row_index][empty_column_index].adjacent_mines_count = count

    def print(self):
        for row in self.cells:
            visible_row = [str(cell) for cell in row]
            print(visible_row)

    def is_cell_opened(self, row_index: int, column_index: int) -> bool:
        return self.cells[row_index][column_index].is_open

    def has_mine_at(self, coordinate: Coordinate) -> bool:
        return self.cells[coordinate.row][coordinate.column].has_mine



class Minesweeper:
    def __init__(self, width, height):
        self.grid = Grid(width, height)

    def _get_valid_coordinate(self, plane: str, max_index: int) -> int:
        prompt_str = "Enter zero-index {plane}-coordinate between 0 and {max_index}: "
        prompt = prompt_str.format(plane=plane, max_index=max_index)
        while True:
            try:
                coordinate = int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            else:

                if 0 <= coordinate <= max_index:
                    return coordinate
                else:
                    print(f"Invalid input. Please enter a number between 0 and {max_index}.")

    def _get_user_guess(self) -> Coordinate:
        while True:
            print("Try to guess a non-mine. I'll ask your x and y coordinates. 0, 0 at top left. "
                  "Positive #s to right and down.")

            # subtract by 1 b/c if grid width=4, then can index 0 to 3 inclusive
            max_row_index = self.grid.width-1
            max_col_index = self.grid.height-1

            # flips x,y human-readable coordinates to y,x as pythonic interpreted coordinates
            column_index = self._get_valid_coordinate(plane="x", max_index=max_row_index)
            row_index = self._get_valid_coordinate(plane="y", max_index=max_col_index)

            if self.grid.is_cell_opened(row_index=row_index, column_index=column_index):
                print("Invalid input. The cell is already opened. Please choose another cell.")
            else:
                return Coordinate(row_index, column_index)

    def _has_guessed_mine(self, user_coordinate_guess: Coordinate) -> bool:
        if self.grid.has_mine_at(user_coordinate_guess):
            print("You guessed a mine")
            return True
        else:
            return False

    def play(self):
        # while all non-mines are unopened
        while self.grid.has_unopened_non_mines():
            self.grid.print()
            user_coordinate_guess = self._get_user_guess()
            if self._has_guessed_mine(user_coordinate_guess):
                print("You lose")
                break
            else:
                # only reach here if guess is 1) valid coordinate, non-mine, unopened cell
                self.grid.cells[user_coordinate_guess.row][user_coordinate_guess.column].open()
        # if we reached here, we didn't hit a mine
        else:
            print("Hooray!! You won")
