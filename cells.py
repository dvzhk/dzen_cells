import argparse
import sys
import numpy as np
import subprocess
import time


def check_size(m, n):
    """Checking m,n is smaller than the size of terminal is"""

    if sys.platform.startswith('freebsd') or sys.platform == 'linux' or sys.platform == 'darwin':

        stty = subprocess.run(["stty", "size"], stdout=subprocess.PIPE)

        height, width = stty.stdout.strip().split(b' ')
        height, width = int(height), int(width)
    else:
        height, width = 25, 80

    warn = "Size of cell field bigger than terminal size. Can't display. Choose {} <= {}"

    if m <= 0 or n <= 0:
        return f"M,N must be > 0 and be smaller than terminal dimensions({height}x{width})"

    elif height < m:
        return warn.format("m", height)

    elif width < n:
        return warn.format("n", width)

    else:
        return True


def create_random_start(args):
    """Creating random field"""

    m, n = args.m, args.n
    checked_field = check_size(m, n)

    if checked_field == True:
        return np.random.choice(2, size=(m, n))

    else:
        sys.exit(checked_field)


def loading_field(args):
    """Loading cell field from file. Assuming it is comma-separated array of ones and zeros"""
    # print(file, type(file))
    field_from_file = np.loadtxt(args.file, dtype='int', delimiter=",")
    m, n = field_from_file.shape
    checked_field = check_size(m, n)

    if checked_field == True:
        return field_from_file
    else:
        sys.exit(checked_field)


def help_and_exit(args):
    args.hlp()
    sys.exit()


def parse_args(args):
    """Parsing arguments in command line"""

    parser = argparse.ArgumentParser(add_help=True, description='Calculating cells states')
    subparser = parser.add_subparsers(dest="command")

    random_parser = subparser.add_parser(
        'random',
        add_help=True,
        help='Random starting position.',
        conflict_handler='resolve')

    random_parser.add_argument(
        'm',
        action="store",
        type=int,
        default=0,
        help='Number of rows')

    random_parser.add_argument(
        'n',
        action="store",
        type=int,
        default=0,
        help='Number of columns')

    random_parser.set_defaults(func=create_random_start)

    file_parser = subparser.add_parser(
        'from',
        add_help=True,
        help='Read starting position from file.',
        conflict_handler='resolve')

    file_parser.add_argument(
        dest="file",
        action="store",
        help='File containing starting positions of cells. Input file should be simple comma-separated 2-d array of ones and zeros.')

    file_parser.set_defaults(func=loading_field)

    parser.set_defaults(func=help_and_exit, hlp=parser.print_help)
    return parser.parse_args(args)


def count_neighbors(field, i, j):
    """Count non-zero cell neighbors"""
    neighbors = 0

    for p in (-1, 0, 1):
        for q in (-1, 0, 1):
            if (i + p) >= 0 and (j + q) >= 0:
                try:
                    neighbors += field[i + p][j + q]
                except IndexError:
                    pass

    return neighbors


def transform_field(field):
    m, n = field.shape
    new_field = np.zeros(field.shape, dtype=int)
    for i in range(m):
        for j in range(n):
            cell_neighbors = count_neighbors(field, i, j)
            if field[i][j] == 0 and cell_neighbors == 3:
                new_field[i][j] = 1

            if field[i][j] == 1:
                if cell_neighbors < 3 or cell_neighbors > 4:
                    new_field[i][j] = 0

                elif cell_neighbors in (3, 4):
                    new_field[i][j] = 1

    return new_field


def display(field):
    # n = 0
    for i in field:
        # n += 1
        stroka = ''

        for j in i:
            stroka += 'X' if j == 1 else '.'
        print(stroka)
        # print(str(n) + '\t' + stroka)
    print()


def main():
    params = parse_args(sys.argv[1:])

    field = params.func(params)

    print("Start field of cells:")
    display(field)

    iteration = 0

    while True:

        iteration += 1
        field_new = transform_field(field)

        if (field == field_new).all():
            break
        else:
            field = field_new

        print(f"Iteration {iteration}:")
        display(field)

        time.sleep(1)


if __name__ == '__main__':
    main()
