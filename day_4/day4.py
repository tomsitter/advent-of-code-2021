import numpy as np
from itertools import islice
import click

class Board:

    def __init__(self, grid):
        self.grid = grid
        self.matches = np.zeros((5,5)).astype(int)

    def mark_number(self, number: int):
        for i, row in enumerate(self.grid):
            for j, num in enumerate(row):
                if number == num:
                    self.matches[i, j] = 1
                    break
        
        return self.has_bingo()

    def has_bingo(self):
        return self.check_rows() or self.check_rows(direction='v')

    def score(self):
        m = self.matches
        return (self.grid * np.where((m==0)|(m==1), m^1, m)).sum()

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

def check_number(number, boards):
    for board in boards:
        winner = board.mark_number(number)
        if winner:
            print('Winner!')
            print(board)
            print(f'Score: {board.score()}, Number: {number}')
            print(f'Solution: {board.score()*number}')
            return True

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
        click.echo(draw_order)
        boards = []
        while True:
            raw_grid = list(islice(infile, 6))
            if not raw_grid:
                break
            assert(len(raw_grid) == 6)
            numbers = [row.strip().split() for row in raw_grid[1:]]
            grid = np.array(numbers).astype(int)
            boards.append(Board(grid))

        for number in draw_order:
            winner = check_number(number, boards)
            if winner:
                break
                
        print('Done')



if __name__ == '__main__':
    run()