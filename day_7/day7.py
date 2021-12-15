import click

def apply_scale(steps):
    return int(steps + (steps*(steps-1))/2)

def cost(positions, pivot, scale=False):
    if scale:
        return sum(apply_scale(abs(p-pivot)) for p in positions)
    else:
        return sum(abs(p-pivot) for p in positions)   


@click.command()
@click.option('--example', is_flag=True, help='Run example input')
@click.option('--scale', is_flag=True, help='Run with scaling of steps (part 2)')
def run(example, scale):
    # Loads the data and runs the main algorithm
    click.echo(f'example: {example}')
    if example:
        filename = 'example_input.txt'
    else:
        filename = 'input.txt'

    with open(filename, 'r') as infile:
        best_loss = float('inf')
        
        positions = list(map(int, infile.readline().split(',')))

        for pivot in range(min(positions), max(positions)):
            loss = cost(positions, pivot, scale=scale)

            if abs(loss) < abs(best_loss):
                best_loss = loss
                best_pivot = pivot

        print(f'Best position found at {best_pivot} with cost {best_loss}')





if __name__ == '__main__':
    run()