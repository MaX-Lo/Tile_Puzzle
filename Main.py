import pygame
import random
from pygame.locals import *

import Constants as const

# created by MaX-Lo
# on 14.03.2016


def main():
    """
    init screen and pygame
    """
    screen = pygame.display.set_mode((450, 550))
    pygame.display.set_caption("Tile Puzzle")
    pygame.init()

    menu(screen)


def menu(screen):
    """ Game menu """

    # creating the menu background
    menu_bg = pygame.Surface(screen.get_size())
    menu_bg = menu_bg.convert()
    menu_bg.fill(const.GREY)

    # Menu Loop
    m_running = True
    selection = 0  # which menu item is highlighted
    clock = pygame.time.Clock()
    while m_running:
        clock.tick(20)

        # handle input events
        for event in pygame.event.get():
            if event.type == QUIT:
                m_running = False
            elif event.type == MOUSEBUTTONUP:
                # TODO support mouse control
                pass
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                m_running = False
            elif event.type == KEYDOWN and event.key == K_UP:
                selection -= 1
            elif event.type == KEYDOWN and event.key == K_DOWN:
                selection += 1
            elif event.type == KEYUP and event.key == K_RETURN:
                if selection == 0:
                    game(screen)
                elif selection == 1:
                    pass
                elif selection == 2:
                    m_running = False

        # adjust item selection if out of range
        if selection > 2:
            selection = 0
        elif selection < 0:
            selection = 2

        # refresh screen
        screen.blit(menu_bg, (0, 0))
        menu_item(screen, "Puzzle", 50, 50, selection == 0)
        menu_item(screen, "Nothing", 50, 170, selection == 1)
        menu_item(screen, "Quit", 50, 290, selection == 2)

        pygame.display.flip()


def menu_item(screen, text, x, y, selected):
    """ Creates a menu item
    :param text: text of the menu item
    :param x, y: Top left corner
    :param selected: true or false"""
    if selected:
        pygame.draw.rect(screen, const.WHITE, (x, y, screen.get_width() - 2 * x, 100))
    else:
        pygame.draw.rect(screen, const.DK_GREY, (x, y, screen.get_width() - 2 * x, 100))
    pygame.draw.rect(screen, const.LT_GREY, (x + 10, y + 10, screen.get_width() - (x + 10) * 2, 80))
    font = pygame.font.Font(None, 80)
    mytext = font.render(text, 1, const.DK_GREY)
    textpos = mytext.get_rect(centerx=screen.get_width() / 2, y=y + 20)
    screen.blit(mytext, textpos)


def game(screen):
    # creating a new random filled field
    # ef is the empty field position
    field, ef = create_game_field()
    # Create The Background
    board = pygame.Surface((const.SIZE*100, const.SIZE*100))
    board = board.convert()
    board.fill(const.WHITE)

    steps = 0

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if ef[1] + 1 != const.SIZE:
                        steps += 1
                        field[ef[0]][ef[1]], field[ef[0]][ef[1] + 1] = field[ef[0]][ef[1] + 1], field[ef[0]][ef[1]]
                        ef_old = ef  # setting old empty field
                        ef = (ef[0], ef[1] + 1)  # getting new empty field
                        animation_up_linear(ef, ef_old, board, screen, field) # simple shifting animation
                elif event.key == K_DOWN:
                    if ef[1] != 0:
                        steps += 1
                        field[ef[0]][ef[1]], field[ef[0]][ef[1] - 1] = field[ef[0]][ef[1] - 1], field[ef[0]][ef[1]]
                        ef_old = ef
                        ef = (ef[0], ef[1] - 1)
                        animation_down_linear(ef, ef_old, board, screen, field)
                elif event.key == K_LEFT:
                    if ef[0] + 1 != const.SIZE:
                        steps += 1
                        field[ef[0]][ef[1]], field[ef[0] + 1][ef[1]] = field[ef[0] + 1][ef[1]], field[ef[0]][ef[1]]
                        ef_old = ef
                        ef = (ef[0] + 1, ef[1])
                        animation_left_linear(ef, ef_old, board, screen, field)
                elif event.key == K_RIGHT:
                    if ef[0] != 0:
                        steps += 1
                        field[ef[0]][ef[1]], field[ef[0] - 1][ef[1]] = field[ef[0] - 1][ef[1]], field[ef[0]][ef[1]]
                        ef_old = ef
                        ef = (ef[0] - 1, ef[1])
                        animation_right_linear(ef, ef_old, board, screen, field)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    running = False

        # Debug info: [[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,0]] would be the goal for a 4x4 field
        if test_winning(field):
            print "VICTORY!!!"
            running = False

        board.fill(const.LT_GREY)
        for i in range(const.SIZE):
            for j in range(const.SIZE):
                if field[i][j] == 0:
                    pygame.draw.rect(board, const.LT_GREY, (i * 100 + 1, j * 100 + 1, 98, 98))
                else:
                    pygame.draw.rect(board, const.DK_GREY, (i * 100 + 1, j * 100 + 1, 98, 98))
                    font = pygame.font.Font(None, 50)
                    mytext = font.render(str(field[i][j]), 1, const.WHITE)
                    textpos = mytext.get_rect(centerx=i * 100 + 50, centery=j * 100 + 50)
                    board.blit(mytext, textpos)

        screen.fill(const.GREY)
        board_x = (screen.get_width()-board.get_width())/2
        show_steps(screen, steps, (board_x, 20))
        time = round(pygame.time.get_ticks()/1000)
        show_time(screen, time, (board_x, 50))

        refresh_screen(screen, board)


