def string_to_lines(input_string):
    # Takes an input string, chops it into lines, removes any blank trailing lines
    lines = input_string.split('\n')
    return [line for line in lines if len(line) > 0]


def string_to_ints(input_string):
    # Takes an input string and, if all lines are integers, converts to integers
    lines = string_to_lines(input_string)
    try:
        return [int(line) for line in lines]
    except ValueError:
        print('Cannot convert input string to integers')