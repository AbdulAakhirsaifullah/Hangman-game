import tkinter as tk
import random

# Predefined words
words = ["apple", "banana", "grape", "mango", "peach"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game 🎮")
        
        # Initialize game variables
        self.word = random.choice(words)
        self.guessed_word = ["_"] * len(self.word)
        self.attempts = 6
        self.guessed_letters = []
        
        # Title
        self.label_title = tk.Label(root, text="Hangman Game", font=("Arial", 20, "bold"), fg="blue")
        self.label_title.pack(pady=10)
        
        # Word display
        self.label_word = tk.Label(root, text=" ".join(self.guessed_word), font=("Arial", 18))
        self.label_word.pack(pady=10)
        
        # Attempts left
        self.label_attempts = tk.Label(root, text=f"Attempts left: {self.attempts}", font=("Arial", 14), fg="red")
        self.label_attempts.pack(pady=10)
        
        # Canvas for drawing hangman
        self.canvas = tk.Canvas(root, width=200, height=250, bg="white")
        self.canvas.pack(pady=10)
        self.draw_gallows()
        
        # Entry box
        self.entry_guess = tk.Entry(root, font=("Arial", 14))
        self.entry_guess.pack(pady=10)
        self.entry_guess.focus()
        
        # Bind Enter key instead of button
        self.entry_guess.bind("<Return>", self.make_guess)
        
        # Result message
        self.label_result = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.label_result.pack(pady=10)
        
        # Retry button (hidden initially)
        self.retry_button = None
    
    def draw_gallows(self):
        """Draw the static gallows"""
        self.canvas.create_line(20, 230, 180, 230, width=3)   # base
        self.canvas.create_line(50, 230, 50, 20, width=3)     # pole
        self.canvas.create_line(50, 20, 120, 20, width=3)     # top beam
        self.canvas.create_line(120, 20, 120, 50, width=3)    # rope
    
    def draw_hangman(self):
        """Draw body parts depending on attempts left"""
        parts = 6 - self.attempts
        if parts == 1:  # head
            self.canvas.create_oval(100, 50, 140, 90, width=3)
        elif parts == 2:  # body
            self.canvas.create_line(120, 90, 120, 150, width=3)
        elif parts == 3:  # left arm
            self.canvas.create_line(120, 110, 90, 130, width=3)
        elif parts == 4:  # right arm
            self.canvas.create_line(120, 110, 150, 130, width=3)
        elif parts == 5:  # left leg
            self.canvas.create_line(120, 150, 90, 190, width=3)
        elif parts == 6:  # right leg
            self.canvas.create_line(120, 150, 150, 190, width=3)
    
    def make_guess(self, event=None):
        guess = self.entry_guess.get().lower()
        self.entry_guess.delete(0, tk.END)
        
        if len(guess) != 1 or not guess.isalpha():
            self.label_result.config(text="⚠️ Enter a single letter.", fg="orange")
            return
        
        if guess in self.guessed_letters:
            self.label_result.config(text="⚠️ You already guessed that!", fg="orange")
            return
        
        self.guessed_letters.append(guess)
        
        if guess in self.word:
            for i in range(len(self.word)):
                if self.word[i] == guess:
                    self.guessed_word[i] = guess
            self.label_word.config(text=" ".join(self.guessed_word))
            self.label_result.config(text="✅ Good guess!", fg="green")
        else:
            self.attempts -= 1
            self.label_attempts.config(text=f"Attempts left: {self.attempts}")
            self.label_result.config(text="❌ Wrong guess!", fg="red")
            self.draw_hangman()
        
        # Check win/lose
        if "_" not in self.guessed_word:
            self.label_result.config(text=f"🎉 You won! The word was '{self.word}'", fg="purple")
            self.entry_guess.config(state=tk.DISABLED)
            self.show_retry_button()
        elif self.attempts == 0:
            self.label_result.config(text=f"💀 Game Over! The word was '{self.word}'", fg="black")
            self.entry_guess.config(state=tk.DISABLED)
            self.show_retry_button()
    
    def show_retry_button(self):
        """Show retry button when the game ends"""
        if self.retry_button is None:  # create only once
            self.retry_button = tk.Button(self.root, text="🔄 Retry", font=("Arial", 14), command=self.reset_game)
            self.retry_button.pack(pady=10)
    
    def reset_game(self):
        """Reset all game variables and UI"""
        self.word = random.choice(words)
        self.guessed_word = ["_"] * len(self.word)
        self.attempts = 6
        self.guessed_letters = []
        
        # Reset labels
        self.label_word.config(text=" ".join(self.guessed_word))
        self.label_attempts.config(text=f"Attempts left: {self.attempts}")
        self.label_result.config(text="", fg="blue")
        
        # Reset entry
        self.entry_guess.config(state=tk.NORMAL)
        self.entry_guess.delete(0, tk.END)
        self.entry_guess.focus()
        
        # Clear canvas and redraw gallows
        self.canvas.delete("all")
        self.draw_gallows()
        
        # Hide retry button
        if self.retry_button:
            self.retry_button.destroy()
            self.retry_button = None


# Run game
root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
