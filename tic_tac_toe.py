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

heuristic_array = {
  {0, -1 , -10, -100},
  {1, 0, 0, 0},
  {10, 0, 0, 0},
  {100, 0, 0, 0} 
}

winning_positions = {
  { 0, 1, 2 },
  { 3, 4, 5 },
  { 6, 7, 8 },
  { 0, 3, 6 },
  { 1, 4, 7 },
  { 2, 5, 8 },
  { 0, 4, 8 },
  { 2, 4, 6 }
}

class TicTacToeGame:
  def __init__(self, difficulty):
    self.players = cycle(PLAYERS)
    self.board_size = 3
    self.current_player = next(self.players)
    self.has_winner = False
    self.difficulty = difficulty
    self.current_state = [['.', '.', '.'],
                          ['.', '.', '.'],
                          ['.', '.', '.']]

  def is_valid_move(self, row, col):
    # Check if move is valid
    if row < 0 or row > 2 or col < 0 or col > 2:
        return False
    elif self.current_state[row][col] != '.':
        return False
    else:
        return True

  def minimax_alphabeta(self, S, d, alpha, beta, ig): # returns heuristic value and next state
    if d == 0:
      return self.hev(S), S  #return h(S)

    if ig == True:
      val = float('-inf')
      for i in 5:
        val = max(val, self.minimax_alphabeta(S, d-1, False)) #S'
        alpha = max(alpha, val)
        if val >= beta:
          break
      return val  
    else:
      val = float('inf')
      for i in 5:
        val = min(val, self.minimax_alphabeta(S, d-1, True)) #S'
        beta = min(beta, val)
        if val <= alpha:
          break
      return val
    
  def max(self):
    row, col = None
    tmpMax = -2

    # -1 for loss, 1 for win and 0 for a tie
    result = self.is_end()
    if result == 'X':
      return (-1, 0, 0)
    elif result == 'O':
      return (1, 0, 0)
    elif result == '.':
      return (0, 0, 0)
    
    for i in range(0, 3):
       for j in range(0, 3):
          if self.current_state[i][j] == '.':
            self.current_state[i][j] = 'O'
            # check this move
            (m, min_i, min_j) = self.min()
            if m > tmpMax:
              tmpMax = m
              row = i
              col = j
            self.current_state[i][j] = '.'
    return (tmpMax, row, col)

  def min(self):     
    row, col = None
    tmpMin = 2

     # -1 for loss, 1 for win and 0 for a tie
    result = self.is_end()
    if result == 'X':
      return (-1, 0, 0)
    elif result == 'O':
      return (1, 0, 0)
    elif result == '.':
      return (0, 0, 0)
    
    for i in range(0, 3):
       for j in range(0, 3):
          if self.current_state[i][j] == '.':
            self.current_state[i][j] = 'X'
            # check this move
            (m, max_i, max_j) = self.max()
            if m < tmpMin:
              tmpMin = m
              row = i
              col = j
            self.current_state[i][j] = '.'
    return (tmpMin, row, col)
  
  def is_leaf(state):
    for i in range(0, 9):
      if(state[i] == '.'): return False
    return True
  
  def hev(self, cells):
    opponent = next(self.current_player)
    heuristic = 0

    for i in range(0,8):
      player_count = opponent_count = 0 
      for j in range(0,3):
        move = cells[winning_positions[i][j]]
        if (move == self.current_player): player_count += 1
        elif (move == opponent): opponent_count += 1
      heuristic += heuristic_array[player_count][opponent_count]

    return heuristic  
    

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

  def reset_game(self):
    self.current_player = next(self.players)
    self.current_state = [['.', '.', '.'],
                          ['.', '.', '.'],
                          ['.', '.', '.']]
    self.has_winner = False


class TicTacToeBoard(tk.Tk):
  def __init__(self, game):
    super().__init__()
    self.title("Tic-Tac-Toe Game")
    self.cells = {}
    self.game = game
    self.create_menu()
    self.create_board_display()
    self.create_board_grid()

  def create_menu(self):
    menu_bar = tk.Menu(master = self)
    self.config(menu=menu_bar)
    file_menu = tk.Menu(master = menu_bar)
    file_menu.add_command(label="Play Again", command=self.reset_board)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    radio_option = tk.IntVar(None, self.game.difficulty)

    difficulty_menu = tk.Menu(master = menu_bar)
    difficulty_menu.add_radiobutton(label="Easy", variable=radio_option, value=3)
    difficulty_menu.add_radiobutton(label="Medium", variable=radio_option, value=5)
    difficulty_menu.add_radiobutton(label="Hard", variable=radio_option, value=7)
    menu_bar.add_cascade(label='Difficulty', menu=difficulty_menu)
    radio_option.set(5)

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
    if(self.game.has_winner != True):
      clicked_button = event.widget
      row, col = self.cells[clicked_button]
      if self.game.is_valid_move(row, col):
        self.game.current_state[row][col] = self.game.current_player.label
        self.update_button(clicked_button)

        # check if game is finished
        result = self.game.is_end()
        if(result == None):
          self.game.toggle_player()
          self.update_display(msg=f"{self.game.current_player.label}'s turn")
        elif(result == '.'):
          self.update_display(msg='Draw!')
        else:
          self.update_display(msg=f"{self.game.current_player.label} wins!")  
          self.game.has_winner = True

  def update_button(self, clicked_button):
    clicked_button.config(text=self.game.current_player.label)
    clicked_button.config(fg=self.game.current_player.color)

  def update_display(self, msg, color="black"):
    self.display['text'] = msg
    self.display['fg'] = color

  def reset_board(self):
    self.game.reset_game()
    self.update_display(msg=f"{self.game.current_player.label}'s turn")
    for button in self.cells.keys():
      button.config(highlightbackground='lightblue')
      button.config(text='')
      button.config(fg='black')


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame(5)
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()        