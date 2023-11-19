import pygame
import tkinter as tk
from tkinter import ttk
import threading
from GUI import GUI
from get_initialized_board import get_initialized_board

grid_size = 8
need_restart = threading.Event()

def run_tkinter():
    def on_select(event=None):
        global grid_size
        new_size = int(combo.get())
        grid_size = new_size
        need_restart.set()

    root = tk.Tk()
    root.title("Settings")
    root.geometry('250x50')

    label = tk.Label(root, text="Grid size:")
    label.grid(column=0, row=0)

    n = tk.StringVar(value=str(grid_size))
    combo = ttk.Combobox(root, width=15, textvariable=n, values=[4, 6, 8, 10, 12, 14, 16])
    combo.grid(column=1, row=0)
    combo.bind("<<ComboboxSelected>>", on_select)
    root.mainloop()

def run_pygame():
    global grid_size, need_restart
    while True:
        pygame.init()
        screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Byte')

        gui = GUI(screen, grid_size)
        board = get_initialized_board(grid_size)
        gui.draw_board(board)

        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if need_restart.is_set():
                pygame.quit()
                need_restart.clear()
                break

        if not tk_thread.is_alive():
            break

tk_thread = threading.Thread(target=run_tkinter, daemon=True)
tk_thread.start()

run_pygame()