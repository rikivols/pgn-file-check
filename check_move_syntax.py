"""
File is called with check_move_syntax_and_get_moves() function.

Gets called with array containing chess move section. It's the section not containing tags. Array passed will already
be without empty characters. If the move is in longer version and can be shorten without losing meaning, program shorts
it (ee4 -> e4). Program will not shorten move if it contains important information (Nef4 will not convert to Nf4).

Returns array containing moves. Those moves are later called in check_moves.py, which should check if the moves are
actually playable [Not yet implemented].

If program finds errors in syntax of file, program ends and prints message explaining the error. 
"""


class Move:
    """
    Accepts move on initialization, and saves shorter version of that move as variable move. If move doesn't make
    sense, saves '' as variable move.
    """

    __pieces = ['K', 'Q', 'R', 'B', 'N']
    __chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    __numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self, move):
        """
        Determines if given input is a move, tries to convert it to its simpliest form.

        :param move: Move from input that we are checking.
        """

        self.move = ''
        self.was_check = 0
        self.was_mate = 0
        self.pawn_promotion = ''

        """ HANDLE CHECKS AND MATES """

        # get rid of mate
        if len(move) >= 3 and move[-1] == '#':
            self.was_mate = 1
            move = move[:-1]

        # get rid of check +
        if len(move) >= 3 and move[-1] == '+':
            self.was_check = 1
            move = move[:-1]

        """ ---------------------- """

        """ DETERMINING IF PAWN OR PIECE MOVE, CALLING OF FUNCTIONS """
        if move:

            if move[0] in self.__chars:
                self.pawn_move(move)

            elif len(move) >= 3 and move[0] == 'P' and move[1] in self.__chars:
                self.pawn_move(move[1:])

            elif move[0] in self.__pieces:
                self.piece_move(move)

            elif move == 'O-O' or move == 'O-O-O':
                self.move = move

            self.append_check_or_mate()

        """ ------------------------------------------------------ """

    def pawn_move(self, move):
        """
        Checks if given pawn move is really a move, converts move to its simpliest form.

        :param move: Move from input that we are checking.
        :return: Updates self.move, if the move is not playable, leaves self.move as ''
        """

        # get rid of promoting =Q
        if len(move) >= 4 and move[-2] == '=' and move[-1] in self.__pieces:
            self.pawn_promotion = move[-2:]
            move = move[:-2]

        if move[-1] in self.__numbers:
            # e4
            if len(move) == 2:
                self.move = move

            # ee4 (get rid of first character)
            elif len(move) == 3:
                if move[0] == move[1]:
                    self.move = move[-2:]

            elif len(move) == 4:

                # full notation of pawn -> e2e3, e2e4... (get rid of first 2 characters)
                if move[0] == move[2] and move[1] in self.__numbers:

                    # e2e3 -> pawn moves by one square
                    if int(move[1]) + 1 == int(move[3]) or int(move[1]) - 1 == int(move[3]):
                        self.move = move[-2:]

                    # e2e4 -> white pawn moves by 2 squares
                    if move[1] == '2' and int(move[1]) + 2 == int(move[3]):
                        self.move = move[-2:]

                    # e7e5 -> black pawn moves by 2 squares
                    if move[1] == '7' and int(move[1]) - 2 == int(move[3]):
                        self.move = move[-2:]

                # pawn taking -> exf3
                if move[1] == 'x' and move[2] in self.__chars:
                    self.move = move

            elif len(move) == 5:

                # full notation of pawn with taking -> e2xf3 (get rid of second character)
                if move[1] in self.__numbers and move[2] == 'x':

                    # We are trying to get rid of second character, we have to check if it fits
                    if abs(int(move[1]) - int(move[4])) == 1:
                        self.move = move[0] + move[2:]

            if self.pawn_promotion:
                self.move += self.pawn_promotion
        else:
            self.move = ''

    def piece_move(self, move):
        """
        Checks if given piece move is really a move, converts move to its simpliest form.

        :param move: Move from input that we are checking.
        :return: Updates self.move, if the move is not playable, leaves self.move as ''
        """

        was_taking = 0

        if len(move) >= 4 and move[-3] == 'x':  # Easier to check without takings
            was_taking = 1
            move = move[:-3] + move[-2:]

        # every piece move must end with character and number (e4)
        if move[-2] in self.__chars and move[-1] in self.__numbers:

            if len(move) == 3:

                # Ne4 -> short notation
                self.move = move

            if len(move) == 4:

                # Nee4 / N3e4 -> semi-full notation, for identification of concrete piece
                if move[1] in self.__chars or move[1] in self.__numbers:
                    self.move = move

            if len(move) == 5:

                # Ne2e4 -> full notation
                if move[1] in self.__chars and move[2] in self.__numbers:
                    self.move = move

            if was_taking and self.move:
                self.move = self.move[:-2] + 'x' + self.move[-2:]

        else:
            self.move = ''

    def append_check_or_mate(self):
        """
        If there was check of mate, appends it to a move.

        :return: Updates self.move
        """

        if self.move:
            if self.was_check:
                self.move += '+'

            if self.was_mate:
                self.move += '#'


