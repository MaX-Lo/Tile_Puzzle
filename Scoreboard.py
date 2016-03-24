import os.path
import pygame
import re
from pygame.locals import *

# module to create a highscorelist for a pygame game
# created by MaX-Lo

class Scoreboard:
    def __init__(self, filename="highscore.dat"):
        self.screen = pygame.display.set_mode((500, 550))

        path = os.path.dirname(os.path.realpath(__file__)) + "/data/" + filename
        self.filename = path
        # creating higscorefile if given file doesn't exist
        if not test_file(self.filename):
            create_file(self.filename)
        self.entry_list = self.load_highscore_list()

        # Entries getting shown
        self.points = False
        self.steps = True
        self.level = False
        self.time = True

        # Sort property
        self.sort_by = "TIME_ASC"

        # Window properties
        self.border = 15
        self.border_color = (230, 230, 230)
        self.bg_color = (0, 100, 0)
        self.table_color = (132, 151, 0)

        # Font
        self.font_size = 25
        self.line_space = 10
        self.font_color = (30, 30, 30)

    def save_entry(self, entry):
        """ creates new Entry and saves it in a file """

        if entry.name == "":
            entry.name = "Mr. XXX"

        self.entry_list.append(entry)

        self.sort_list()

        if len(self.entry_list) > 10:
            self.entry_list.pop(-1)
        self.save_in_file()

    def sort_list(self):
        # sort the highscorelist
        # TODO complete options
        if self.sort_by == "POINTS_DESC":
            self.sort_by_points("DESC")
        elif self.sort_by == "POINTS_ASC":
            self.sort_by_points("ASC")
        elif self.sort_by == "STEPS_DESC":
            self.sort_by_steps("DESC")
        elif self.sort_by == "STEPS_ASC":
            self.sort_by_steps("ASC")
        elif self.sort_by == "TIME_DESC":
            self.sort_by_time("DESC")
        elif self.sort_by == "TIME_ASC":
            self.sort_by_time("ASC")
        elif self.sort_by == "LEVEL_DESC":
            self.sort_by_level("DESC")
        elif self.sort_by == "LEVEL_ASC":
            self.sort_by_level("ASC")

    def save_in_file(self):
        raw_content = []
        for entry in self.entry_list:
            line = entry.name + "-" + str(entry.points) + "-" + str(entry.steps) + "-" + str(entry.level) + "-" + str(entry.time)
            raw_content.append(str(line))
        save_file(self.filename, raw_content)

    def add(self, name="", points=0, steps=0, level=0, time=0.0):

        entry = Entry(name, points, steps, level, time)

        new_entry_pos = self.get_position(entry)
        if new_entry_pos <= 10 <= len(self.entry_list):
            self.entry_list.pop(-1)

        clock = pygame.time.Clock()

        scoreboard_running = True
        while scoreboard_running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == KEYUP:
                    if event.key == K_RETURN or event.key == K_ESCAPE:
                        self.save_entry(entry)
                        scoreboard_running = False
                    elif event.key == K_DELETE or event.key == 8:
                        entry.name = entry.name[:-1]  # Deletes last char
                    elif event.key == K_MINUS:  # "-" gets replaced by "_"
                        entry.name += "_"
                    elif event.key <= 127:
                        if len(entry.name) < 9:  # name may not be longer than 8 character
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                entry.name += chr(event.key).upper()
                            else:
                                entry.name += chr(event.key)

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
            xn = x
            self.screen.blit(fontobject.render("Name", 1, self.font_color), (xn, y_entry))
            xn += 130
            if self.points:
                self.screen.blit(fontobject.render("Points", 1, self.font_color), (xn, y_entry))
                xn += 75
            if self.steps:
                self.screen.blit(fontobject.render("Steps", 1, self.font_color), (xn, y_entry))
                xn += 75
            if self.level:
                self.screen.blit(fontobject.render("Level", 1, self.font_color), (xn, y_entry))
                xn += 75
            if self.time:
                self.screen.blit(fontobject.render("Time", 1, self.font_color), (xn, y_entry))
                xn += 75

            y_entry += self.font_size + self.line_space

            if len(self.entry_list) == 0:
                # printing new entry at correct position
                xn = x
                self.screen.blit(fontobject.render(entry.name + (9-len(entry.name))*"_", 1, self.font_color), (xn, y_entry))
                xn += 130

                if self.points:
                    self.screen.blit(fontobject.render("{0:8d}".format(entry.points), 1, self.font_color), (xn, y_entry))
                    xn += 75

                if self.steps:
                    self.screen.blit(fontobject.render("{0:8d}".format(entry.steps), 1, self.font_color), (xn, y_entry))
                    xn += 75

                if self.level:
                    self.screen.blit(fontobject.render("{0:3d}".format(entry.level),
                                                           1, self.font_color), (xn, y_entry))
                    xn += 75

                if self.time:
                    self.screen.blit(fontobject.render("{0:5.2f} sec".format(entry.time),
                                                       1, self.font_color), (xn, y_entry))

            num = 1 # increased everytime by 1 to know when it's time to draw the new entry
            # print all existing entries
            for element in self.entry_list:
                # printing new entry at correct position
                if num == new_entry_pos:
                    xn = x
                    self.screen.blit(fontobject.render(entry.name + (9-len(entry.name))*"_", 1, self.font_color), (xn, y_entry))
                    xn += 130

                    if self.points:
                        self.screen.blit(fontobject.render("{0:8d}".format(entry.points), 1, self.font_color), (xn, y_entry))
                        xn += 75

                    if self.steps:
                        self.screen.blit(fontobject.render("{0:8d}".format(entry.steps), 1, self.font_color), (xn, y_entry))
                        xn += 75

                    if self.level:
                        self.screen.blit(fontobject.render("{0:3d}".format(entry.level),
                                                           1, self.font_color), (xn, y_entry))
                        xn += 75

                    if self.time:
                        self.screen.blit(fontobject.render("{0:5.2f} sec".format(entry.time),
                                                           1, self.font_color), (xn, y_entry))
                        xn += 75
                    y_entry += self.font_size + self.line_space
                num += 1

                # printing already existing entries
                xn = x
                self.screen.blit(fontobject.render(element.name, 1, self.font_color), (xn, y_entry))
                xn += 130

                if self.points:
                    self.screen.blit(fontobject.render("{0:8d}".format(element.points), 1, self.font_color), (xn, y_entry))
                    xn += 75

                if self.steps:
                    self.screen.blit(fontobject.render("{0:8d}".format(element.steps), 1, self.font_color), (xn, y_entry))
                    xn += 75

                if self.level:
                    self.screen.blit(fontobject.render("{0:3d}".format(element.level),
                                                           1, self.font_color), (xn, y_entry))
                    xn += 75

                if self.time:
                    self.screen.blit(fontobject.render("{0:5.2f} sec".format(element.time),
                                                           1, self.font_color), (xn, y_entry))
                    xn += 75

                y_entry += self.font_size + self.line_space
            pygame.display.flip()

    def get_position(self, entry):
        """
        calculates the position of the new entry in the highscorelist
        """
        self.sort_list()

        pos = 1
        if self.sort_by == "TIME_ASC":
            for element in self.entry_list:
                if entry.time >= element.time:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "TIME_DESC":
            for element in self.entry_list:
                if entry.time <= element.time:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "POINTS_ASC":
            for element in self.entry_list:
                if entry.points >= element.points:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "POINTS_DESC":
            for element in self.entry_list:
                if entry.points <= element.points:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "STEPS_ASC":
            for element in self.entry_list:
                if entry.steps >= element.steps:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "STEPS_DESC":
            for element in self.entry_list:
                if entry.steps <= element.steps:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "LEVEL_ASC":
            for element in self.entry_list:
                if entry.level >= element.level:
                    pos += 1
                else:
                    return pos
        elif self.sort_by == "LEVEL_DESC":
            for element in self.entry_list:
                if entry.level <= element.level:
                    pos += 1
                else:
                    return pos
        return pos


    def sort_by_points(self, direction):
        """ sort the list by points descending """
        for num in range(len(self.entry_list)-1, 0, -1):   # goes from last to first element
            for i in range(num):
                if direction == "ASC":
                    if self.entry_list[i].points > self.entry_list[i+1].points:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]   # exchanges the elements
                elif direction == "DESC":
                    if self.entry_list[i].points < self.entry_list[i+1].points:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]   # exchanges the elements

    def sort_by_steps(self, direction):
        """ sort the list by steps ascending """
        for num in range(len(self.entry_list)-1, 0, -1):   # goes from last to first element
            for i in range(num):
                if direction == "ASC":
                    if self.entry_list[i].steps > self.entry_list[i+1].steps:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]   # exchanges the elements
                elif direction == "DESC":
                    if self.entry_list[i].steps < self.entry_list[i+1].steps:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]   # exchanges the elements

    def sort_by_time(self, direction):
        for num in range(len(self.entry_list)-1, 0, -1):   # goes from last to first element
            for i in range(num):
                if direction == "ASC":
                    if self.entry_list[i].time > self.entry_list[i+1].time:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]
                elif direction == "DESC":
                    if self.entry_list[i].time < self.entry_list[i+1].time:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]

    def sort_by_level(self, direction):
        for num in range(len(self.entry_list)-1, 0, -1):   # goes from last to first element
            for i in range(num):
                if direction == "ASC":
                    if self.entry_list[i].level > self.entry_list[i+1].level:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]
                elif direction == "DESC":
                    if self.entry_list[i].level < self.entry_list[i+1].level:
                        self.entry_list[i], self.entry_list[i + 1] = self.entry_list[i + 1], self.entry_list[i]

    def load_highscore_list(self):
        """ formats the higscore file content
        into a List with single entries """
        raw_list = load_file(self.filename)
        formated_list = []
        for line in raw_list:
            entry = Entry()
            pos = [c.start() for c in re.finditer('-', line)] # getting the divider positions
            entry.name = line[:pos[0]]
            entry.points = int(line[pos[0]+1:pos[1]])
            entry.steps = int(line[pos[1]+1:pos[2]])
            entry.level = int(line[pos[2]+1:pos[3]])
            entry.time = float(line[pos[3]+1:])
            formated_list.append(entry)
        return formated_list
    
    def set_border_color(self, c):
        self.border_color = c
    
    def set_bg_color(self, c):
        self.bg_color = c
    
    def set_table_color(self, c):
        self.table_color = c


class Entry:
    def __init__(self, name="The Fox", points=0, steps=0, level=0, time=0.0):
        self.name = name
        self.points = points
        self.steps = steps
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
