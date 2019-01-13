import sys

def check(inp_file):

    file = open(inp_file, 'r', encoding='utf-8')

    # checking the notation
    last_line = check_tags(file)

    # checking the moves
    check_moves(file, last_line)

    file.close()

def check_tags(file):

    '''
    required tags: Event, Site, Date, Round, White, Black, Result
                   -> in this order
    '''
    tag_order = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result']
    possible_results = ['1-0', '0-1', '1/2-1/2', '*']
    last_line = ''

    # the line now
    line = 0

    for row in file:

        # ignore new lines
        if row == '\n':
            continue

        row = row.rstrip("\n\r")
        # check the start of file
        if line == 0:
            if row[:6] != '[Event':
                raise_error(row, """Syntax error: bad start of file (it should start
                          with Event tag -> [Event)""")

        # check if we're still at tags section
        if row[0] == "[":
            # check if it's right tag (from tag_order)
            if row[-1:] != ']':
                raise_error(row, "no enclosing of tag")

            # split to 2 parts without brackets []
            row_split = row[1:-1].split(' ', 1)
            # row_split[0] -> tag
            # row_split[1] -> content

            if row_split[1][0] != '"' or row_split[1][-1] != '"':
                raise_error(row, 'wrong format / no quotes ("")')

            if not row_split[0] or not row_split[1][1:-1]:
                raise_error(row, "no tag / not enough content in tag")

            if not row_split[0][0].isupper():
                raise_error(row, "Tag should start with upper case")
            # check if needed tags are present
            if line < 7:
                if row_split[0] != tag_order[line]:
                    raise_error(row, "bad tag (should be:[" + tag_order[line] + "])")

            # check if there's correct result
            if line == 6:
                if row_split[1][1:-1] not in possible_results:
                    raise_error(row, "bad result (can be only 1-0 0-1 1/2-1/2 *)")

        else:
            # save last line (it has already moves)
            last_line = row
            # go to moves
            print("tags ok")
            return last_line

        line += 1

def check_moves(file, prev_line):

    if prev_line[:3] != '1. ':
        raise_error(prev_line, """Bad start of first move (should start with 1. )""")
    for row in file:
        pass

def raise_error(row, message):
    print(row)
    print("^^^^^^^^")
    # kill program
    sys.exit(message)

# testing
check('file.txt')