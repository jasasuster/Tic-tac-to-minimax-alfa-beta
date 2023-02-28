import tkinter as tk
from tkinter import font
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
  label: str
  color: str

class Move(NamedTuple):
  row: int
  col: int
  label: str = ''

PLAYERS = (
  Player(label='X', color='blue'),
  Player(label='O', color='red')
)

class TicTacToeGame:
  def __init__(self):
    self.players = cycle(PLAYERS)
    self.board_size = 3
    self.current_player = next(self.players)
    self.winner_combo = []
    self.current_state = []
    self.has_winner = False
    # self.winning_combos = []
    self.setup_board()

  def setup_board(self):
    self.current_state = [['.', '.', '.'],
                          ['.', '.', '.'],
                          ['.', '.', '.']]
    # self.winning_combos = self.get_winning_combos()

  def is_valid_move(self, row, col):
    # Check if move is valid
    if row < 0 or row > 2 or col < 0 or col > 2:
        return False
    elif self.current_state[row][col] != '.':
        return False
    else:
        return True

  def minimax(S, d, ig):
    if d == 0:
      return()  #return h(S)

    if ig == True:
      val = float('-inf')
      for i in 5:
        val = max(val, TicTacToeGame.minimax(S, d-1, False)) #S'
      return val  
    else:
      val = float('inf')
      for i in 5:
        val = min(val, TicTacToeGame.minimax(S, d-1, True)) #S'
      return val

  def toggle_player(self):
    self.current_player = next(self.players)

  def is_end(self):
    # Vertical win
    for i in range(0, 3):
        if (self.current_state[0][i] != '.' and
            self.current_state[0][i] == self.current_state[1][i] and
            self.current_state[1][i] == self.current_state[2][i]):
            return self.current_state[0][i]

    # Horizontal win
    for i in range(0, 3):
        if (self.current_state[i] == ['X', 'X', 'X']):
            return 'X'
        elif (self.current_state[i] == ['O', 'O', 'O']):
            return 'O'

    # Main diagonal win
    if (self.current_state[0][0] != '.' and
        self.current_state[0][0] == self.current_state[1][1] and
        self.current_state[0][0] == self.current_state[2][2]):
        return self.current_state[0][0]

    # Second diagonal win
    if (self.current_state[0][2] != '.' and
        self.current_state[0][2] == self.current_state[1][1] and
        self.current_state[0][2] == self.current_state[2][0]):
        return self.current_state[0][2]

    # Is whole board full?
    for i in range(0, 3):
        for j in range(0, 3):
            # There's an empty field, we continue the game
            if (self.current_state[i][j] == '.'):
                return None

    # It's a tie!
    return '.'  

class TicTacToeBoard(tk.Tk):
  def __init__(self, game):
    super().__init__()
    self.title("Tic-Tac-Toe Game")
    self.cells = {}
    self.game = game
    self.create_menu
    self.create_board_display()
    self.create_board_grid()

  def create_menu(self):
    menu_bar = tk.Menu(master=self)
    self.config(menu=menu_bar)
    file_menu = tk.Menu(master=menu_bar)
    file_menu.add_command(label="Play Again", command=self.reset_board)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=quit)
    menu_bar.add_cascade(label="File", menu=file_menu)  

  def create_board_display(self):
    display_frame = tk.Frame(master=self)
    display_frame.pack(fill=tk.X)
    self.display = tk.Label(
      master=display_frame,
      text=f"{self.game.current_player.label}'s turn",
      font=font.Font(size=28, weight="bold"),
    )
    self.display.pack()

  def create_board_grid(self):
    grid_frame = tk.Frame(master=self)
    grid_frame.pack()
    for row in range(3):
      self.rowconfigure(row, weight=1, minsize=50)
      self.columnconfigure(row, weight=1, minsize=75)
      for col in range(3):
        button = tk.Button(
          master=grid_frame,
          text="",
          font=font.Font(size=36, weight="bold"),
          fg="black",
          width=3,
          height=2,
          highlightbackground="lightblue",
        )
        self.cells[button] = (row, col)
        button.bind("<ButtonPress-1>", self.handle_move)
        button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

  def handle_move(self, event):
    clicked_button = event.widget
    row, col = self.cells[clicked_button]
    if self.game.is_valid_move(row, col):
      self.game.current_state[row][col] = self.game.current_player.label
      self.update_button(clicked_button)

      print(self.game.is_end())

      self.game.toggle_player()
      self.update_display(msg=f"{self.game.current_player.label}'s turn")
      print(self.game.current_state)

  def update_button(self, clicked_button):
    clicked_button.config(text=self.game.current_player.label)
    clicked_button.config(fg=self.game.current_player.color)

  def update_display(self, msg, color="black"):
    self.display['text'] = msg
    self.display['fg'] = color


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()        