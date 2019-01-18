import sys

def check(inp_file):
    '''
    main function that trigger every other.

    inp_file - name of file in our directory we want to check

    returns tags ok and moves ok or ends with error and explanation
    '''

    file = open(inp_file, 'r', encoding='utf-8').read()
    file = file.split('\n')

    # checking the notation
    last, result = check_tags(file)

    # checking the moves
    check_moves(file, last, result)


def check_tags(file):
    """
    Check if tags are okay, if not, ends with error and explanation

    file - the whole file

    not checking optional ones (there are too many, every site has their own)
    note - maybe later implement checking date tag

    returns:
    last - the index of row of file when tags have ended
    result - the result of game in tag Result
    """

    # required tags: Event, Site, Date, Round, White, Black, Result
    # -> in this order
    tag_order = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result']

    possible_results = ['1-0', '0-1', '1/2-1/2', '*']

    # the line from which we start counting tags (it's if there are \n
    # characters in beginning)
    tag_line = 0

    for line, row in enumerate(file):

        if row == '':
            continue

        row = row.strip()

        # check the start of file
        if tag_line == 0:
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

            try:
                if row_split[1][0] != '"' or row_split[1][-1] != '"':
                    raise_error(row, 'wrong format / no quotes ("")')
            except IndexError:
                raise_error(row, 'wrong format of tag (no space)')

            if not row_split[0] or not row_split[1][1:-1]:
                raise_error(row, "no tag / not enough content in tag")

            if not row_split[0][0].isupper():
                raise_error(row, "Tag should start with upper case")
            # check if needed tags are present
            if tag_line < 7:
                if row_split[0] != tag_order[tag_line]:
                    raise_error(row, "bad tag (should be:[" + tag_order[tag_line] + "])")

            # checks date format
            if tag_line == 2:
                if row_split[1][1:-1] != '??':
                    try:
                        year, month, day = row_split[1][1:-1].split('.')
                        if len(year) != 4 or int(year) == False:
                            raise_error(row, "bad date format, should be YYYY.MM.DD")
                        if int(month) > 12 or len(month) != 2:
                            raise_error(row, "bad date format, should be YYYY.MM.DD")
                        if int(day) > 31:
                            raise_error(row, "bad date format, should be YYYY.MM.DD")
                    except ValueError:
                        raise_error(row, "bad date format, should be YYYY.MM.DD")

            # check if there's correct result
            if tag_line == 6:
                if row_split[1][1:-1] not in possible_results:
                    raise_error(row, "bad result (can be only 1-0 0-1 1/2-1/2 *)")
                result = row_split[1][1:-1]
            tag_line += 1
        else:
            # save last line (it has already moves)
            # go to moves
            print("tags ok")
            return line, result


def check_moves(file, last, result):
    """
    file - the whole file
    last - the index of row of file when tags have ended
    result - the result of game in tag Result

    checks if moves are okay, splits every row by space, the moves itself
    checks the function is_move

    prints - "moves ok" if everything is correct
    """
    moves_arr = []

    """
    SPLITTING MOVES INTO ARRAY BY SPACE
    """
    for row in file[last:]:

        row = row.rstrip()
        if row == '':
            continue

        if row[:-1] == ' ':
            row = row[:-1]

        moves_arr += row.split(" ") + ['\n']  # to know where line ended

    """
    CHECKING THE MOVES
    """
    correct_move_num = 1
    move_index = 0
    is_bracket_comment = 0
    is_dot_comment = 0

    for index, value in enumerate(moves_arr[:-3]):

        # HANDLING COMMENTS
        if value != '':
            if value[0] == '{':
                is_bracket_comment = 1

            if value[-1] == '}':
                is_bracket_comment = 0
                continue

        if is_bracket_comment == 1:
            continue

        if value != '':
            if value[0] == ';':
                is_dot_comment = 1

            if value == '\n':
                is_dot_comment = 0
                continue

        if is_dot_comment == 1:
            continue


        # handling too many spaces
        if value == '':
            raise_error(-1, f"too many spaces on move {correct_move_num-1}")

        if move_index % 3 == 0:  # It should be number of move
            try:
                if int(value[:-1]) != correct_move_num:
                    raise_error(value, f"""wrong number of move, should
                                           be {correct_move_num}""")
            except ValueError:
                raise_error(value, "Should be number / bad form of move")

            if value[-1] != '.':
                raise_error(value, f"missing dot '.'")
            correct_move_num += 1
            move_index += 1
        else:
            if is_move(value) == False:
                raise_error(value, f"bad move (move {correct_move_num-1})")

            move_index += 1

    # handling mate (#)
    if moves_arr[-3][-1] == '#':
        if is_move(moves_arr[-3][:-1]) == False:
            raise_error(moves_arr[-3], f"bad move (move {correct_move_num-1})")
    else:
        if is_move(moves_arr[-3]) == False:
            raise_error(moves_arr[-3], f"bad move (move {correct_move_num-1})")

    if moves_arr[-2] != result:
        raise_error(moves_arr[-2], "bad result / no result")

    print("moves ok")

def is_move(m):
    """
    m - move ('Ne4')

    Checks if the form of submove is correct.

    returns True / False
    """

    pieces = ['K', 'Q', 'R', 'B', 'N']
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

    if m[-1] == '+':
        m = m[:-1]

    # taking
    if len(m) >= 3:
        if m[-3] == 'x':
            m = m[:-3] + m[-2:]

    if len(m) == 2:
        # e4
        if m[0] in chars and m[1] in numbers:
            return True
    elif len(m) == 3:
        # Ne4 or ee4
        if m[0] in pieces or m[0] in chars and m[1] in chars and m[2] in numbers:
            return True
    elif len(m) == 4:
        # Nee4 or N3e4
        if m[0] in pieces:
            if m[1] in chars or m[1] in numbers and m[2] in chars and m[3] in numbers:
                return True
        # e2e4
        if m[0] in chars and m[1] in numbers and m[2] in chars and m[3] in numbers:
            return True

        # pawn queens e8=Q
        if m[0] in chars and m[1] in ['1', '8'] and m[2] == '=' and m[3] in pieces:
            return True
    elif len(m) == 5:
        # Ne2f4
        if m[0] in pieces and m[1] in chars and m[2] in numbers and m[3] in chars and m[4] in numbers:
            return True
        # pawn queens ee8=Q
        if m[0] in chars and m[1] in chars and m[2] in ['1', '8'] and m[3] == '=' and m[4] in pieces:
            return True
    elif len(m) == 6:
        # pawn queens e7e8=R
        if m[0] in chars and m[1] in ['2', '7'] and m[2] in chars and m[3] in ['1', '8'] and m[4] == '=' and m[5] in pieces:
            return True

    # castles
    if m == 'O-O' or m == 'O-O-O':
        return True

    return False

def raise_error(row, message):
    if row != -1:
        print(repr(row))
        print("^^^^^^^^")
    # kill program
    sys.exit(f"Syntax error: {message}")

# run the check function
if __name__ == '__main__':
    check(sys.argv[1])
