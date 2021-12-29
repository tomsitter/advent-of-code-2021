import click
from collections import defaultdict


class Maze:
    caves = defaultdict(list)

    def __init__(self):
        pass

    def add_path(self, path):
        start, end = path.split('-')
        self.caves[start].append(end)
        self.caves[end].append(start)

    def find_all_paths(self,
                       start: str = 'start',
                       end: str = 'end',
                       path: list = None,
                       can_revisit_small_cave: bool = False):
        if path is None:
            path = []

        path = path + [start]
        if start == end:
            return [path]

        if start not in self.caves:
            return []

        # print(f'Path is {path} and can revisit is {can_revisit_small_cave}')
        paths = []
        for node in self.caves[start]:
            can_visit = True
            can_revisit_small_cave_after_node = can_revisit_small_cave
            if node.islower() and node in path:
                if node in ('start', 'end'):
                    can_visit = False
                elif not can_revisit_small_cave:
                    can_visit = False
                else:
                    can_revisit_small_cave_after_node = False
                    can_visit = True

            if can_visit:
                new_paths = self.find_all_paths(node, end, path, can_revisit_small_cave=can_revisit_small_cave_after_node)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths


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
            maze.add_path(row.strip())

    # print(maze.caves)
    paths = maze.find_all_paths(can_revisit_small_cave=False)
    print(f'Found {len(paths)} paths')

    paths_pt2 = maze.find_all_paths(can_revisit_small_cave=True)
    print(f'Found {len(paths_pt2)} paths with one small cave revisit')
    # for p in sorted(paths_pt2): print(','.join(p))


if __name__ == '__main__':
    run()
