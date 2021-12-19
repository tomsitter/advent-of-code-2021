import click
import numpy as np

def foldud(pos: int, data):
    top, btm = data[:pos], np.flipud(data[pos+1:])
    top_ht = top.shape[0]
    btm_ht = btm.shape[0]
    
    # if fold was asymettrical, pad either top or bottom to make them same size
    if top_ht < btm_ht:
        top = pad_side(top, bottom=btm_ht-top_ht)
    elif top_ht > btm_ht:
        btm = pad_side(btm, top=top_ht-btm_ht)

    return np.logical_or(top, btm)

def foldlr(pos: int, data):
    left, right = data[:, :pos], np.fliplr(data[:, pos+1:])
    left_width = left.shape[1]
    right_width = right.shape[1]
    if left_width < right_width:
        left = pad_side(left, left=right_width-left_width)
    elif left_width > right_width:
        right = pad_side(right, left=left_width-right_width) 
        
    return np.logical_or(left, right)

def pad_side(matrix, top:int=0, bottom:int=0, left:int=0, right:int=0):
    padding = [(top, bottom), (left, right)]
    return np.pad(matrix, padding, mode='constant', constant_values=False)

def display(data):
    for row in data:
        v = ''.join(['#' if d else '.' for d in row])
        print(v)

@click.command()
@click.option('--example', is_flag=True, help='Run example input')
def run(example):
    # Loads the data and runs the main algorithm
    if example:
        filename = 'example_input.txt'
        click.echo(f'Using example dataset: {filename}')
        data = np.zeros((15, 11), dtype=bool)
    else:
        filename = 'input.txt'
        click.echo(f'Using full dataset: {filename}')
        data = np.zeros((895, 1310), dtype=bool)

    with open(filename, 'r') as infile:
        folds = 0
        print(data.shape)
        for row in infile:
            if row[0].isdigit():
                y, x = row.strip().split(",")
                data[int(x), int(y)] = True
            
            if row.startswith('fold'):
                direction, pos = row.strip().split()[2].split("=")
                if direction=='x':
                    data = foldlr(int(pos), data)
                else:
                    data = foldud(int(pos), data)
                
                if example:
                    display(data)
                folds += 1
                print(f'Fold {folds}: {np.sum(data)} dots')
        display(data)


if __name__ == '__main__':
    run()
