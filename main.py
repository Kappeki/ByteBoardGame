import pygame
from GUI import GUI
from Board import Board
from utils import get_clicked_tile_position, print_score
from color import fcolors


def start_game(board_size, first_player):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    if first_player in ['h', 'H']:
        pygame.display.set_caption('Byte - HUMAN TURN (white)')
    else:
        pygame.display.set_caption('Byte - COMPUTER TURN (black) ')

    running = True

    gui = GUI(screen)
    tile_size = screen.get_height() // board_size
    board = Board(board_size, tile_size, first_player)
    board.initialize_board()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    board.highlight_clicked_token(x, y)
                elif event.button == 3:
                    x, y = event.pos
                    row, column = get_clicked_tile_position(x, y, board_size, tile_size)
                    is_winning_move = board.move_stack(row, column)
                    if is_winning_move:
                        print('Human won!') if board.human_points > board.computer_points else print('Computer won!')
                        print_score(board.human_points, board.computer_points)
                        running = False

        gui.draw_board(board)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    # board_size = int(input('Input board size: '))
    board_size = 8
    while board_size not in [8, 10, 16]:
        print('Wrong input. Try again!')
        board_size = int(input('Input board size: '))

    # first_player = input('Who is to make the first move [h/c]: ')
    first_player = 'h'
    while first_player not in ['h', 'H', 'c', 'C']:
        print('Wrong input. Try again!')
        first_player = input('Who is to make the first move [h/c]: ')

    start_game(board_size, first_player)


