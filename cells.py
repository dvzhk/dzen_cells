import argparse
import sys
import numpy as np
import curses
import time


def check_size(m, n):
    """Проверка, что  M,N помещается в терминал"""
    stdscr = curses.initscr()
    height, width = stdscr.getmaxyx()

    curses.reset_shell_mode()

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
    # print("-----------------------------------")
    m, n = args.m, args.n
    checked_field = check_size(m, n)
    # print("+++++++++++++++++++++++++++++++++++++++")
    if checked_field == True:
        # print("checked_true!!!")
        return np.random.choice(2, size=(m, n))
    else:
        sys.exit(checked_field)


def loading_field(file):
    """Loading cell field from file. Assuming it is comma-separated array of ones and zeros"""

    field_from_file = np.loadtxt(file, dtype='int', delimiter=",")
    checked_field = check_size(field_from_file.shape)
    if checked_field:
        return field_from_file
    else:
        sys.exit(checked_field)


def parse_args(args):
    """Parsing arguments in command line"""
    parser = argparse.ArgumentParser(add_help=True, description='This is a program')
    subparser = parser.add_subparsers()

    random_parser = subparser.add_parser(
        'random',

        help='Random starting position.')

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
        '-from',
        # nargs='?',
        # action="store_true",
        # dest="from_file",
        # default=False,
        help='Read starting position from file.')

    file_parser.add_argument(
        # '-file',
        dest="file",
        action="store",
        help='File containing starting position of cells.')

    # random_parser.set_defaults(func=loading_field)

    return parser.parse_args(args)


def count_neighbors(field, i, j, m, n):
    """Count non-zero cell neighbors"""
    neighbors = 0

    for p in (-1, 0, 1):
        for q in (-1, 0, 1):
            # if p == 0 and q == 0:
            #    neighbors += 0

            if (i + p) >= 0 and (j + q) >= 0:
                try:
                    neighbors += field[i + p][j + q]
                except IndexError:
                    pass

    # print("neighbors:", neighbors, i , j)
    return neighbors


def transform_field(field):
    m, n = field.shape
    new_field = np.zeros(field.shape, dtype=int)
    for i in range(m):
        for j in range(n):
            cell_neighbors = count_neighbors(field, i, j, m, n)
            if field[i][j] == 0 and cell_neighbors == 3:
                new_field[i][j] = 1

            if field[i][j] == 1:
                if cell_neighbors < 3 or cell_neighbors > 4:
                    new_field[i][j] = 0

                elif cell_neighbors in (3, 4):
                    new_field[i][j] = 1
                    # print(field[i][j], new_field[i][j], i ,j, cell_neighbors)
    return new_field


def display():
    try:
        myscreen = curses.initscr()
        LogicLoop()
    finally:
        curses.endwin()


def main():
    params = parse_args(sys.argv[1:])

    field = params.func(params)
    print(field)
    for i in field:
        print(i)

    stdscr = curses.initscr()
    a = 0
    while 1:
        a += 1
        stdscr.refresh()
        curses.nl()
        field = transform_field(field)
        # display = np.array2string(field, max_line_width=field.shape[0], precision=None, suppress_small=None, separator='')
        # for i in range(field.shape[0]):
        #    stdscr.addstr(i, 0, (np.array2string(field[i], max_line_width=(field.shape[1]+2), separator='').replace('0','.')))
        # stdscr.addstr(i+1, 0, '')
        display_string = np.array2string(field, precision=None, suppress_small=None, separator='')

        stdscr.addstr(0, 0, display_string[1:-1])
        # stdscr.addstr(i+2, 0, str(a))
        # stdscr.addstr(i+3, 0, np.array2string(field, precision=None, suppress_small=None, separator=''))
        # print()
        # print(field)
        stdscr.addstr('')
        time.sleep(1)
    curses.reset_shell_mode()


if __name__ == '__main__':
    main()
