import tkinter as tk
import requests
import random
import time
from tkinter import messagebox


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test Game")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4f8")
        
        # Game variables
        self.time_left = 60
        self.score = 0
        self.current_word = ""
        self.word_list = []

        # UI Elements
        self.header_label = tk.Label(
            root, text="Typing Speed Test", font=("Arial", 24, "bold"), bg="#f0f4f8", fg="#2c3e50"
        )
        self.header_label.pack(pady=10)

        self.timer_label = tk.Label(
            root, text="Time left: 60 seconds", font=("Arial", 16), bg="#f0f4f8", fg="#555"
        )
        self.timer_label.pack(pady=10)

        self.word_label = tk.Label(
            root, text="", font=("Arial", 28, "bold"), bg="#f0f4f8", fg="#3498db"
        )
        self.word_label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 16), justify="center", fg="#333", bg="#ffffff", relief="solid")
        self.entry.pack(pady=10, ipadx=10, ipady=5)
        self.entry.bind("<Return>", self.check_word)

        self.score_label = tk.Label(
            root, text="Score: 0", font=("Arial", 16), bg="#f0f4f8", fg="#555"
        )
        self.score_label.pack(pady=10)

        self.result_label = tk.Label(
            root, text="", font=("Arial", 14), bg="#f0f4f8", fg="green"
        )
        self.result_label.pack(pady=10)

        self.start_button = tk.Button(
            root, text="Start Game", font=("Arial", 16), command=self.start_game, bg="#27ae60", fg="white", relief="flat"
        )
        self.start_button.pack(pady=20)

        # Timer update reference
        self.running = False

    def fetch_random_words(self):
        
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word?number=100") #Fetch a list of random words from an online API.
            if response.status_code == 200:
                self.word_list = response.json()
            else:
                raise Exception("Error fetching words.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch random words: {e}")
            # Fallback words
            self.word_list = ["fallback", "word", "typing", "test", "speed", "keyboard", "practice"]

    def start_game(self):
        """Start the typing speed test."""
        self.running = True
        self.time_left = 60
        self.score = 0
        self.current_word = ""
        self.fetch_random_words()
        self.entry.delete(0, tk.END)
        self.update_timer()
        self.next_word()

    def next_word(self):
        """Display a new random word."""
        if self.word_list:
            self.current_word = random.choice(self.word_list)
            self.word_label.config(text=self.current_word)
            self.result_label.config(text="")
            self.entry.delete(0, tk.END)

    def check_word(self, event=None):
        """Check if the typed word matches the displayed word."""
        if not self.running:
            return
        typed_word = self.entry.get().strip()
        if typed_word == self.current_word:
            self.score += 1
            self.result_label.config(text="Correct!", fg="green")
        else:
            self.result_label.config(text=f"Wrong! The word was '{self.current_word}'", fg="red")
        self.score_label.config(text=f"Score: {self.score}")
        self.next_word()

    def update_timer(self):
        """Update the timer every second."""
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        """End the game and display the final score."""
        self.running = False
        self.word_label.config(text="Game Over!")
        self.result_label.config(text=f"Final Score: {self.score}", fg="blue")
        self.timer_label.config(text="Time left: 0 seconds")


# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    game = TypingSpeedTest(root)
    root.mainloop()
