import click
from itertools import chain

@click.command()
@click.option('--example', is_flag=True, help='Run example input')
@click.option('--steps', default=4)
def run(example, steps):
    # Loads the data and runs the main algorithm
    if example:
        filename = 'example_input.txt'
        click.echo(f'Using example dataset: {filename}')
    else:
        filename = 'input.txt'
        click.echo(f'Using full dataset: {filename}')

    with open(filename, 'r') as infile:
        template = infile.readline().strip()
        _ = infile.readline()  # blank
        rules = {}

        for row in infile:
            match, replace = row.split(" -> ")
            rules[match] = replace.strip()

        print(template)
        # print(rules)

        for _ in range(steps):
            new_template = []
            for index in range(len(template) - 1):
                pair = template[index:index + 2]
                # print(pair)
                if pair in rules:
                    before, after = pair
                    insert = rules[pair]
                    new_template += [before + insert + after]
            template = merge_template(new_template)
            # print(f'{len(template)}: {template}')

        print(f'Solution 1 after {steps} steps: {difference(template)}')


def difference(template):
    chars = sorted(set(template), key=lambda x: template.count(x))
    most = chars[-1]
    least = chars[0]
    return template.count(most) - template.count(least)


def merge_template(new_template):
    return ''.join(chain(new_template[0], [p[1:] for p in new_template[1:]]))


if __name__ == '__main__':
    run()
