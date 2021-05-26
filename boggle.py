"""Utilities related to Boggle game."""

from random import choice, shuffle
import string


class Boggle():

    def __init__(self):
        self.words = self.read_dict("words.txt")
        self.dim = 5
        self.DICE4 = [
            ['A', 'E', 'A', 'N', 'E', 'G'], ['W', 'N', 'G', 'E', 'E', 'H'],
            ['A', 'H', 'S', 'P', 'C', 'O'], ['L', 'N', 'H', 'N', 'R', 'Z'],
            ['A', 'S', 'P', 'F', 'F', 'K'], ['T', 'S', 'T', 'I', 'Y', 'D'],
            ['O', 'B', 'J', 'O', 'A', 'B'], ['O', 'W', 'T', 'O', 'A', 'T'],
            ['I', 'O', 'T', 'M', 'U', 'C'], ['E', 'R', 'T', 'T', 'Y', 'L'],
            ['R', 'Y', 'V', 'D', 'E', 'L'], ['T', 'O', 'E', 'S', 'S', 'I'],
            ['L', 'R', 'E', 'I', 'X', 'D'], ['T', 'E', 'R', 'W', 'H', 'V'],
            ['E', 'I', 'U', 'N', 'E', 'S'], ['N', 'U', 'I', 'H', 'M', 'Q']]
        self.DICE5 = [
            ['A', 'A', 'A', 'F', 'R', 'S'], ['A', 'A', 'E', 'E', 'E', 'E'],
            ['A', 'A', 'F', 'I', 'R', 'S'], ['A', 'D', 'E', 'N', 'N', 'N'],
            ['A', 'E', 'E', 'E', 'E', 'M'], ['A', 'E', 'E', 'G', 'M', 'U'],
            ['A', 'E', 'G', 'M', 'N', 'N'], ['A', 'F', 'I', 'R', 'S', 'Y'],
            ['B', 'J', 'K', 'Q', 'X', 'Z'], ['C', 'C', 'E', 'N', 'S', 'T'],
            ['C', 'E', 'I', 'I', 'L', 'T'], ['C', 'E', 'I', 'L', 'P', 'T'],
            ['C', 'E', 'I', 'P', 'S', 'T'], ['D', 'D', 'H', 'N', 'O', 'T'],
            ['D', 'H', 'H', 'L', 'O', 'R'], ['D', 'H', 'L', 'N', 'O', 'R'],
            ['D', 'H', 'L', 'N', 'O', 'R'], ['E', 'I', 'I', 'I', 'T', 'T'],
            ['E', 'M', 'O', 'T', 'T', 'T'], ['E', 'N', 'S', 'S', 'S', 'U'],
            ['F', 'I', 'P', 'R', 'S', 'Y'], ['G', 'O', 'R', 'R', 'V', 'W'],
            ['I', 'P', 'R', 'R', 'R', 'Y'], ['N', 'O', 'O', 'T', 'U', 'W'],
            ['O', 'O', 'O', 'T', 'T', 'U']]
        

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""

        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        dict_file.close()
        return words

    def make_board(self, board_size):
        """Make and return a random boggle board."""
        self.dim = board_size
        board = []
        (DICE4, DICE5) = (self.DICE4.copy(), self.DICE5.copy())
            
        Dice = DICE4 if self.dim == 4 else DICE5
        shuffle(Dice)
        
        for y in range(self.dim):
            row = [choice(Dice.pop()) for i in range(self.dim)]
            board.append(row)

        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""
        
        word_exists = word in self.words
        valid_word = self.find(board, word.upper())

        if word_exists and valid_word:
            result = "You got one!"
        elif word_exists and not valid_word:
            result = "Not on board"
        else:
            result = "Not a word"

        return result

    def find_from(self, board, word, y, x, seen):
        """Can we find a word on board, starting at x, y?"""
        dim_idx = self.dim -1

        if x > dim_idx or y > dim_idx:
            return

        # This is called recursively to find smaller and smaller words
        # until all tries are exhausted or until success.

        # Base case: this isn't the letter we're looking for.

        if board[y][x] != word[0]:
            return False

        # Base case: we've used this letter before in this current path

        if (y, x) in seen:
            return False

        # Base case: we are down to the last letter --- so we win!

        if len(word) == 1:
            return True

        # Otherwise, this letter is good, so note that we've seen it,
        # and try of all of its neighbors for the first letter of the
        # rest of the word
        # This next line is a bit tricky: we want to note that we've seen the
        # letter at this location. However, we only want the child calls of this
        # to get that, and if we used `seen.add(...)` to add it to our set,
        # *all* calls would get that, since the set is passed around. That would
        # mean that once we try a letter in one call, it could never be tried again,
        # even in a totally different path. Therefore, we want to create a *new*
        # seen set that is equal to this set plus the new letter. Being a new
        # object, rather than a mutated shared object, calls that don't descend
        # from us won't have this `y,x` point in their seen.
        #
        # To do this, we use the | (set-union) operator, read this line as
        # "rebind seen to the union of the current seen and the set of point(y,x))."
        #
        # (this could be written with an augmented operator as "seen |= {(y, x)}",
        # in the same way "x = x + 2" can be written as "x += 2", but that would seem
        # harder to understand).

        seen = seen | {(y, x)}

        # adding diagonals

        if y > 0:
            if self.find_from(board, word[1:], y - 1, x, seen):
                return True

        if y < dim_idx:
            if self.find_from(board, word[1:], y + 1, x, seen):
                return True

        if x > 0:
            if self.find_from(board, word[1:], y, x - 1, seen):
                return True

        if x < dim_idx:
            if self.find_from(board, word[1:], y, x + 1, seen):
                return True

        # diagonals
        if y > 0 and x > 0:
            if self.find_from(board, word[1:], y - 1, x - 1, seen):
                return True

        if y < dim_idx and x < dim_idx:
            if self.find_from(board, word[1:], y + 1, x + 1, seen):
                return True

        if x > 0 and y < dim_idx:
            if self.find_from(board, word[1:], y + 1, x - 1, seen):
                return True

        if x < dim_idx and y > 0:
            if self.find_from(board, word[1:], y - 1, x + 1, seen):
                return True
        # Couldn't find the next letter, so this path is dead

        return False

    def find(self, board, word):
        """Can word be found in board?"""

        # Find starting letter --- try every spot on board and,
        # win fast, should we find the word at that place.

        for y in range(0, self.dim):
            for x in range(0, self.dim):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        # We've tried every path from every starting square w/o luck.
        # Sad panda.

        return False
