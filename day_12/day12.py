import click
import numpy as np


class Maze:
    caves = {}

    def __init__(self):
        pass

    def add_path(self, path):
        cave_name, path = path.split('-')
        if cave_name in self.caves.keys():
            self.caves[cave_name].add_path(path)
        else:
            cave = Cave(cave_name)
            cave.add_path(path)
            self.caves[cave_name] = cave


class Cave:
    name = ''
    start = False
    end = False
    paths = []

    def __init__(self, name):
        self.name = name
        if name == 'start':
            self.start = True
        if name == 'end':
            self.end = True
        if name.isupper():
            self.size = 'large'
        else:
            self.size = 'small'

    def add_path(self, name):
        self.paths.append(name)

    def __str__(self):
        path_strings = ' '.join([p for p in self.paths])
        if self.start:
            return f"Start: {self.name}-{path_strings}"
        elif self.end:
            return f"{path_strings}-{self.name}: End"
        else:
            return f"{self.name}-{path_strings}"



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
        maze = Maze()
        for row in infile:
            maze.add_path(row)

    print(maze.caves['start'])


if __name__ == '__main__':
    run()
