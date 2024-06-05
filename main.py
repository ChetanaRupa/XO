import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self, player1_name, player2_name, player1_symbol, player2_symbol):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_symbol = player1_symbol
        self.player2_symbol = player2_symbol
        self.current_player = self.player1_symbol
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            return True
        else:
            return False

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        return None

class TicTacToeSetupGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe Setup")

        self.player1_name = None
        self.player2_name = None
        self.player1_symbol = None

        self.create_setup_dialog()

    def create_setup_dialog(self):
        player1_label = tk.Label(self.root, text="Player 1 Name:")
        player1_label.grid(row=0, column=0)
        self.player1_entry = tk.Entry(self.root)
        self.player1_entry.grid(row=0, column=1)

        player2_label = tk.Label(self.root, text="Player 2 Name:")
        player2_label.grid(row=1, column=0)
        self.player2_entry = tk.Entry(self.root)
        self.player2_entry.grid(row=1, column=1)

        symbol_label = tk.Label(self.root, text="Choose Symbol for Player 1:")
        symbol_label.grid(row=2, column=0)
        self.symbol_var = tk.StringVar(self.root)
        self.symbol_var.set("X")  # Default symbol
        self.symbol_menu = tk.OptionMenu(self.root, self.symbol_var, "X", "O")
        self.symbol_menu.grid(row=2, column=1)

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.grid(row=3, columnspan=2)

    def start_game(self):
        self.player1_name = self.player1_entry.get()
        self.player2_name = self.player2_entry.get()
        self.player1_symbol = self.symbol_var.get()

        if self.player1_name.strip() == "" or self.player2_name.strip() == "":
            messagebox.showerror("Error", "Please enter names for both players.")
            return
        
        self.root.destroy()
        game = TicTacToeGame(self.player1_name, self.player2_name, self.player1_symbol, "X" if self.player1_symbol == "O" else "O")
        TicTacToeGUI(game)

class TicTacToeGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")

        self.create_board()

    def create_board(self):
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text="", font=("Helvetica", 20), width=6, height=3,
                                   command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, columnspan=3)

    def reset(self):
        for i in range(3):
            for j in range(3):
                self.game.board[i][j] = " "
                self.buttons[i][j].config(text="")
        self.game.current_player = self.game.player1_symbol

    def on_click(self, row, col):
        if self.game.make_move(row, col):
            self.buttons[row][col].config(text=self.game.current_player)
            winner = self.game.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{self.game.player1_name if winner == 'X' else self.game.player2_name} wins!")
                self.root.destroy()
            elif all(all(cell != " " for cell in row) for row in self.game.board):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.root.destroy()
            else:
                self.game.current_player = self.game.player2_symbol if self.game.current_player == self.game.player1_symbol else self.game.player1_symbol

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    setup_gui = TicTacToeSetupGUI()
    setup_gui.root.mainloop()
