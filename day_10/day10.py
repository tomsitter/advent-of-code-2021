import click
import numpy as np

   
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

    start = '{[<('
    end = '}]>)'

    segments = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }

    scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    scores2 = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    corrupted_segs = []
    part2_scores = []

    with open(filename, 'r') as infile:
        for row in infile:
            stack = []
            line = row.strip()
            is_corrupted = False
            for char in line:
                if char in segments.keys():
                    stack.append(char)
                else:
                    cur_segment = stack.pop()
                    if char != segments[cur_segment]:
                        corrupted_segs.append(char)
                        is_corrupted = True
                        break
            
            if not is_corrupted:
                # stack not corrupted, but is incomplete, calculate score for completing the line.
                remaining = [segments[c] for c in stack[::-1]]
                score = 0
                for c in remaining:
                    score *= 5
                    score += scores2[c]
                part2_scores.append(score)

        # Part 1
        score = sum(scores[seg] for seg in corrupted_segs)
        print(f'Part 1: {score}')

        # Part 2
        middle_index = int(len(part2_scores)/2)
        print(f'Part 2: {sorted(part2_scores)[middle_index]}')


if __name__ == '__main__':
    run()