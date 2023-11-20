import pygame
from GUI import GUI
from Board import Board


def start_game(board_size, first_player):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Byte')
    running = True

    gui = GUI(screen)
    tile_size = screen.get_height() // board_size
    board = Board(board_size, tile_size)
    board.initialize_board()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    print(f"Mouse clicked at position: {x}, {y}")
                    board.highlight_clicked_token(x, y)

        gui.draw_board(board)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    # board_size = int(input('Input board size: '))
    board_size = 8
    while board_size % 2 == 1 or board_size < 4 or board_size > 16:
        print('Wrong input. Try again!')
        board_size = input('Input board size: ')

    # first_player = input('Who is to make the first move [h/c]: ')
    first_player = 'h'
    while first_player not in ['h', 'H', 'c', 'C']:
        print('Wrong input. Try again!')
        first_player = input('Who is to make the first move [h/c]: ')


    start_game(board_size, first_player)