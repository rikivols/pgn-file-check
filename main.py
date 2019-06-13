import click
import os
import glob
import check_tag_syntax
import check_move_syntax
import check_moves


def split_file_content(file):
    """
    Converts input file to an array, splits whole input file into tag section and move section.

    :param file: Opened input file.

    :return: tag_section - Array that contains tags.

    """

    tag_section = []
    move_section = []
    appending_to_tag = True

    for line in file:

        line = line.strip()

        if line.isspace() or line == '':
            continue

        if line[0] != '[' and line[-1] != ']':  # this is when tag section ends
            appending_to_tag = False

        if appending_to_tag:
            tag_section.append(line)
        else:
            move_section.append(line)

    return tag_section, move_section


def print_err_message(file, err_message):
    """
    Prints message if there is an error in input file.

    :param file: Input file name
    :param err_message: Message to be printed.
    :return: returns err_message to know if there is one.
    """

    if err_message:

        print(f"Error on file: {file}\n")
        print(err_message, '\n')

    return err_message


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--output', '-o', is_flag=True,
              help="[NOT YET IMPLEMENTED] (Processes all [INPUT_FILES] repairs files and gives output to "
                   "[OUTPUT_FILE].) ---- This option does nothing in this version")
@click.option('--check', '-c', is_flag=True,
              help="Checks all [INPUT_FILES], tells if the files are alright")
@click.argument('input_files', nargs=-1)
def main(output, check, input_files):
    """
    Checks all pgn files given in input, if there are any errors, gives a message. This program checks standard
    version of pgn. Program checks only syntax, does not check if the moves are playable [will be later].

    Right now program can only check files, it does not automatically repair them, so --output and --check will
    do the same. You can even call the program without them.

    If no [INPUT_FILES] given, program loads all files from input_files.
    """

    files_ok_arr = []
    files_err_arr = []

    if len(input_files) == 0:  # If input files not provided, gets all files from input_files
        input_files1 = glob.glob("./input_files/*.txt")
        input_files2 = glob.glob("./input_files/*.pgn")
        input_files = [i for i in input_files1 + input_files2 if i]

    for inp_file in input_files:

        if os.path.isfile(f'./input_files/{inp_file}'):
            inp_file = f'./input_files/{inp_file}'

        elif os.path.isfile(f'./{inp_file}'):
            inp_file = inp_file

        else:
            print(f"File {inp_file} not found.")
            continue

        with open(inp_file, 'r', encoding='utf-8') as file:
            tag_section, move_section = split_file_content(file)

        """    CHECKING TAGS     """

        result_tag, err_message = check_tag_syntax.check_tag_syntax(tag_section)

        if './input_files/' in inp_file:  # Get just the name of file not directory
            inp_file = inp_file.split('./input_files/')[1]

        if './input_files\\' in inp_file:  # Get just the name of file not directory
            inp_file = inp_file.split('./input_files\\')[1]

        if print_err_message(inp_file, err_message):
            files_err_arr.append(inp_file)
            continue

        """ -------------------- """

        print()

        """    CHECKING MOVES     """

        moves_arr, result_move, err_message = check_move_syntax.check_move_syntax_and_get_moves(move_section)

        if print_err_message(inp_file, err_message):
            files_err_arr.append(inp_file)
            continue

        """ -------------------- """

        """    CHECKING RESULT    """
        if result_tag != result_move:

            err_message = "Result from tag section does not match result from move section."
            print_err_message(inp_file, err_message)

        if err_message:
            files_err_arr.append(inp_file)
            continue

        """ ------------------- """

        files_ok_arr.append(inp_file)
        print(f"{inp_file} OK")  # File without errors.

    print("\n---------------------------\n")

    print(f"Files ok: {len(files_ok_arr)} / {len(files_ok_arr) + len(files_err_arr)}", files_ok_arr)
    print(f"Err files: {len(files_err_arr)} / {len(files_ok_arr) + len(files_err_arr)}", files_err_arr)


if __name__ == '__main__':

    main()
