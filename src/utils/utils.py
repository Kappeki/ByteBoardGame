from . import fcolors


def add_tuples(tuple1, tuple2):
    return tuple(a + b for a, b in zip(tuple1, tuple2))

def print_score(human_points, computer_points):
    print(f'{fcolors.OKGREEN}############################')
    print(f'### Human: {human_points} Computer: {computer_points} ###')
    print(f'############################{fcolors.ENDC}')

def print_error(text):
    print(f'{fcolors.FAIL}{text}{fcolors.ENDC}')

def print_warning(text):
    print(f'{fcolors.WARNING}{text}{fcolors.ENDC}')

def print_green(text):
    print(f'{fcolors.OKGREEN}{text}{fcolors.ENDC}')