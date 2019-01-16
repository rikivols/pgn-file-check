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

        # get rid of space in the start or end
        if row[0] == ' ':
            row = row[1:]
        if row[-1] == ' ':
            row = row[:-1]


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


def check_moves(file, prev_line, result):
    """
    file - the whole file
    last - the index of row of file when tags have ended
    result - the result of game in tag Result

    checks if moves are okay, splits every move into function is_move, if it
    can't split (too many spaces, not real move...), it ends with error and
    explanation

    prints - "moves ok" if everything is correct
    """

    half_move = 0
    correct_move_num = 1
    was_result = 0 # checks if result was already between moves

    for line, row in enumerate(file[prev_line:]):

        if row == '':
            continue

        if result in row:
            # get rid of result in the last move to check it
            row = row.replace(result, '', 1)
            # if there was checkmate
            row = row.replace('#', '', 1)
            was_result = 1

        # get rid of space in the start or end
        if row[0] == ' ':
            row = row[1:]
        if row[-1] == ' ':
            row = row[:-1]

        row += ' '

        # ignore new lines
        if line == 0 and row[:3] != '1. ':
            raise_error(row, """Bad start of first move (should start with 1. )""")

        k = 0  # index of previous start of move
        s = 0  # get correct slice of number if the move number had more digits
        is_comment = 0

        row.rstrip()

        # if it's half move without number
        if not row[0].isdigit():
            for i in range(len(row)):
                if row[i] == ' ':
                    half_move = is_move(row[0:i+1], half_move = half_move)
                    break

        # send each move to is_move to validate
        for i in range(len(row)-1):

            # command is to the end of the line, there are no more moves
            if row[i+1] == ';':
                continue
            # every move has number and dot after
            while row[i].isdigit():
                if row[i+1] == '.':
                    # avoid empty strings
                    if row[k-s:i-s] != '':
                        half_move = is_move(row[k-s:i-s], correct_move_num, half_move)
                        correct_move_num += 1

                    k = i
                    s = 0
                    break
                elif row[i+1].isdigit():
                    i += 1
                    s += 1
                else:
                    break

            # add last move
            if i == len(row) - 2:
                half_move = is_move(row[k-1:i+1] + row[-1], correct_move_num, half_move)
                correct_move_num += 1

        if is_comment == 1:
            raise_error(row, "comment with no ending")
            '''
            Divide whole row by each move, and validate individual parts till number
            by check_move
            '''
    if was_result == 0:
        raise_error(row, "no result at the end of moves")

    print("moves ok")


def is_move(move, n=-1, half_move=0):
    """
    move - chess move with number and space in the end e.g ('1. e4 e5 ')
    n - correct number of move (if it's halfmove, n=-1)
    half_move - checks if we can have halfmove without a number ('Ne4 '),
                we can have only if previous move was halfmove with number
                (1. e4)
                two states - 1 - can be there half_move, 0 - can't

    checks if the move is correct, pushes only the submove part ('Ne4') into
    is_submove to check if the form is correct. If the form of move is
    incorrect, ends with error explaining the mistake.

    return half_move - if currect move was half move ('Ne4 ')
    """

    is_comment = 0

    # delete first space
    if move[0] == ' ':
        move = move[1:]

    # if there are more spaces at start
    if move[0] == ' ':
        raise_error(move, "no space")


    # normal move
    if move[0].isdigit():
        space_counter = 0
        index_of_dot = move.index('.')
        if str(n) != move[0:index_of_dot]:
            raise_error(move, f"wrong number of move, should be {n}")

        # skip the number
        if move[index_of_dot + 1] != ' ':
            raise_error(move, "no space")

        k = index_of_dot + 2
        for i in range(index_of_dot + 2, len(move)):
            if move[i] == '{':
                is_comment = 1
            if move[i] == ' ':
                space_counter += 1
            if move[i] == '\n':
                space_counter += 2

            if is_comment == 0:
                if move[i] == ' ' or move[i] == '\n':
                    # we don't want index error
                    if i+1 < len(move):
                        if move[i+1] == ' ':
                            raise_error(move, "too many spaces")
                    if is_submove(move[k:i]) == False:
                        raise_error(move, "bad submove")
                    k = i + 1

            if move[i-1] == '}':
                is_comment = 0

        if space_counter < 2:
            half_move = 1
    else:
        if half_move == 0:
            raise_error(move, "bad move")

        if is_submove(move[:-1]) == False:
            raise_error(move, "bad submove")

    if is_comment == 1:
        raise_error(move, "comment has no ending {")

    return half_move


def is_submove(m):
    """
    m - submove ('Ne4')

    Checks if the form of submove is correct.

    returns True / False
    """

    pieces = ['K', 'Q', 'R', 'B', 'N']
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

    try:
        if m[-1] == '+':
            m = m[:-1]
    except IndexError:
        raise_error(m, "bad move (probably too many spaces)")

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
    print(repr(row))
    print("^^^^^^^^")
    # kill program
    sys.exit(message)

# testing
check('file.txt')
