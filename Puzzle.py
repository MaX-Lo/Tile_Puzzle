import pygame
import random

import Constants as Const


# created by MaX-Lo on 15.03.2016
# contains puzzle with methods to create new puzzles, move tiles and so on...


class Puzzle:
    def __init__(self):
        self.field = None
        self.empty_field = None
        self.size = Const.SIZE
        self.num_at_correct_pos = -1

        self.create_puzzle()
        while not self.is_solvable():
            self.create_puzzle()

        self.refresh_num_at_correct_pos()

    def create_puzzle(self):
        """
        generates the field filled with unique random numbers
        """
        # init int array
        field = [[0 for _ in range(self.size)] for i in range(self.size)]
        empty_field = None

        # set array elements with unique random numbers
        for i in range(self.size):
            for j in range(self.size):
                searching_unused_number = True
                number = 0
                # create random numbers until an unused number is created
                while searching_unused_number:
                    number = random.randint(1, self.size ** 2)
                    searching_unused_number = False
                    for k in range(self.size):
                        for l in range(self.size):
                            if int(field[k][l]) == number:
                                searching_unused_number = True
                field[i][j] = number

        # set array element with highest number 0 -> empty field
        for i in range(self.size):
            for j in range(self.size):
                if field[i][j] == self.size ** 2:
                    field[i][j] = 0
                    empty_field = (i, j)

        self.field = field
        self.empty_field = empty_field

    def refresh_num_at_correct_pos(self):
        """ checks how many tiles are at their final (correct) position """
        number = 1
        correct = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.field[j][i] == number:
                    correct += 1
                number += 1
                # last field is empty
                if number == self.size ** 2:
                    continue
        if self.num_at_correct_pos != correct:
            self.num_at_correct_pos = correct
            return True
        else:
            return False

    def move_tile_up(self):
        if self.empty_field[1] + 1 != self.size:
            self.field[self.empty_field[0]][self.empty_field[1]], self.field[self.empty_field[0]][
                self.empty_field[1] + 1] = \
                self.field[self.empty_field[0]][self.empty_field[1] + 1], self.field[self.empty_field[0]][
                    self.empty_field[1]]

            self.empty_field = (self.empty_field[0], self.empty_field[1] + 1)  # getting new empty field
            return True
        else:
            return False

    def move_tile_down(self):
        if self.empty_field[1] - 1 >= 0:
            self.field[self.empty_field[0]][self.empty_field[1]], self.field[self.empty_field[0]][
                self.empty_field[1] - 1] = \
                self.field[self.empty_field[0]][self.empty_field[1] - 1], self.field[self.empty_field[0]][
                    self.empty_field[1]]

            self.empty_field = (self.empty_field[0], self.empty_field[1] - 1)  # getting new empty field
            return True
        else:
            return False

    def move_tile_right(self):
        if self.empty_field[0] - 1 >= 0:
            self.field[self.empty_field[0]][self.empty_field[1]], self.field[self.empty_field[0] - 1][
                self.empty_field[1]] = \
                self.field[self.empty_field[0] - 1][self.empty_field[1]], self.field[self.empty_field[0]][
                    self.empty_field[1]]

            self.empty_field = (self.empty_field[0] - 1, self.empty_field[1])  # getting new empty field
            return True
        else:
            return False

    def move_tile_left(self):
        if self.empty_field[0] + 1 != self.size:
            self.field[self.empty_field[0]][self.empty_field[1]], self.field[self.empty_field[0] + 1][
                self.empty_field[1]] = \
                self.field[self.empty_field[0] + 1][self.empty_field[1]], self.field[self.empty_field[0]][
                    self.empty_field[1]]

            self.empty_field = (self.empty_field[0] + 1, self.empty_field[1])  # getting new empty field
            return True
        else:
            return False

    def draw(self, board):
        board.fill(Const.LT)
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 0:
                    pygame.draw.rect(board, Const.LT, (i * 100 + 1, j * 100 + 1, 98, 98))
                else:
                    pygame.draw.rect(board, Const.DK, (i * 100 + 1, j * 100 + 1, 98, 98))
                    font = pygame.font.Font(None, 50)
                    mytext = font.render(str(self.field[i][j]), 1, Const.WHITE)
                    textpos = mytext.get_rect(centerx=i * 100 + 50, centery=j * 100 + 50)
                    board.blit(mytext, textpos)

    def draw_colorful(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 0:
                    pygame.draw.rect(board, Const.LT, (i * 100 + 1, j * 100 + 1, 98, 98))
                else:
                    red = random.randint(0, 90)
                    green = random.randint(0, 90)
                    blue = random.randint(0, 90)
                    color = (red, green, blue)
                    pygame.draw.rect(board, color, (i * 100 + 1, j * 100 + 1, 98, 98))
                    font = pygame.font.Font(None, 50)
                    mytext = font.render(str(self.field[i][j]), 1, Const.WHITE)
                    textpos = mytext.get_rect(centerx=i * 100 + 50, centery=j * 100 + 50)
                    board.blit(mytext, textpos)

    def is_solvable(self):
        """
        Not every puzzle is solvable therefore this method test the current puzzle.
        :return: whether puzzle is solvable
        """
        l = []
        # writing all numbers row by row into one list (not necessary, but makes the following step easier)
        empty_field_row = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.field[j][i] != 0:
                    l.append(self.field[j][i])
                else:
                    empty_field_row = i + 1

        # getting the number of unsorted pairs and row of the empty field
        unsorted_pairs = 0
        for pos in range(len(l)):
            for i in range(0, pos):
                if l[pos] < l[i]:
                    unsorted_pairs += 1

        # even size: unsorted_pairs + empty_field_row = even -> solvable
        # odd size: unsorted_pairs = even -> solvable
        if self.size % 2 == 0:  # even
            if (unsorted_pairs + empty_field_row) % 2 == 0:
                return True
            else:
                return False
        else:  # odd
            if unsorted_pairs % 2 == 0:
                return True
            else:
                return False

    def is_solved(self):
        """
        checks wether the puzzle is solved
        :return: true if puzzle is solved
        """
        number = 1
        for i in range(self.size):
            for j in range(self.size):
                if self.field[j][i] != number:
                    return False
                number += 1
                # last field should be empty
                if number == self.size ** 2:
                    return True
        return True
