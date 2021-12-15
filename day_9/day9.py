import click
import numpy as np

def adjacent(pos, data):
    """Returns a list of adjacent values from the data matrix for the given position"""
    x,y = pos
    for (adj_x, adj_y) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        try:
            if adj_x >= 0 and adj_y >= 0:
                yield data[adj_x][adj_y]
        except IndexError:
            pass
    
@click.command()
@click.option('--example', is_flag=True, help='Run example input')
def run(example):
    # Loads the data and runs the main algorithm
    if example:
        filename = 'example_input.txt'
        click.echo(f'Using example dataset: {filename}')
    else:
        filename = 'input.txt'
        click.echo(f'Using full dataset: {filename}')

    with open(filename, 'r') as infile:
        data = []
        for row in infile:
            data.append([int(num) for num in row.strip()])

        list(adjacent((2, 2), data))

        #data = np.array(data, dtype='int') 
        low_points = []
        for x, row in enumerate(data):
            for y, point in enumerate(row):
                if all(point < adj_point for adj_point in adjacent((x, y), data)):
                    low_points.append(point)

        risk_levels = [1+point for point in low_points]

        print(f'Solution 1: {sum(risk_levels)}')

if __name__ == '__main__':
    run()