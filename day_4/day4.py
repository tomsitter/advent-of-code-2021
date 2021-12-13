import numpy as np
from itertools import islice
import click

class Board:

    def __init__(self, grid, size=5):
        self.grid = grid
        self.size = size
        self.matches = np.zeros((size, size)).astype(int)
        self.has_bingo = False

    def mark_number(self, number: int):
        found = np.array((self.grid == number).astype(int))
        self.matches = self.matches + found
        self.check_bingo()
        
    def check_bingo(self):
        self.has_bingo = self.check_rows() or self.check_rows(direction='v')
    
    def reset(self):
        self.matches =np.zeros((self.size, self.size)).astype(int)

    def score(self):
        m = self.matches
        return (self.grid * np.where(m==1, 0, 1)).sum()

    def check_rows(self, direction='h'):
        if direction == 'v':
            _matches = np.transpose(self.matches)
        else:
            _matches = self.matches

        for row in _matches:
            if row.sum() == 5:
                return True
        return False

    def __str__(self, grid=None):
        if grid is None:
            grid = self.grid
        return '\n'.join("{:<5}{:<5}{:<5}{:<5}{:<5}".format(*row) for row in grid)

    def print_matches(self):
        print(self.__str__(self.matches))
    
    def print_board(self):
        print(self.__str__(self.grid))


def all_boards_win(boards):
    return all(board.has_bingo for board in boards)


def find_first_winner(numbers, boards):
    for number in numbers:
        for board in boards:
            board.mark_number(number)
            if board.has_bingo:
                return number, board
    return False, []

def find_last_winner(numbers, boards):
    for number in numbers:
        for board in boards:
            board.mark_number(number)
            if all_boards_win(boards):
                # this board is the last winner
                return number, board
    return False, []


@click.command()
@click.option('--example', is_flag=True, help='Run example input')
def run(example):
    # 
    click.echo(f'example: {example}')
    #example = True
    if example:
        filename = 'example_input.txt'
    else:
        filename = 'input.txt'

    with open(filename, 'r') as infile:
        draw_order = list(map(int, infile.readline().strip().split(",")))
        boards = []
        while True:
            raw_grid = list(islice(infile, 6))
            if not raw_grid:
                break
            assert(len(raw_grid) == 6)
            numbers = [row.strip().split() for row in raw_grid[1:]]
            grid = np.array(numbers).astype(int)
            boards.append(Board(grid))

        number, board = find_first_winner(draw_order, boards)
        print('Found first winner!')
        print(board)
        print(f'Score: {board.score()}, Number: {number}')
        print(f'Solution: {board.score()*number}')

        for board in boards:
            board.reset()
        
        number, board = find_last_winner(draw_order, boards)
        print('Found last winner!')
        print(board)
        print(f'Score: {board.score()}, Number: {number}')
        print(f'Solution: {board.score()*number}')

        print('Done')



if __name__ == '__main__':
    run()