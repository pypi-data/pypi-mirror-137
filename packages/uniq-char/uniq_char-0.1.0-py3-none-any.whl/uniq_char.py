from collections import Counter
from functools import lru_cache
import click


@lru_cache(maxsize=None)
def unique_characters(string: str):
    """Creates a list from string with unique characters by using Counter and then collect it by values = 1"""
    return list([k for k, v in Counter(string).items() if v == 1])


def result(case):
    """The function for mapping our case in main function and print it"""
    result = list(map(unique_characters, case))
    for i in range(len(result)):
        print('The quantity of unique characters in your string #', i + 1, ' are: ', len(result[i]), sep='')
    return len(result)

@click.command()
@click.option('--file', default=None)
@click.option('--string', type=str, default='')
def main(file=None, string=''):
    """Main function which depends from chosen option changes the input to unique characters func"""

    if file != None:
        with open(file, 'r') as f:
            case = f.readline().split()
            result(case)

    if file == None:
        case = string.split()
        result(case)


if __name__ == '__main__':
    main()
