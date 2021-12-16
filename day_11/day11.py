import click
import numpy as np

class Octopus:
    flashing = False

    def __init__(self, energy):
        self.energy = energy
    
    def step(self):
        self.energy += 1
        if self.energy > 9:
            if not self.flashing:
                self.flashing = True
                return True
            return False

    def reset(self):
        if self.energy > 9:
            self.energy = 0
        self.flashing=False

    def __str__(self):
        if self.flashing: return '*'
        return str(self.energy)

def flash_adjacent(pos, data):
    adj_octos_pos = adjacent(pos, data)
    for octo_pos in adj_octos_pos:
        x,y = octo_pos
        octo = data[x][y]
        if octo.step():
            flash_adjacent(octo_pos, data)

        
def adjacent(pos, data):
    """Returns a list of adjacent values from the data matrix for the given position"""
    x,y = pos
    x_size, y_size = data.shape
    for (adj_x, adj_y) in [(x-1, y-1), (x-1, y), (x+1, y-1), (x+1, y), 
                           (x,   y-1), (x, y+1), (x-1, y+1),  (x+1, y+1)]:
        if 0 <= adj_x < x_size and 0 <= adj_y < y_size:
            yield (adj_x, adj_y)

def step(data):
    flashing = []
    for x, row in enumerate(data):
        for y, octo in enumerate(row):
            if octo.step():
                flashing.append((x,y))

    for octo_pos in flashing:
        flash_adjacent(octo_pos, data)

def reset(data):
    for row in data:
        for octo in row:
            octo.reset()

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
            data.append([Octopus(int(e)) for e in row.strip()])

        data = np.array(data)
        num_flashes = 0
        for _ in range(100):
            #for row in data:
            #    print(''.join([str(octo) for octo in row]))
            step(data)
            #print(data)
            for row in data:
                for octo in row:
                    if octo.flashing:
                        num_flashes +=1      
            print(f'Flashing: {num_flashes}')
            reset(data)
        

if __name__ == '__main__':
    run()