def refresh_screen(screen, board):
    board_x = (screen.get_width()-board.get_width())/2
    screen.blit(board, (board_x, 100))
    pygame.display.flip()


def show_steps(screen, steps, (x, y)):
    font = pygame.font.Font(None, 25)
    text = font.render("Steps: {0}".format(steps), 1, const.WHITE)
    textpos = text.get_rect(x=x, y=y)
    screen.blit(text, textpos)


def show_time(screen, time, (x, y)):
    font = pygame.font.Font(None, 25)
    text = font.render("Time: {0}".format(time)+" sec", 1, const.WHITE)
    textpos = text.get_rect(x=x, y=y)
    screen.blit(text, textpos)


def create_game_field():
    """
    generates the field filled with unique random numbers
    :return: field filled with numbers, position of the empty field
    """
    # init int array
    field = [[0 for i in range(const.SIZE)] for i in range(const.SIZE)]
    empty_field = None

    # set array elements with unique random numbers
    for i in range(const.SIZE):
        for j in range(const.SIZE):
            searching_unused_number = True
            number = 0
            # create random numbers until an unused number is created
            while searching_unused_number:
                number = random.randint(1, const.SIZE ** 2)
                searching_unused_number = False
                for k in range(const.SIZE):
                    for l in range(const.SIZE):
                        if int(field[k][l]) == number:
                            searching_unused_number = True
            field[i][j] = number

    # set array element with highest number 0 -> empty field
    for i in range(const.SIZE):
        for j in range(const.SIZE):
            if field[i][j] == const.SIZE ** 2:
                field[i][j] = 0
                empty_field = (i, j)

    print "New field: "
    print field
    return field, empty_field


def test_winning(field):
    number = 1
    for i in range(const.SIZE):
        for j in range(const.SIZE):
            if field[j][i] != number:
                return False
            number += 1
            # last field is empty
            if number == const.SIZE ** 2:
                return True
    return True


# a lot of animation stuff to make the game look better
def animation_right_linear(ef, ef_old, board, screen, field):
    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT_GREY, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT_GREY, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK_GREY, (ef[0] * 100 + i, ef[1] * 100 + 1, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50 + i, centery=ef[1] * 100 + 50)
        board.blit(mytext, textpos)
        refresh_screen(screen, board)


def animation_left_linear(ef, ef_old, board, screen, field):
    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT_GREY, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT_GREY, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK_GREY, (ef[0] * 100 - i, ef[1] * 100 + 1, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50 - i, centery=ef[1] * 100 + 50)
        board.blit(mytext, textpos)
        refresh_screen(screen, board)


def animation_up_linear(ef, ef_old, board, screen, field):
    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT_GREY, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT_GREY, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK_GREY, (ef[0] * 100 + 1, ef[1] * 100 + 1 - i, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50, centery=ef[1] * 100 + 50 - i)
        board.blit(mytext, textpos)
        refresh_screen(screen, board)


def animation_down_linear(ef, ef_old, board, screen, field):
    clock2 = pygame.time.Clock()
    for i in range(const.ANIMATION_SPEED):
        i *= 100 / const.ANIMATION_SPEED
        clock2.tick(60)
        # draw old and new empty Tile
        pygame.draw.rect(board, const.LT_GREY, (ef[0] * 100 + 1, ef[1] * 100 + 1, 98, 98))
        pygame.draw.rect(board, const.LT_GREY, (ef_old[0] * 100 + 1, ef_old[1] * 100 + 1, 98, 98))
        # draw shifting number tile
        pygame.draw.rect(board, const.DK_GREY, (ef[0] * 100 + 1, ef[1] * 100 + 1 + i, 98, 98))
        font = pygame.font.Font(None, 50)
        mytext = font.render(str(field[ef_old[0]][ef_old[1]]), 1, const.WHITE)
        textpos = mytext.get_rect(centerx=ef[0] * 100 + 50, centery=ef[1] * 100 + 50 + i)
        board.blit(mytext, textpos)
        refresh_screen(screen, board)

if __name__ == '__main__':
    main()
