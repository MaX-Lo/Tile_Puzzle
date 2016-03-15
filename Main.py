
from pygame.locals import *


# created by MaX-Lo
# on 14.03.2016
from Animation import *
from Puzzle import Puzzle
from Scoreboard import Scoreboard





def main():
    """
    init screen and pygame
    """
    screen = pygame.display.set_mode((const.SIZE*100 + 50, const.SIZE * 100 + 150))
    pygame.display.set_caption("Tile Puzzle")
    pygame.init()

    menu(screen)


def menu(screen):
    """ Game menu """

    # creating the menu background
    menu_bg = pygame.Surface(screen.get_size())
    menu_bg = menu_bg.convert()
    menu_bg.fill(const.MD)

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
        menu_bg.fill(const.MD)
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
        pygame.draw.rect(screen, const.DK, (x, y, screen.get_width() - 2 * x, 100))
    pygame.draw.rect(screen, const.LT, (x + 10, y + 10, screen.get_width() - (x + 10) * 2, 80))
    font = pygame.font.Font(None, 80)
    mytext = font.render(text, 1, const.DK)
    textpos = mytext.get_rect(centerx=screen.get_width() / 2, y=y + 20)
    screen.blit(mytext, textpos)


def game(screen):

    # creating a new random filled field
    # ef is the empty field position
    puzzle = Puzzle()

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
                    if puzzle.move_tile_up():
                        steps += 1
                        animation_up_linear(board, screen, puzzle)  # simple shifting animation
                    else:
                        animation_tremble(screen, board, get_screen_without_puzzle(screen, steps, time))

                elif event.key == K_DOWN:
                    if puzzle.move_tile_down():
                        steps += 1
                        animation_down_linear(board, screen, puzzle)
                    else:
                        animation_tremble(screen, board, get_screen_without_puzzle(screen, steps, time))

                elif event.key == K_LEFT:
                    if puzzle.move_tile_left():
                        steps += 1
                        animation_left_linear(board, screen, puzzle)
                    else:
                        animation_tremble(screen, board, get_screen_without_puzzle(screen, steps, time))

                elif event.key == K_RIGHT:
                    if puzzle.move_tile_right():
                        steps += 1
                        animation_right_linear(board, screen, puzzle)
                    else:
                        animation_tremble(screen, board, get_screen_without_puzzle(screen, steps, time))

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    running = False

        board.fill(const.LT)
        puzzle.draw(board)

        # Debug info: [[1,5,9,13],[2,6,10,14],[3,7,11,15],[4,8,12,0]] would be the goal for a 4x4 field
        if puzzle.is_solved():
            print "VICTORY!!!"
            show_winning_screen(screen, board, puzzle)
            scoreboard = Scoreboard(screen)
            scoreboard.add("", 0, steps, 0, time)
            running = False
        else:
            if puzzle.refresh_num_at_correct_pos():
                change_theme()

        time = round(pygame.time.get_ticks()/1000)

        screen.blit(get_screen_without_puzzle(screen, steps, time), (0, 0))
        screen.blit(board, (25, 100))
        pygame.display.flip()


def get_screen_without_puzzle(screen, steps, time):
    s = pygame.Surface(screen.get_size())
    s = s.convert()
    s.fill(const.MD)
    show_steps(s, steps, (25, 20))
    show_time(s, time, (25, 50))
    return s


def change_theme():
    red = random.randint(0, 90)
    green = random.randint(0, 90)
    blue = random.randint(0, 90)
    const.LT = (red+90, green+90, blue+90)
    const.DK = (red, green, blue)
    const.MD = (red+10, green+10, blue+10)


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


def show_winning_screen(screen, board, puzzle):
    clock = pygame.time.Clock()
    i = 2
    running = True
    count = 0
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

        screen.blit(board, (25, 100))
        # draw "Solved" caption
        font = pygame.font.Font(None, const.SIZE*50)

        text = font.render("Solved", 1, const.WHITE)
        textpos = text.get_rect(centerx=screen.get_width()/2, centery=screen.get_height()/2)
        screen.blit(text, textpos)

        # TODO implement something like a firework

        # refresh Screen
        pygame.display.flip()

if __name__ == '__main__':
    main()
