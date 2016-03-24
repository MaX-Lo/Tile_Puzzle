from pygame.locals import *

# created by MaX-Lo
# on 14.03.2016
import time

from Animation import *
from Puzzle import Puzzle
from Scoreboard import Scoreboard
import Constants as Const


def main():
    """
    init screen and pygame
    """
    screen = pygame.display.set_mode((Const.SIZE * 100 + 50, Const.SIZE * 100 + 150))
    pygame.display.set_caption("Tile Puzzle")
    pygame.init()

    menu(screen)


def menu(screen):
    """ Game menu """
    # creating the menu background
    menu_bg = pygame.Surface(screen.get_size())
    menu_bg = menu_bg.convert()
    menu_bg.fill(Const.MD)

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
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                m_running = False
            elif event.type == KEYUP:
                if event.key == K_UP:
                    selection -= 1
                elif event.key == K_DOWN:
                    selection += 1
                elif event.key == K_PLUS or event.key == K_KP_PLUS:
                    if Const.SIZE < 6:
                        Const.SIZE += 1
                elif event.key == K_MINUS or event.key == K_KP_MINUS:
                    if Const.SIZE > 3:
                        Const.SIZE -= 1
                elif event.key == K_RETURN:
                    if selection == 0:
                        game()
                        menu_bg = pygame.Surface(screen.get_size())
                    elif selection == 1:
                        Const.SIZE += 1
                        if Const.SIZE == 7:
                            Const.SIZE = 3
                    elif selection == 2:
                        m_running = False

        # adjust item selection if out of range
        if selection > 2:
            selection = 0
        elif selection < 0:
            selection = 2

        # refresh screen
        screen.blit(menu_bg, (0, 0))
        menu_bg.fill(Const.MD)
        menu_item(screen, "Puzzle", 50, 50, selection == 0)
        menu_item(screen, "-  " + str(Const.SIZE) + "  +", 50, 170, selection == 1)
        menu_item(screen, "Quit", 50, 290, selection == 2)

        pygame.display.flip()


def menu_item(screen, text, x, y, selected):
    """ Creates a menu item
    :param text: text of the menu item
    :param x, y: Top left corner
    :param selected: true or false"""
    if selected:
        pygame.draw.rect(screen, Const.WHITE, (x, y, screen.get_width() - 2 * x, 100))
    else:
        pygame.draw.rect(screen, Const.DK, (x, y, screen.get_width() - 2 * x, 100))
    pygame.draw.rect(screen, Const.LT, (x + 10, y + 10, screen.get_width() - (x + 10) * 2, 80))
    font = pygame.font.Font(None, 80)
    mytext = font.render(text, 1, Const.DK)
    textpos = mytext.get_rect(centerx=screen.get_width() / 2, y=y + 20)
    screen.blit(mytext, textpos)


def game():
    screen = pygame.display.set_mode((Const.SIZE * 100 + 50, Const.SIZE * 100 + 150))
    # creating a new random filled field
    # ef is the empty field position
    puzzle = Puzzle()

    # Create The Background
    board = pygame.Surface((Const.SIZE * 100, Const.SIZE * 100))
    board = board.convert()
    board.fill(Const.WHITE)

    steps = 0
    time0 = time.time()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        t = time.time() - time0
        blank_screen = get_screen_without_puzzle(screen, steps, t)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONUP:
                puzzle.click(pygame.mouse.get_pos(), board, blank_screen)
            elif event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    if puzzle.move_tile_up(board, blank_screen):
                        steps += 1
                elif event.key == K_DOWN or event.key == K_s:
                    if puzzle.move_tile_down(board, blank_screen):
                        steps += 1
                elif event.key == K_LEFT or event.key == K_a:
                    if puzzle.move_tile_left(board, blank_screen):
                        steps += 1
                elif event.key == K_RIGHT or event.key == K_d:
                    if puzzle.move_tile_right(board, blank_screen):
                        steps += 1
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    running = False

        puzzle.draw(board)

        if puzzle.is_solved():
        #if True:
            print "VICTORY!!!"
            show_winning_screen(screen, board, puzzle, steps, t)
            show_scoreboard(steps, t)
            running = False
        else:
            if puzzle.refresh_num_at_correct_pos():
                change_theme()

        screen.blit(get_screen_without_puzzle(screen, steps, t), (0, 0))
        screen.blit(board, (25, 100))
        pygame.display.flip()


def get_screen_without_puzzle(screen, steps, time):
    s = pygame.Surface(screen.get_size())
    s = s.convert()
    s.fill(Const.MD)
    show_steps(s, steps, (25, 20))
    show_time(s, time, (25, 50))
    return s


def change_theme():
    red = random.randint(0, 90)
    green = random.randint(0, 90)
    blue = random.randint(0, 90)
    Const.LT = (red + 90, green + 90, blue + 90)
    Const.DK = (red, green, blue)
    Const.MD = (red + 10, green + 10, blue + 10)


def show_steps(screen, steps, (x, y)):
    font = pygame.font.Font(None, 25)
    text = font.render("Steps: {0}".format(steps), 1, Const.WHITE)
    textpos = text.get_rect(x=x, y=y)
    screen.blit(text, textpos)


def show_time(screen, time, (x, y)):
    font = pygame.font.Font(None, 25)
    time = round(time, 1)
    text = font.render("Time: {0}".format(time) +" sec", 1, Const.WHITE)
    textpos = text.get_rect(x=x, y=y)
    screen.blit(text, textpos)


def show_winning_screen(screen, board, puzzle, steps, t):
    clock = pygame.time.Clock()
    i = 2
    running = True
    count = 0

    # experimental graphics effects
    init_particle_spring(screen)

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    running = False

        # refresh puzzle color
        if count == 10:
            puzzle.draw_colorful(board)
            count = 0
        else:
            count += 1

        screen.blit(get_screen_without_puzzle(screen, steps, t), (0, 0))

        screen.blit(board, (25, 100))
        # draw "Solved" caption
        font = pygame.font.Font(None, Const.SIZE * 50)

        text = font.render("Solved", 1, Const.WHITE)
        textpos = text.get_rect(centerx=screen.get_width()/2, centery=screen.get_height()/2)
        screen.blit(text, textpos)

        # updates the particle spring
        animation_particle_spring(screen)

        # refresh Screen
        pygame.display.flip()


def show_scoreboard(steps, time):
    filename = "highscore" + str(Const.SIZE) + "x" + str(Const.SIZE) + ".dat"
    scoreboard = Scoreboard( filename)
    scoreboard.set_bg_color(Const.MD)
    scoreboard.set_border_color(Const.DK)
    scoreboard.set_table_color(Const.LT)
    scoreboard.add("", 0, steps, 0, round(time, 2))

if __name__ == '__main__':
    main()
