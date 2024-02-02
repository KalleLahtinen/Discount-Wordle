"""
COMP.CS.100 Exercise gui_project
Creator: Kalle Lahtinen
"""

import random
from tkinter import *
from tkinter import filedialog as fd

"""An advanced project"""

"""A discount clone of Wordle, originally by Josh Wardle. 
A list of guessable words is read from an input text file with each row 
containing a single five letter word. 

A default input file <wordle_wordlist.txt> located in program folder is assumed 
but the program will ask for a different file in it's absence."""


"""HOW TO PLAY: You try to guess a word in six tries. Correctly guessed 
letters in the correct spot are colored green, correct letters in the wrong 
spot are colored orange. Wrong letters are darkened."""


# Word length can be changed between 4 and 8 with a matching input file,
# but the default length (5) is recommended.
WORD_LENGTH = 5
WORD_INPUT_FILE = "wordle_wordlist.txt"


class Wordle:
    def __init__(self):
        self.__root = Tk()
        self.__root.title("Discount Wordle")

        # Define main window size
        root_width, root_height = 700, 650

        # ======================================================================
        # Centering the main window, as per the tkinter documentation.
        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()

        x = screenwidth/2 - root_width/2
        y = screenheight/2 - root_height/2

        self.__root.geometry('%dx%d+%d+%d' % (root_width, root_height, x, y))

        # ======================================================================
        # Adding colors as attributes for ease of use.
        self.__bg_color = "#333333"
        self.__fg_color = "white"
        self.__widget_color = "#595959"

        self.__root.config(bg= self.__bg_color)

        # Initializing the word being guessed and other data.
        self.__word_split = None
        self.__word_lst = None

        self.__input_letters = []
        self.__guess_count = 0

        self.__game_over = False

        self.__key_lst = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                          'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                          'X', 'C', 'V', 'B', 'N', 'M']

        # ======================================================================
        # The matrix for guessed words.

        self.__letter_labels = []

        # A matrix of 6 * WORD_LENGTH (y*x) is created.
        # The matrix elements are initialized as None.
        for row in range(6):
            self.__letter_labels.append([None] * WORD_LENGTH)

        # Create blank labels for every element of "__letter_labels" and store
        # them in their corresponding coordinates with x=column and y=row.
        for y, row in enumerate(self.__letter_labels):
            for x, letter in enumerate(row):
                letter_label = Label(self.__root, font=("Helvetica", 25),
                                     width=5, height=2, bg= self.__widget_color,
                                     fg="#FFFFFF", borderwidth=1, relief=RAISED)

                self.__letter_labels[y][x] = letter_label

                # Place the label into a grid based on its coordinates.
                letter_label.grid(row=y+1, column=x+2, sticky="NESW")

        # ======================================================================
        # Breathing room
        empty_row_top = Label(height=5, bg= self.__bg_color)
        empty_row_top.grid(row=0, column=0, columnspan=10)

        empty_row_middle = Label(height=6, bg= self.__bg_color)
        empty_row_middle.grid(row=8, column=0, columnspan=10)

        # ======================================================================
        # The on-screen keyboard.

        self.__keys = []

        # Initialize the list for keys(key buttons) as None.
        for _ in self.__key_lst:
            self.__keys.append(None)

        for index, key in enumerate(self.__key_lst):
            # Define the function for a key press with
            # the specific key as a parameter.
            def key_press(key_character=key):
                # Key buttons only work (add letters) if word length
                # hasn't been reached.
                if len(self.__input_letters) < WORD_LENGTH:
                    self.__input_letters.append(key_character)
                    self.update_letters()

            # Create a button with the key as text and key_press as command.
            new_button = Button(self.__root, text=key, font=("Helvetica", 22),
                                width=5, height=2, command=key_press,
                                relief=RAISED, bg= self.__widget_color,
                                fg= self.__fg_color)

            # Store the key button in "__keys" with running number as index.
            self.__keys[index] = new_button

            # Make the key button rows match a keyboard.
            if key in ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']:
                row = 9
                column = index % 10
            elif key in ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']:
                row = 10
                column = index % 10
            else:
                row = 11
                column = index % 9

            new_button.grid(row=row, column=column, sticky="NESW")

        # ======================================================================
        # Weighting the window elements.

        for column in range(10):
            self.__root.columnconfigure(column, weight=1)

        for row in range(12):
            self.__root.rowconfigure(row, weight=1)

        # ======================================================================
        # The enter button.
        enter_button = Button(self.__root, text="ENTER", font=("Helvetica", 11),
                              command=self.enter_word, bg= self.__widget_color,
                              fg=self.__fg_color, relief=RAISED)
        enter_button.grid(row=10, column=9, sticky="NESW")

        # ======================================================================
        # The backspace button.
        backspace_button = Button(self.__root, text="←", font=("Helvetica", 20),
                                  command=self.backspace, width=5, height=2,
                                  relief=RAISED, bg= self.__widget_color,
                                  fg=self.__fg_color)
        backspace_button.grid(row=11, column=8, columnspan=2, sticky="NESW")

        # ======================================================================
        # The quit button.
        quit_button = Button(self.__root, text="Quit", font=("Helvetica", 14),
                             command=self.quit, width=5, height=2, relief=RAISED,
                             bg= self.__widget_color, fg=self.__fg_color)
        quit_button.grid(row=11, column=0, sticky="NESW")

        # Try to pick the word being guessed after mainloop is created.
        self.__root.after(600, self.read_file)
        self.__root.mainloop()

    def update_letters(self):
        """Update the current row of the letter matrix for typed letters.
        Called when a button in "__key_lst" or "backspace_button" is clicked."""
        current_row = self.__letter_labels[self.__guess_count]

        # Initialize the current row with empty strings to account
        # for a partial word / backspace.
        for label in current_row:
            label.config(text="")

        # Fill in the currently typed letters.
        for index, letter in enumerate(self.__input_letters):
            current_row[index].config(text=letter)

    def enter_word(self):
        """Check the currently typed word against the correct word and color
        letters accordingly. Called from the "enter_button" widget."""
        # Check a full word is entered and the game isn't already over.
        if len(self.__input_letters) == WORD_LENGTH and not self.__game_over:

            current_row = self.__letter_labels[self.__guess_count]

            try:
                # Create a dictionary for letter counts in word being guessed.
                # Helps make sure the number of times a letter gets colored
                # matches it's count in the word being guessed.
                letter_count = {}
                for letter in self.__word_split:
                    if letter not in letter_count:
                        letter_count[letter] = 1
                    else:
                        letter_count[letter] += 1

                # As a baseline, darken all labels (letters) on current row.
                for index, letter in enumerate(self.__input_letters):
                    current_row[index].config(bg="#404040")

                    self.update_keyboard(letter, "black")

                # Color correct letters in correct slot green. Subtract them
                # from the letter count dictionary.
                for index, letter in enumerate(self.__input_letters):
                    if letter == self.__word_split[index]:
                        current_row[index].config(bg="green")
                        letter_count[letter] -= 1

                        self.update_keyboard(letter, "green")

                # If guess contains a correct letter in wrong slot when correct
                # slots have been taken into account (green), color orange.
                for index, letter in enumerate(self.__input_letters):
                    if letter in self.__word_split:
                        if letter_count[letter] > 0:
                            current_row[index].config(bg="#b38f00")
                            letter_count[letter] -= 1

                            self.update_keyboard(letter, "orange")

                self.__guess_count += 1
                self.is_game_over()
                self.__input_letters = []

            # A TypeError happens if the user tries to continue the game
            # in spite of a problem loading the input file.
            except TypeError as error:
                self.error_popup(error)

    def backspace(self):
        """Remove a letter from the current row of the input matrix.
        Called from the "backspace_button" widget."""
        if len(self.__input_letters) > 0:
            del self.__input_letters[-1]
            self.update_letters()

    def quit(self):
        """Quit the program. Called from all "quit_button" widgets."""
        self.__root.destroy()

    def update_keyboard(self, letter, color):
        """Update the on-screen keyboard colors to match guessed letters."""
        index = self.__key_lst.index(letter)

        # If a letter was in the correct slot (green), color key green.
        if color == "green":
            self.__keys[index].config(bg="green")

        # If a correct letter was in the wrong slot (orange), color key orange.
        elif color == "orange":
            # Check the letter hasn't already been correctly guessed (green).
            if self.__keys[index]["bg"] != "green":
                self.__keys[index].config(bg="#b38f00")

        # Else, a wrong letter was guessed. Darken key button.
        else:
            # Check the letter hasn't already been correctly guessed (green).
            if self.__keys[index]["bg"] != "green":
                self.__keys[index].config(bg="#404040")

    def select_word(self):
        """Pick a word to be guessed from <self.__word_lst>."""
        word = random.choice(self.__word_lst)
        word = word.upper()
        self.__word_split = list(word)
        # Cheat sheet : print(word)

    def read_file(self, filename = WORD_INPUT_FILE):
        """Create a list of possible words for the word being guessed from
        a text file. Errors are turned into pop-ups with func "error_popup()".

        :param filename: str, name of the input file. Default value of
                         WORD_INPUT_FILE is "wordle_wordlist.txt"."""
        # Empty the word list in case of words from a previous read attempt.
        self.__word_lst = []
        try:
            data_file = open(filename, mode="r")

            for line in data_file:
                line = line.rstrip()
                if len(line) != WORD_LENGTH:
                    raise ValueError
                elif not line.isalpha():
                    raise ValueError

                self.__word_lst.append(line)

            data_file.close()
            self.select_word()

        except Exception as error:
            self.error_popup(error)

    def error_popup(self, error):
        """Create an error pop-up when an exception is caught.
        Different error messages are defined for different situations."""
        error_class = error.__class__

        # message = ("title message", "explanation text")

        # ValueError usually from an invalid input file.
        if error_class == ValueError:
            message = ("Error while loading file",
                       "There was an error in loading the input text file. "
                       "\nWords must be five letters and on separate lines.")

        # TypeError is raised if the user continues despite an error message.
        elif error_class == TypeError:
            message = ("The input file can not be read!",
                       "You need to choose a valid input file to continue!")

        elif error_class == FileNotFoundError:
            message = ("Error while loading file",
                       "The default input file \"wordle_wordlist.txt\" was not"
                       " found in program folder.")

        # A general error message for other error types.
        else:
            message = ("My God, My God, Why Hast Thou Forsaken Me?",
                       f"The program ran into an unexpected error: "
                       f"\n\"{error}\"\n "f"You should probably restart it.")

        error_window = Toplevel(self.__root)
        error_window.title(message[0])
        error_window.config(bg=self.__bg_color)

        # ======================================================================
        # Centering the pop-up window, as per the tkinter documentation.
        popup_width, popup_height = 420, 150

        screenwidth = self.__root.winfo_screenwidth()
        screenheight = self.__root.winfo_screenheight()

        x = screenwidth / 2 - popup_width / 2
        y = screenheight / 2 - popup_height / 2

        error_window.geometry('%dx%d+%d+%d' % (popup_width, popup_height, x, y))
        error_window.resizable(False, False)

        # ======================================================================
        # Creating the window widgets.

        def select_file():
            """Open file explorer and try to read selected file."""
            filename = fd.askopenfilename(title="Select an input file")
            self.read_file(filename)

        explanation_label = Label(error_window, text=message[1], font=12,
                                  wraplength=370, bg=self.__bg_color,
                                  fg=self.__fg_color)
        explanation_label.pack(expand=TRUE, fill=BOTH)

        quit_button = Button(error_window, text="Quit", font=("Helvetica", 12),
                             command=self.quit, bg=self.__widget_color,
                             fg=self.__fg_color)
        quit_button.pack(side=LEFT, expand=TRUE, fill=BOTH, pady=10, padx=10,
                         ipady=10, ipadx=10)

        open_button = Button(error_window, text="Choose a new input file",
                             font=12, command=select_file,
                             bg=self.__widget_color, fg=self.__fg_color)
        open_button.pack(side=LEFT, expand=TRUE, fill=BOTH, pady=10, padx=10,
                         ipady=10, ipadx=20)

        error_window.mainloop()

    def restart(self):
        """Restart the game by resetting the changed attributes."""
        for row in self.__letter_labels:
            for label in row:
                label.config(text="", bg=self.__widget_color)

        for key in self.__keys:
            key.config(bg=self.__widget_color)

        self.__guess_count = 0
        self.__input_letters = []
        self.__game_over = False
        # Pick a new word to guess.
        self.select_word()

    def is_game_over(self):
        """Create a pop-up window when the game is over. The window has buttons
        for quitting and starting a new game."""
        # Check if the word is correct or the player is out of guesses.
        if self.__input_letters == self.__word_split or self.__guess_count == 6:
            self.__game_over = True

            if self.__input_letters == self.__word_split:
                title_msg = "You win!"
                explain_msg = "You guessed it!"
            elif self.__guess_count == 6:
                title_msg = "Better luck next time!"
                explain_msg = "Out of guesses!"

            win_window = Toplevel(self.__root)
            win_window.title(title_msg)

            win_window.config(bg=self.__bg_color)

            # ==================================================================
            # Centering the pop-up window, as per the tkinter documentation.
            popup_width, popup_height = 420, 150

            screenwidth = self.__root.winfo_screenwidth()
            screenheight = self.__root.winfo_screenheight()

            x = screenwidth / 2 - popup_width / 2
            y = screenheight / 2 - popup_height / 2

            win_window.geometry('%dx%d+%d+%d' % (popup_width, popup_height, x, y))
            win_window.resizable(False, False)

            # ==================================================================
            # Creating the window widgets.

            def restart_btn():
                win_window.destroy()
                self.restart()

            explanation_label = Label(win_window, text=explain_msg,
                                      font=("Helvetica", 15),
                                      bg=self.__bg_color, fg=self.__fg_color)
            explanation_label.pack(expand=TRUE, fill=BOTH)

            quit_button = Button(win_window, text="Quit",
                                 font=("Helvetica", 15), command=self.quit,
                                 bg=self.__widget_color, fg=self.__fg_color)
            quit_button.pack(side=LEFT, expand=TRUE, fill=BOTH, pady=10,
                             padx=10, ipady=10, ipadx=10)

            restart_button = Button(win_window, text="New game",
                                    font=("Helvetica", 15), command=restart_btn,
                                    bg=self.__widget_color, fg=self.__fg_color)
            restart_button.pack(side=LEFT, expand=TRUE, fill=BOTH, pady=10,
                                padx=10, ipady=10, ipadx=10)

            win_window.mainloop()


def main():
    Wordle()


if __name__ == "__main__":
    main()
