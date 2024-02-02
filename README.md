# Discount-Wordle
A Wordle clone, originally made as the final project of my first programming course. Based on [Wordle](https://www.nytimes.com/games/wordle/index.html) by Josh Wardle.

![alt text](https://github.com/KalleLahtinen/materials/blob/main/discount_wordle.png?raw=true)

## About the project

The game first picks a random word from a list of same-length words. A default word file "wordle_wordllist.txt" is assumed in project folder, but the game will ask for a different file if it's not found. The player then proceeds guessing the word in six tries. 

With each guess, the correctly guessed letters in the correct place will be colored green, the correct letters in the wrong place orange and wrong letters will be darkened. If the player runs out of guesses or guesses correctly, a pop-up window shows up and lets the player either quit or start a new game.

The graphical user interface was made using Tkinter. It supports adaptive window resizing and stretching. You can also change the length of the guessed word by changing the global WORD_LENGTH variable and providing a file with matching length words.