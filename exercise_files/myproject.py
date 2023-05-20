import os
import time
from termcolor import colored

# This is the Canvas class. It defines some height and width, and a
# matrix of characters to keep track of where the TerminalScribes are moving


class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        self._canvas[pos[0]][pos[1]] = mark

    # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))


class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.2
        self.pos = [0, 0]

    def draw(self, pos):
        self.move_marks(pos)
        self.print_marks()

    # Move marker AND create trail in old position (but don't print)
    def move_marks(self, pos):
        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, self.trail)
        self.set_mark(pos)

    # Set the position of the mark
    def set_mark(self, pos):
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))

    def print_marks(self):
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    # set the current position to the "trail" symbol
    def end_line(self):
        self.canvas.setPos(self.pos, self.trail)
        self.print_marks()

    # Print a marker at the current self.pos
    def start_new_line(self):
        self.set_mark(self.pos)
        self.print_marks()

    # Jump mark position to new position relative to current, indicated by direction and number of spaces to move for each
    def jump(self, up=0, down=0, left=0, right=0, new=False):
        if new == False:
            self.end_line()
        x = (self.pos[0] + right) - left
        y = (self.pos[1] - up) + down

        # Update position
        self.pos = [x, y]

    # Animation:

    def up(self):
        pos = [self.pos[0], self.pos[1]-1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def down(self):
        pos = [self.pos[0], self.pos[1]+1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def right(self):
        pos = [self.pos[0]+1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def left(self):
        pos = [self.pos[0]-1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def diag_up(self, dir_horizontal='right'):
        if dir_horizontal == 'right':
            x = self.pos[0] + 1
        else:
            x = self.pos[0] - 1

        pos = [x, self.pos[1] - 1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def diag_down(self, dir_horizontal='right'):
        y = self.pos[1] + 1
        if dir_horizontal == 'right':
            x = self.pos[0] + 1
        else:
            x = self.pos[0] - 1

        pos = [x, y]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    # Draw Lines and Shapes:

    def draw_line(self, length=2, direction='right', new=False, end=False):
        for _ in range(length):
            if direction == 'up':
                self.up()
            elif direction == 'down':
                self.down()
            elif direction == 'right':
                self.right()
            elif direction == 'left':
                self.left()

    def draw_diag_up(self, length=2, direction='right'):
        for _ in range(int(length)):
            self.diag_up(direction)

    def draw_diag_down(self, length=2, direction='right'):
        for _ in range(int(length)):
            self.diag_down(direction)

    # works
    def draw_rectangle(self, width, height):
        w = width
        h = height
        self.draw_line(w, 'right')
        self.draw_line(h, 'down')
        self.draw_line(w, 'left')
        self.draw_line(h, 'up')

        # to maybe add... ability to choose which corner to start drawing from? Plus draw direction (clockwise, counter-clockwise)...

# to-do, add "shape size" option, which will scale the shape depending on the number entered

# Draw a 5x5 box, with checkmark -- change object size with "scale"


def make_checked_box(scribe, pos, scale=1):
    # create square
    start_pos = pos
    scribe.start_new_line()
    scribe.draw_rectangle(3*scale, 3*scale)

    # create checkmark
    start_pos
    scribe.jump(down=1*scale, right=1)
    scribe.start_new_line()
    scribe.draw_diag_down(1*scale)
    scribe.draw_diag_up(3*scale)
    scribe.end_line()


# Create a new Canvas instance that is 30 units wide by 30 units tall
canvas = Canvas(30, 30)

# Create a new scribe and give it the Canvas object
s = TerminalScribe(canvas)

start_pos = s.jump(down=3, right=1, new=True)
make_checked_box(s, start_pos, 2)