def is_match_result(element, last_el):
    """
    Checks if current element is correct result of match.

    :param element: Smallest part of input file, part separated by space
    :param last_el: Last element of input file, should contain result

    :return: Result of match, if there is no result, returns ''
    """

    match_result = ''
    err_message = ''

    if element == last_el:

        if element in ['1-0', '0-1', '1/2-1/2', '*']:

            try:
                match_result = last_el
            except ValueError:
                err_message = make_error_msg('', "Wrong result at the end of move section.")

    return match_result, err_message


def is_bracket_comment(inp_move, skip_turn):
    """
    Checks if the content of file is still inside brackets (is ignored)

    :param inp_move: Smallest part from input, we check if it is a '{' or '}'
    :param skip_turn: If element is inside of '{', we skip all other element.

    :return: Returns if we are still inside of bracket.
    """

    # HANDLING COMMENTS - comments are either enclosed in { } or they have ; which means comment is for whole row
    if inp_move != '':
        if inp_move[0] == '{':
            skip_turn = 1

        if inp_move[-1] == '}':
            skip_turn = 0

    return skip_turn


def check_move_number(move_num, correct_move_num):
    """
    Checks if number of move corresponds to actual number of move.

    :param move_num: Smallest part of input file, part separated by space.
    :param correct_move_num: What number should the element be (real move number).
    :return:
    """

    try:
        if int(move_num[:-1]) != correct_move_num:
            return f"Wrong number of move, should be {correct_move_num}"
    except ValueError:
        return "Should be number / bad form of element"

    if move_num[-1] != '.':
        return "missing dot '.' after number"


def check_move_syntax_and_get_moves(move_section):
    """
    checks if moves are okay, splits every row by space, the moves itself
    checks the function is_move

    :param move_section: Array of all lines of moves from move section of input file.

    :return move_arr - Array of just moves, that are shortened. [e4, e5...]
            match_result - Result of match, should be last element.
            err_message - Message to be printed if there is error, else returns ''
    """

    moves_arr = []
    correct_move_num = 1  # for checking chess moves, 1. 2.
    element_counter = 0  # To determine if element should be a nubmer (%3 == 0) or move.
    skip_turn = 0  # If we are inside of a bracket comment '{', we skip turns.
    match_result = ''
    err_message = ''
    last_el = move_section[-1].split()[-1]  # Last element of input file, should be game result.

    for row in move_section:

        for element in row.split():

            """     FORM     """

            if last_el == element:
                match_result, err_message = is_match_result(element, last_el)

            if err_message:
                return '', '', err_message

            if match_result:
                break

            if element[0] == ';':  # We are directly skipping row, everything after semicolon should be skipped
                break

            skip_turn = is_bracket_comment(element, skip_turn)  # we are in comment

            if skip_turn == 1 or element[-1] == '}':
                continue

            if element.isspace() or element == '':
                err_message = make_error_msg(row, "Too many spaces")
                return '', '', err_message

            """ ------------ """

            inp_move = element

            """   MOVE NUMBERS   """

            if element_counter % 3 == 0:  # It should be number of element

                if len(element) > 3:  # if element has more than 2 characters, it is treated as move without whitespace
                                      # 1.e4
                    try:
                        move_num, inp_move = element.split('.')
                    except ValueError:
                        return '', '', make_error_msg(row, "Missing dot")

                    move_num += '.'
                    element_counter += 1
                else:
                    move_num = element

                message = check_move_number(move_num, correct_move_num)

                if message:
                    err_message = make_error_msg(row, message)
                    return '', '', err_message

                correct_move_num += 1

            """ ---------------- """

            """       MOVES      """
            if element_counter % 3 != 0:
                final_move = Move(inp_move)
                if final_move.move:
                    moves_arr.append(final_move.move)
                else:
                    err_message = make_error_msg(row, f"bad element (move number {correct_move_num - 1})")
                    return '', '', err_message

            """ ---------------- """

            element_counter += 1

    return moves_arr, match_result, err_message


def make_error_msg(row, message):
    """
    Returns message if error in input file arises.

    :param row: Current row of file with error.
    :param message: Message to be returned.
    :return: Error message.
    """

    return f"{row}\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMove syntax error: {message}"
