import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time

MAX_LINES = 3
MAX_BET = 1000000000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

class SlotMachineGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")

        self.player_balance = 0
        self.wallet_balance = 1000
        self.lost_balance = 0
        
        self.create_widgets()

    def create_widgets(self):
        self.balance_label = tk.Label(self.root, text=f"Player Balance: ${self.player_balance}\nWallet Balance: ${self.wallet_balance}")
        self.balance_label.pack()

        self.add_cash_button = tk.Button(self.root, text="Add Cash", command=self.add_cash)
        self.add_cash_button.pack()

        self.cashout_button = tk.Button(self.root, text="Cashout", command=self.cashout)
        self.cashout_button.pack()

        self.lines_label = tk.Label(self.root, text="Select Number of Lines:")
        self.lines_label.pack()

        self.lines_var = tk.StringVar(self.root)
        self.lines_var.set("1")
        self.lines_menu = tk.OptionMenu(self.root, self.lines_var, *range(1, MAX_LINES + 1))
        self.lines_menu.pack()

        self.bet_label = tk.Label(self.root, text="Bet per Line:")
        self.bet_label.pack()

        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        self.spin_button = tk.Button(self.root, text="Spin", command=self.spin)
        self.spin_button.pack()
        self.lost_balance_button = tk.Button(self.root, text=f"Lost: ${self.lost_balance}", state="disabled")
        self.lost_balance_button.pack()


        self.canvas = tk.Canvas(self.root, width=200, height=100)
        self.canvas.pack()
    
    def update_lost_balance_button(self):
        self.lost_balance_button.config(text=f"Lost: ${self.lost_balance}")

    
    def add_cash(self):
        amount = int(simpledialog.askstring("Add Cash", "Enter the amount you want to add:"))
        if amount is not None and amount > 0:
            if amount <= self.wallet_balance:
                self.wallet_balance -= amount
                self.player_balance += amount
                self.update_balance_label()
            else:
                messagebox.showerror("Insufficient Funds", "You do not have enough money in your wallet.")

    def cashout(self):
        self.wallet_balance += self.player_balance
        self.player_balance = 0
        self.update_balance_label()

    def spin(self):
        lines = int(self.lines_var.get())
        bet = int(self.bet_entry.get())

        if bet < MIN_BET or bet > MAX_BET:
            messagebox.showerror("Invalid Bet", f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
            return

        self.total_bet = bet * lines
        if self.total_bet > self.player_balance:  # Here change total_bet to self.total_bet
            messagebox.showerror("Insufficient Balance", "You do not have enough balance to place this bet.")
            return

        self.player_balance -= self.total_bet  # Here change total_bet to self.total_bet

        self.update_balance_label()
        self.animate_slot_machine()


    def update_balance_label(self):
        self.balance_label.config(text=f"Player Balance: ${self.player_balance}\nWallet Balance: ${self.wallet_balance}")

    def show_spin_result(self, winning_lines, winnings):
        message = f"You won ${winnings} on lines: {', '.join(map(str, winning_lines))}" if winnings > 0 else "You lost."
        messagebox.showinfo("Spin Result", message)
        self.update_balance_label()

    def animate_slot_machine(self):
        # Create a list of symbols for each column to give the impression of spinning
        # Let's take 5 sets of symbols for each column
        columns = [random.choices(list(symbol_count.keys()), k=ROWS * 5) for _ in range(COLS)]
        column_text_ids = [[None for _ in range(ROWS * 5)] for _ in range(COLS)]  # Text IDs for canvas items

        # Initial draw of the slot machine
        slot_width = 200 / COLS
        slot_height = 100 / ROWS
        for col in range(COLS):
            for row in range(ROWS * 5):
                x0 = col * slot_width
                y0 = row * slot_height  # Adjust the position based on the row index
                x1 = x0 + slot_width
                y1 = y0 + slot_height
                column_text_ids[col][row] = self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=columns[col][row], font=("Arial", 16))

        for spin_round in range(5 * ROWS):  # Adjusted the rounds based on the number of symbols
            for col in range(COLS):
                for row in range(ROWS * 5):
                    current_coords = self.canvas.coords(column_text_ids[col][row])
                    new_y = current_coords[1] + slot_height
                    # If the text goes beyond canvas, wrap it to the top
                    if new_y > ROWS * 5 * slot_height:
                        new_y -= ROWS * 5 * slot_height
                    self.canvas.coords(column_text_ids[col][row], current_coords[0], new_y)

        self.root.update()
        time.sleep(0.1)

        # Clean up: delete the additional symbols outside of the visible canvas
        for col in range(COLS):
            for row in range(ROWS * 5):
                if row >= ROWS:  # We keep the first ROWS symbols and delete the rest
                    self.canvas.delete(column_text_ids[col][row])

        # Extract the final state of the slots after animation.
        final_columns = [columns[col][:ROWS] for col in range(COLS)]
        winnings, winning_lines = check_winnings(final_columns, int(self.lines_var.get()), self.total_bet, symbol_value)





    def draw_slot_machine(self, columns):
        self.canvas.delete("all")
        slot_width = 200 / COLS
        slot_height = 100 / ROWS
        for col in range(COLS):
            for row in range(ROWS):
                x0 = col * slot_width
                y0 = row * slot_height
                x1 = x0 + slot_width
                y1 = y0 + slot_height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=columns[col][row], font=("Arial", 16))

if __name__ == "__main__":
    root = tk.Tk()
    game = SlotMachineGame(root)
    root.mainloop()
