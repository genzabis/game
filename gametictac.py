import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.config(bg="#f0f0f0")  # Set background color for the window

        # Inisialisasi variabel permainan
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        # Skor untuk masing-masing pemain dan seri
        self.score_x = 0
        self.score_o = 0
        self.draws = 0

        # Frame untuk status
        status_frame = tk.Frame(self.window, bg="#f0f0f0")
        status_frame.pack(pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="Klik 'Start' untuk mulai permainan",
            font=('Helvetica', 16, 'bold'),
            bg="#f0f0f0",
            fg="#333"
        )
        self.status_label.pack()

        self.score_label = tk.Label(
            status_frame,
            text=f"X: {self.score_x} | O: {self.score_o} | Seri: {self.draws}",
            font=('Helvetica', 14),
            bg="#f0f0f0",
            fg="#555"
        )
        self.score_label.pack()

        # Frame untuk papan permainan
        game_frame = tk.Frame(self.window, bg='white')
        game_frame.pack(pady=10)

        # Membuat grid 3x3
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    game_frame,
                    text="",
                    font=('Arial', 24, 'bold'),
                    width=6,
                    height=2,
                    bg="#f7f7f7",
                    relief="solid",
                    borderwidth=2,
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

        # Tombol start
        start_button = tk.Button(
            self.window,
            text="Start Game",
            font=('Helvetica', 14, 'bold'),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            command=self.start_game,
            relief="flat",
            padx=20,
            pady=10
        )
        start_button.pack(pady=10)

        # Tombol reset
        reset_button = tk.Button(
            self.window,
            text="Reset Game",
            font=('Helvetica', 14, 'bold'),
            bg="#FF5733",
            fg="white",
            activebackground="#e04d2b",
            command=self.reset_game,
            relief="flat",
            padx=20,
            pady=10
        )
        reset_button.pack(pady=10)

        # Frame untuk animasi (scrolling text)
        animation_frame = tk.Frame(self.window, bg="#f0f0f0")
        animation_frame.pack(pady=10)

        self.scroll_label = tk.Label(
            animation_frame,
            text="Keep playing! | Keep playing! | Keep playing! | Keep playing! | Keep playing! ",
            font=('Helvetica', 12),
            bg="#f0f0f0",
            fg="#007bff"
        )
        self.scroll_label.pack()

        self.animate_scroll()

        # Mengatur ukuran minimum window
        self.window.minsize(400, 500)

    def animate_scroll(self):
        # Animasi scrolling
        current_text = self.scroll_label.cget("text")
        new_text = current_text[1:] + current_text[0]
        self.scroll_label.config(text=new_text)
        self.window.after(150, self.animate_scroll)  # Ulangi setiap 150ms

    def start_game(self):
        # Reset game dan aktifkan tombol
        self.reset_game()
        self.status_label.config(text=f"Giliran Player {self.current_player}")
        for button in self.buttons:
            button.config(state="normal")

    def button_click(self, row, col):
        index = row * 3 + col

        # Cek apakah kotak masih kosong
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(
                text=self.current_player,
                state="disabled",
                disabledforeground="black"
            )

            # Cek pemenang
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} Menang!")
                if self.current_player == "X":
                    self.score_x += 1
                else:
                    self.score_o += 1
                self.update_score()
                self.disable_all_buttons()
            # Cek seri
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "Permainan Seri!")
                self.draws += 1
                self.update_score()
                self.disable_all_buttons()
            else:
                # Ganti pemain
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Giliran Player {self.current_player}")

    def check_winner(self):
        # Kombinasi menang
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Baris
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Kolom
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]

        # Cek setiap kombinasi
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == 
                self.board[combo[2]] == self.current_player):
                # Highlight kombinasi pemenang
                for index in combo:
                    self.buttons[index].config(bg='#8cff66')  # Warna latar belakang pemenang
                return True
        return False

    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")

    def reset_game(self):
        # Reset variabel
        self.current_player = "X"
        self.board = [""] * 9
        self.status_label.config(text="Klik 'Start' untuk mulai permainan")

        # Reset tombol
        for button in self.buttons:
            button.config(
                text="",
                state="disabled",
                bg="#f7f7f7"
            )

    def update_score(self):
        # Update tampilan skor
        self.score_label.config(text=f"X: {self.score_x} | O: {self.score_o} | Seri: {self.draws}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
