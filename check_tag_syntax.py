"""
Gets called with array containing chess tag section. Tag section are all lines containing tags. Array passed will
already be without empty characters. Program checks format of those tags, and order. Program only checks nevessary
tags, ignores optional ones.

File is called with check_tag_syntax() function.

Returns match result - Results of a match collected in a tag Result.

If program finds errors in syntax of file, program ends and prints message explaining the error.
"""


def check_tag_name(row, tag_name, tag_order):
    """
    Checks tag name, the outside format of tag. In [Event "Ev"] -> name is Event.

    :param row: Current searched row from file.
    :param tag_name: Name of the tag, Event, Site, ECO...
    :param tag_order: Serves as stack, always last element is needed tag name.
    """

    err_message = ''

    # check if tags are rightly enclosed
    if row[0] != "[" or row[-1] != ']':
        err_message = raise_error(row, "bad enclosing of tag, missing '[' or ']'")
        return err_message

    if tag_order:
        if tag_name != tag_order[-1]:
            err_message = raise_error(row, "bad tag (should be:[" + tag_order[-1] + "])")
            return err_message

        if not tag_name[0].isupper():
            raise_error(row, "Tag should start with upper case")
            return err_message

    # check the start of inp_file_arr
    if len(tag_order) == 7:
        if row[:6] != '[Event':
            err_message = raise_error(row, "Syntax error: bad start of inp_file_arr (it should start "
                                           "with Event tag -> [Event)")
            return err_message

    return err_message


def is_date_tag_ok(tag_content):
    """
    Checks if date from date tag is okay.

    :param tag_content: What is inside quotes of tag.

    :return: True - Date form is correct.
             False - Date form is incorrect.
    """

    if tag_content[1:-1] != '??':
        try:
            year, month, day = tag_content[1:-1].split('.')

            if year != '????':
                if int(year) < 0 or int(year) > 10000:
                    return False
            if month != '??':
                if int(month) > 12 or len(month) <= 0:
                    return False
            if day != '??':
                if int(day) > 31 or int(day) < 1:
                    return False
        except ValueError:
            return False

    return True


def check_tag_content(row, tag_name, tag_content, tag_order, possible_results, match_result):
    """
    Checks if content inside " " of tag is right. Also gets result from result tag.

    :param row: Current searched row of file.
    :param tag_name: Name of the tag, Event, Site, ECO...
    :param tag_content: What is inside quotes of tag.
    :param tag_order: Serves as stack, always last element is needed tag name.
    :param possible_results: Array of possible results of match.
    :param match_result: Content of result tag (result of match).

    :return: match_result
             err_message - Message to be printed if error arises, else it is ''

    """

    err_message = ''

    try:
        if tag_content[0] != '"' or tag_content[-1] != '"':
            err_message = raise_error(row, 'wrong format / no quotes ("")')
            return '', err_message
    except IndexError:
        err_message = raise_error(row, 'wrong format of tag (no space)')
        return '', err_message

    if not tag_name:
        raise_error(row, "no tag")

    if tag_order:
        # checks date format
        if tag_order[-1] == "Date":

            if not is_date_tag_ok(tag_content):
                err_message = raise_error(row, "bad date format, should be YYYY.MM.DD")
                return '', err_message

        # check if there's correct match_result
        if tag_order[-1] == "Result":

            if tag_content[1:-1] not in possible_results:
                err_message = raise_error(row, "bad match_result (can be only '1-0', '0-1', '1/2-1/2', '*')")

            match_result = tag_content[1:-1]

    return match_result, err_message


def check_tag_syntax(tag_section):
    """
    Server as main function. Check if tags are okay, if not, ends with SynaxError and explanation.

    tag_section - array of all moves from tag section.

    Not checking optional tags (there are too many, every site has their own)
    note - Maybe later implement checking eco tag.

    returns:
    match_result - the match_result of game in tag Result.
    err_message - Message to be printed if error arises, else it is ''
    """

    # required tags: Event, Site, Date, Round, White, Black, Result -> in this order
    tag_order = ['Result', 'Black', 'White', 'Round', 'Date', 'Site', 'Event']  # this order is reversed for checking

    possible_results = ['1-0', '0-1', '1/2-1/2', '*']

    # the line from which we start counting tags (it's if there are \n characters in beginning)
    match_result = ''
    err_message = ''

    for row in tag_section:

        # check if we are still in tag section.
        if not tag_order:
            try:
                if row[0] != '[' and row[-1] != ']':
                    break

            except ValueError:
                err_message = raise_error(row, "Bad start of move section")
                return '', err_message

        # split to 2 parts without brackets []
        try:
            tag_name, tag_content = row[1:-1].split(' ', 1)
        except ValueError:
            err_message = raise_error(row, "Wrong tag.")
            return '', err_message

        err_message = check_tag_name(row, tag_name, tag_order)
        if err_message:
            return '', err_message

        match_result, err_message = check_tag_content(row, tag_name, tag_content, tag_order, possible_results,
                                                      match_result)
        if err_message:
            return '', err_message

        if tag_order:
            tag_order.pop()  # get rid of previous necessary tag

    if tag_order:
        err_message = raise_error('', 'No tags.')

    return match_result, err_message


def raise_error(row, message):
    """
    Raises syntax error, prints a message and row of file where the error showed up.

    :param row:
    :param message:
    :return:
    """

    return f"{row}\n^^^^^^^^\n{message}"
