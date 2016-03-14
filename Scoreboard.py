import os.path
import pygame
import re
from pygame.locals import *

# module to create fast and easy a highscorelist for a pygame game
# created by MaX-Lo


class Scoreboard:
    def __init__(self, screen, filename="highscore.dat"):
        path = os.path.dirname(os.path.realpath(__file__)) + "/data/" + filename
        self.filename = path
        if not test_file(self.filename):
            create_file(self.filename)
        self.score_list = self.load_highscore_list()

        # Entries getting shown
        self.points = True
        self.level = True
        self.time = True

        self.screen = screen

        # Window properties
        self.border = 15
        self.border_color = (230, 230, 230)
        self.bg_color = (0, 100, 0)
        self.table_color = (132, 151, 0)

        # Font
        self.font_size = 25
        self.line_space = 10
        self.font_color = (30, 30, 30)

    def save_entry(self, name, points, level, time):
        entry = Entry(name, points, level, time)
        self.score_list.append(entry)
        self.sort_score_list_by_points()
        if len(self.score_list) > 10:
            self.score_list.pop(-1)
        self.save_in_file()

    def save_in_file(self):
        raw_content = []
        for entry in self.score_list:
            line = entry.name + "-" + str(entry.points) + "-" + str(entry.level) + "-" + str(entry.time)
            raw_content.append(str(line))
        save_file(self.filename, raw_content)

    def add(self, name="", points=0, level=0, time=0.0):
        scoreboard_running = True
        while scoreboard_running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYUP:
                    if event.key == KMOD_SHIFT:
                        if event.key <= 127:
                            name += chr(event.key).upper()
                    elif event.key == K_RETURN or event.key == K_ESCAPE:
                        self.save_entry(name, points, level, time)
                        scoreboard_running = False
                    elif event.key == K_DELETE or event.key == 8:
                        name = name[:-1]  # Deletes last char
                    elif event.key == K_MINUS:  # "-" gets replaced by "_"
                        name += "_"
                    elif event.key <= 127:
                        name += chr(event.key)

            # Table
            pygame.draw.rect(self.screen, self.bg_color, (0, 0, self.screen.get_width(), self.screen.get_height()))
            x = self.screen.get_width()/2-200
            y = 20
            width = 400
            height = (self.font_size+self.line_space)*11
            pygame.draw.rect(self.screen, self.border_color, (x-5, y-5, width+10, height+10))
            pygame.draw.rect(self.screen, self.table_color, (x, y, width, height))
            fontobject = pygame.font.Font(None, self.font_size)
            y += 5
            x += 5
            y_entry = y
            # print table head
            self.screen.blit(fontobject.render("Name", 1, self.font_color), (x, y_entry))
            xn = x
            if self.points:
                xn += 125
                self.screen.blit(fontobject.render("Points", 1, self.font_color), (xn, y_entry))
            if self.level:
                xn += 75
                self.screen.blit(fontobject.render("Level", 1, self.font_color), (xn, y_entry))
            if self.time:
                xn += 75
                self.screen.blit(fontobject.render("Time", 1, self.font_color), (xn, y_entry))
            y_entry += self.font_size + self.line_space
            # print all existing entries
            for entry in self.score_list:
                self.screen.blit(fontobject.render(entry.name, 1, self.font_color), (x, y_entry))
                xn = x
                if self.points:
                    xn += 125
                    self.screen.blit(fontobject.render("{0:8d}".format(entry.points),
                                                       1, self.font_color), (xn, y_entry))
                if self.level:
                    xn += 75
                    self.screen.blit(fontobject.render("{0:3d}".format(entry.level),
                                                       1, self.font_color), (xn, y_entry))
                if self.time:
                    xn += 75
                    self.screen.blit(fontobject.render("{0:5.2f}".format(entry.time),
                                                       1, self.font_color), (xn, y_entry))
                y_entry += self.font_size + self.line_space
            y = (self.font_size + self.line_space) * 11

            # Input Line
            pygame.draw.rect(self.screen, self.border_color, (x-10, y+50, width+10, 40+10))
            pygame.draw.rect(self.screen, self.table_color, (x-5, y+55, width, 40))
            self.screen.blit(fontobject.render("Name: " + name + " Points: " + str(points), 1, self.font_color), (x, y+60))

            pygame.display.flip()

    def sort_score_list_by_points(self):
        for num in range(len(self.score_list)-1, 0, -1):   # goes from last to first element
            for i in range(num):
                if self.score_list[i].points < self.score_list[i+1].points:
                    self.score_list[i], self.score_list[i + 1] = self.score_list[i + 1], self.score_list[i]   # exchanges the elements

    def load_highscore_list(self):
        """ formats the higscore file content
        into a List with single entries """
        raw_list = load_file(self.filename)
        formated_list = []
        for line in raw_list:
            entry = Entry()
            pos = [c.start() for c in re.finditer('-', line)]
            entry.name = line[:pos[0]]
            entry.points = int(line[pos[0]+1:pos[1]])
            entry.level = int(line[pos[1]+1:pos[2]])
            entry.time = float(line[pos[2]+1:])
            formated_list.append(entry)
        return formated_list


class Entry:
    def __init__(self, name="The Fox", points=0, level=0, time=0.0):
        self.name = name
        self.points = points
        self.level = level
        self.time = time


def save_file(name, content):
    fobj = open(name, "w")
    for i in range(len(content)):
        fobj.write(content[i]+"\n")
    fobj.close()


def load_file(name):
    content = []
    print name
    fobj = open(name, "r")
    for line in fobj:
        content.append(line.rstrip())  # rstrip entfernt Leerzeichen und Newlines am rechten Rand
    fobj.close()
    return content


def test_file(name):
    """ checks whether file exists """
    name = os.path.abspath(name)
    return os.path.isfile(name)


def create_file(filename):
    fobj = open(filename, 'w+')
    fobj.close()
