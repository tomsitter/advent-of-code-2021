import numpy as np
import sys
import click

class Grid:
    def __init__(self, height, width):
        self.grid = np.zeros((height, width))

    def add_ridge(self, ridge):
        #start, stop = ridge
        ys, xs = ridge
        if xs[0]==xs[1]:
            # horizontal
            self.grid[xs[0], min(ys):max(ys)+1] += 1
        elif ys[0] == ys[1]:
            # vertical
            self.grid[min(xs):max(xs)+1, ys[0]] += 1
        else:
            # diagonal at 45 deg
            xstep = 1 if xs[0] < xs[1] else -1
            ystep = 1 if ys[0] < ys[1] else -1
            for x,y in zip(range(xs[0], xs[1]+xstep, xstep), range(ys[0], ys[1]+ystep, ystep)):
                self.grid[x,y] += 1
        
    def count_overlaps(self):
        return np.where(self.grid>1, 1, 0).sum()


@click.command()
@click.option('--example', is_flag=True, help='Run example input')
def run(example):

    if example:
        filename = 'example_input.txt'
    else:
        filename = 'input.txt'

    with open(filename, 'r') as infile:
        height = 0
        width = 0
        ridges = []
        for row in infile:
            start, stop = [tuple(int(c) for c in coord.split(',')) for coord in row.split('->')]
            #ridges.append((start, stop))

            # Work out the dimensions of the grid by finding largest x,y coordinates
            xs, ys = zip(start, stop)
            ridges.append((xs, ys))
            height = max((height, *xs))
            width = max((width, *ys))

        grid = Grid(height+2, width+2)

        for ridge in ridges:
            grid.add_ridge(ridge)

        #print(ridges[0])
        #grid.add_ridge(ridges[0])
        print('Done!')
        print(grid.count_overlaps())




if __name__ == '__main__':
    run()