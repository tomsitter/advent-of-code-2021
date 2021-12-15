import click
import numpy as np

def adjacent(pos, data):
    """Returns a list of adjacent values from the data matrix for the given position"""
    x,y = pos
    x_size, y_size = data.shape
    for (adj_x, adj_y) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if adj_x >= 0 and adj_x < x_size and adj_y >= 0 and adj_y < y_size:
            yield (adj_x, adj_y)

def find_basin(pos, data):
    """Similar to adjacent but yields starting point, and is recursive if adjacent point is > current point but < 9"""
    x,y = pos
    yield (x,y)
    x_size, y_size = data.shape
    for (adj_x, adj_y) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if adj_x >= 0 and adj_x < x_size and adj_y >= 0 and adj_y < y_size:
            adj_pt = data[adj_x][adj_y]
            if data[x][y] < adj_pt and adj_pt < 9:
                yield (adj_x, adj_y)
                yield from find_basin((adj_x, adj_y), data)

    
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
            data.append([num for num in row.strip()])
        data = np.array(data, dtype='int')

    low_points = []
    basins = []
    for x, row in enumerate(data):
        for y, point in enumerate(row):
            if all(point < data[adj_x, adj_y] for (adj_x, adj_y) in adjacent((x, y), data)):
                low_points.append(point)
            basins.append(list(find_basin((x,y), data)))

    # Part 1
    risk_levels = [1+point for point in low_points]
    print(f'Solution 1: {sum(risk_levels)}')

    # Part 2
    top_3 = sorted([set(b) for b in basins], key=len, reverse=True)[0:3]
    product = np.prod([len(t) for t in top_3])
    print(f'Solution 2: {product}')

if __name__ == '__main__':
    run()