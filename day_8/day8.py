import click

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

    count_1478 = 0
    total = 0

    with open(filename, 'r') as infile:
        for row in infile:
            signal_patterns, output_values = row.split("|")
            signal_patterns = [frozenset(s) for s in signal_patterns.split()]
            output_values = [frozenset(s) for s in output_values.split()]

            code = {}
            code[1] = [s for s in signal_patterns if len(s)==2][0]
            code[4] = [s for s in signal_patterns if len(s)==4][0]
            code[6] = [s for s in signal_patterns if len(s)==6 and not code[1] < s][0]
            code[5] = [s for s in signal_patterns if len(s)==5 and s < code[6]][0]
            code[7] = [s for s in signal_patterns if len(s)==3][0]
            code[8] = [s for s in signal_patterns if len(s)==7][0]
            code[9] = [s for s in signal_patterns if len(s)==6 and code[1] < s and code[4] < s][0]
            code[2] = [s for s in signal_patterns if len(s)==5 and not s < code[9]][0]
            code[3] = [s for s in signal_patterns if len(s)==5 and code[1] < s][0]
            code[0] = [s for s in signal_patterns if len(s)==6 and code[1] < s and not code[4] < s][0]

            # Part 1
            for entry in output_values:
                if any([entry==code[num] for num in (1,4,7,8)]):
                    count_1478 += 1

            # Part 2
            # invert code to get a decode matrix
            decode = {v: str(k) for k, v in code.items()}
            # decode values, join into one number and convert to int, add to the running total
            total += int(''.join(decode[entry] for entry in output_values))

        print(f'Solution 1: {count_1478}')
        print(f'Solution 2: {total}')

if __name__ == '__main__':
    run()