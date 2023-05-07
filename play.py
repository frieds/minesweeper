from minesweeper import Minesweeper


def main():
    width = input("Enter integer value of width of cells: ")
    height = input("Enter integer value of height of cells: ")

    game = Minesweeper(width=int(width), height=int(height))
    game.play()


if __name__ == "__main__":
    main()
