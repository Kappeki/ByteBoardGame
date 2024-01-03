from . import fcolors


def final_stack(board_dict):
    stack_count = 0
    for stack in board_dict.values():
        if stack:  # Check if there is a stack on this tile
            stack_count += 1
            if stack_count > 1 or len(stack) != 8:
                # If there is more than one stack, or this stack is not 8 tokens high
                return False
    # If we only found one stack and it was 8 tokens high
    return stack_count == 1

def add_tuples(tuple1, tuple2):
    return tuple(a + b for a, b in zip(tuple1, tuple2))

def lighten_color(color_tuple):
    return tuple(min(chanel + 20, 255) for chanel in color_tuple)

def print_score(white_points, black_points):
    print(f'{fcolors.OKGREEN}############################')
    print(f'### White: {white_points} Black: {black_points} ###')
    print(f'############################{fcolors.ENDC}')

def print_error(text):
    print(f'{fcolors.FAIL}{text}{fcolors.ENDC}')

def print_warning(text):
    print(f'{fcolors.WARNING}{text}{fcolors.ENDC}')

def print_green(text):
    print(f'{fcolors.OKGREEN}{text}{fcolors.ENDC}')