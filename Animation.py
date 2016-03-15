import pygame
import random

import Constants as const

# created by Max-Lo on 15.03.2016
# methods to animate the puzzle a little bit
# to improve or tune the look a bit


# a lot of animation stuff to make the game look better
def animation_right_linear(board, screen, puzzle):
    field = puzzle.field
    ef = puzzle.empty_field
    ef_old = (puzzle.empty_field[0] + 1, puzzle.empty_field[1])

    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK, (ef[0] * 100 + i, ef[1] * 100 + 1, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50 + i, centery=ef[1] * 100 + 50)
        board.blit(mytext, textpos)
        screen.blit(board, (25, 100))
        pygame.display.flip()


def animation_left_linear(board, screen, puzzle):
    field = puzzle.field
    ef = puzzle.empty_field
    ef_old = (puzzle.empty_field[0] - 1, puzzle.empty_field[1])

    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK, (ef[0] * 100 - i, ef[1] * 100 + 1, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50 - i, centery=ef[1] * 100 + 50)
        board.blit(mytext, textpos)
        screen.blit(board, (25, 100))
        pygame.display.flip()


def animation_up_linear(board, screen, puzzle):
    field = puzzle.field
    ef = puzzle.empty_field
    ef_old = (puzzle.empty_field[0], puzzle.empty_field[1] - 1)

    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK, (ef[0] * 100 + 1, ef[1] * 100 + 1 - i, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50, centery=ef[1] * 100 + 50 - i)
        board.blit(mytext, textpos)
        screen.blit(board, (25, 100))
        pygame.display.flip()


def animation_down_linear(board, screen, puzzle):
    field = puzzle.field
    ef = puzzle.empty_field
    ef_old = (puzzle.empty_field[0], puzzle.empty_field[1] + 1)

    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK, (ef[0] * 100 + 1, ef[1] * 100 + 1 + i, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50, centery=ef[1] * 100 + 50 + i)
        board.blit(mytext, textpos)
        screen.blit(board, (25, 100))
        pygame.display.flip()


def animation_tremble(screen, board, blank_screen):
    clock = pygame.time.Clock()
    for i in range(15):
        clock.tick(60)

        screen.blit(blank_screen, (0, 0))

        board_x = 25 + random.randint(-10, 10)
        board_y = 100 + random.randint(-10, 10)
        screen.blit(board, (board_x, board_y))
        pygame.display.flip()
