import click
from collections import defaultdict

class School():
    def __init__(self, fish):
        self.school = defaultdict(int)
        for f in fish:
            self.school[f] += 1

    def __str__(self):
        all_fish = []
        for key in sorted(self.school.keys()):
            all_fish.extend([str(key)]*self.school[key])
        return ','.join(all_fish)

    def __len__(self):
        return sum(self.school.values())

    def step(self):
        new_school = defaultdict(int)
        for key in sorted(self.school.keys(), reverse=True):
            timer = key-1
            count = self.school[key]
            if (timer < 0):
                new_school[8] = count
                new_school[6] += count
            else:
                new_school[timer] = count

        self.school = new_school

@click.command()
@click.option('--example', is_flag=True, help='Run example input')
@click.option('--days', help='Number of days to run simulation', default=18)
def run(example, days):
    # Loads the data and runs the main algorithm
    click.echo(f'example: {example}')
    if example:
        filename = 'example_input.txt'
    else:
        filename = 'input.txt'

    with open(filename, 'r') as infile:
        fish = list(map(int, infile.readline().strip().split(",")))
        school = School(fish)
        
        for _ in range(days):
            school.step()

        print(len(school))  


if __name__ == '__main__':
    run()