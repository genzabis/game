import tkinter as tk
import random
from PIL import Image, ImageTk  # Import Pillow untuk manipulasi gambar

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Ular")
        self.master.resizable(False, False)

        # Ukuran canvas
        self.canvas_width = 400
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # Tombol Start dan Restart
        self.start_button = tk.Button(self.master, text="Start", width=10, command=self.start_game)
        self.start_button.pack(pady=10)

        self.restart_button = tk.Button(self.master, text="Restart", width=10, command=self.restart_game)
        self.restart_button.pack(pady=10)
        self.restart_button.config(state=tk.DISABLED)

        # Inisialisasi game
        self.snake = []
        self.snake_direction = ""
        self.food = None
        self.score = 0
        self.game_over = False

        # Menggunakan Pillow untuk mengubah ukuran gambar
        self.snake_image = self.resize_image("images/ular.png", 10, 10)  # Gambar ular dikecilkan
        self.food_image = self.resize_image("images/apel.png", 10, 10)   # Gambar apel dikecilkan

        # Key bindings untuk kontrol
        self.master.bind("<Left>", lambda event: self.change_direction("Left"))
        self.master.bind("<Right>", lambda event: self.change_direction("Right"))
        self.master.bind("<Up>", lambda event: self.change_direction("Up"))
        self.master.bind("<Down>", lambda event: self.change_direction("Down"))

    def resize_image(self, image_path, width, height):
        """Mengubah ukuran gambar menggunakan Pillow"""
        try:
            img = Image.open(image_path)
            img = img.resize((width, height), Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")  # Menampilkan pesan error
            return None  # Kembalikan None jika ada error

    def start_game(self):
        """Memulai game saat tombol Start ditekan."""
        self.start_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)
        self.game_over = False
        self.score = 0
        self.snake = [(100, 100), (90, 100), (80, 100)]  # Posisi awal ular
        self.snake_direction = "Right"
        self.create_food()
        self.run_game()

    def restart_game(self):
        """Memulai ulang game saat tombol Restart ditekan."""
        self.canvas.delete("all")  # Menghapus semua objek di canvas
        self.start_game()  # Memulai ulang permainan

    def create_food(self):
        """Membuat makanan di tempat acak di canvas."""
        food_x = random.randint(0, (self.canvas_width - 10) // 10) * 10
        food_y = random.randint(0, (self.canvas_height - 10) // 10) * 10
        self.food = (food_x, food_y)
        if self.food_image:  # Pastikan gambar makanan berhasil dimuat
            self.canvas.create_image(food_x + 5, food_y + 5, image=self.food_image, tags="food")

    def change_direction(self, new_direction):
        """Mengubah arah gerakan ular jika tidak berlawanan arah."""
        if (new_direction == "Left" and self.snake_direction != "Right") or \
           (new_direction == "Right" and self.snake_direction != "Left") or \
           (new_direction == "Up" and self.snake_direction != "Down") or \
           (new_direction == "Down" and self.snake_direction != "Up"):
            self.snake_direction = new_direction

    def move_snake(self):
        """Menggerakkan ular berdasarkan arah yang dipilih."""
        head_x, head_y = self.snake[0]

        if self.snake_direction == "Left":
            head_x -= 10
        elif self.snake_direction == "Right":
            head_x += 10
        elif self.snake_direction == "Up":
            head_y -= 10
        elif self.snake_direction == "Down":
            head_y += 10

        # Menambah kepala ular
        new_head = (head_x, head_y)

        # Cek tabrakan dengan tubuh sendiri
        if new_head in self.snake:
            self.game_over = True
            return

        # Menambahkan kepala ular ke depan dan menghapus ekor
        self.snake = [new_head] + self.snake[:-1]

        # Cek tabrakan dengan dinding
        if head_x < 0 or head_x >= self.canvas_width or head_y < 0 or head_y >= self.canvas_height:
            self.game_over = True

    def check_food_collision(self):
        """Cek jika ular makan makanan."""
        if self.snake[0] == self.food:
            self.score += 1
            self.snake.append(self.snake[-1])  # Menambah panjang ular
            self.canvas.delete("food")
            self.create_food()

    def draw_snake(self):
        """Menggambar ular di canvas dengan gambar."""
        self.canvas.delete("snake")  # Menghapus ular lama
        for segment in self.snake:
            if self.snake_image:  # Pastikan gambar ular berhasil dimuat
                self.canvas.create_image(segment[0] + 5, segment[1] + 5, image=self.snake_image, tags="snake")

    def run_game(self):
        """Menjalankan game loop."""
        if self.game_over:
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2, text="Game Over!", fill="white", font=("Arial", 24))
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 30, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        else:
            self.move_snake()
            self.check_food_collision()
            self.draw_snake()
            self.master.after(100, self.run_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
