import os
import time
from termcolor import colored
import math
import copy

# This is the Canvas class. It defines some height and width, and a
# matrix of characters to keep track of where the TerminalScribes are moving

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]
    

    # Returns info if given point is outside the boundaries of the Canvas
    def hits_wall(self, point):
        if point[0] < 0 or point[0] >= self._x:
            return 'vertical'
        elif point[1] < 0 or point[1] >= self._y:
            return 'horizontal'   

    # Set the given position to the provided character on the canvas
    def set_pos(self, pos, char):
        self._canvas[round(pos[0])][round(pos[1])] = char

    # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print_canvas(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))



class TerminalScribe:
    
    def __init__(self, canvas, position=[0,0], angle=90, framerate=0.05, color_shift=False, default_mark_color='red', default_trail_color='white'):
        self.canvas = canvas
        self.direction = (1, 0)
        self._bounce = False
        self.color_shift_list = ['red', 'light_red', 'light_yellow', 'yellow', 'green', 'light_green', 
                        'light_cyan', 'cyan', 'blue', 'light_blue', 'light_magenta', 'magenta']
        
        self.color_shift = color_shift
        self.trail = '.'
        self.default_trail_color = default_trail_color
        self.trail_color = self.default_trail_color
        self.default_mark_color = default_mark_color
        self.mark_color = self.default_mark_color
        self.mark = '*'
        self.framerate = framerate
        self.pos = position
        self.dir_angle = angle
        
        if color_shift == True:
            if self.trail_color == 'white':
                self.trail_color = self.mark_color

        self.initial_settings = None
        
        self.save_init()

    def save_init(self):
        self.initial_settings = copy.deepcopy(vars(self))
    
    def reset(self):
        for key in self.initial_settings:
            setattr(self, key, self.initial_settings[key])
    
    def set_all(self, attributes):
        for key in attributes:
            setattr(self, key, self.initial_settings[key])

    def forward(self, angle, bounce=True):
        if angle != self.dir_angle:
            self.dir_angle = angle
            self.angle_to_dir()
            self.angle_adjust()

        pos = self.get_dpos(*self.direction)
        
        hits_wall = self.canvas.hits_wall(pos)
        if hits_wall is not None:
            if bounce == True:
                self._bounce_angle(hits_wall)
                self.forward(self.dir_angle)
        else:
            self.draw(pos)

    def set_position(self, pos):
        self.pos = pos

    def draw(self, pos):
        self.move_marks(pos)
        self.print_marks()
        
    # Move marker AND create trail in old position (but don't print)
    def move_marks(self, pos):
        self.set_trail(self.pos)
        self.set_mark(pos)

    def print_marks(self):
        # Print everything to the screen, then sleep to create animation
        self.canvas.print_canvas()
        time.sleep(self.framerate)
    
    # Set the position of the mark
    def set_mark(self, pos):
        if self.color_shift == True:
            self.mark_color = self.get_next_color(self.trail_color)
            
        # Update position, then set it to the "mark" symbol
        self.pos = pos
        self.canvas.set_pos(self.pos, colored(self.mark, self.mark_color))

    def set_trail(self, pos):
        # Consider adding temp "override" of color, using color = None + if color == None: color = self.trail_color ??
        self.canvas.set_pos(pos, colored(self.trail, self.trail_color))

        if self.color_shift == True:
            self.trail_color = self.get_next_color(self.trail_color)

    def set_color(self, mark_color=None, trail_color=None, color_shift=None):
        if mark_color is not None:
            self.mark_color = mark_color
        if trail_color is not None:
            self.trail_color = trail_color
        
        if color_shift == True or color_shift == False:
            self.color_shift = color_shift
            
            if color_shift is True:
                if trail_color is None:
                    self.trail_color = self.mark_color
            # Reset marker colors to defaults if color_shift turned off (unless color specified in args)
            if color_shift == False:
                if mark_color is None:
                    self.mark_color = self.default_mark_color
                if trail_color is None:
                    self.trail_color = self.default_trail_color

        ## exceptions -- input is not string, or input is string, but not one of the possible colors
    
    def get_next_color(self, current_color):
        ## exceptions -- input is not string and/or not one of the possible colors
        current_color_index = self.color_shift_list.index(current_color)
        try:
            color = self.color_shift_list[current_color_index + 1]
        except Exception:
            color = self.color_shift_list[0]
        
        return color


    # Print a marker at the current self.pos
    def start_new_line(self, pos=None):
        if pos is None:
            pos = self.pos
        self.set_mark(pos)
        self.print_marks()
    
    # set the current position to the "trail" symbol
    def end_line(self):
        self.set_trail(self.pos)
        self.print_marks()


    ## in-terminal scribe...?
    # Jump mark position to new position relative to current, indicated by direction and number of spaces to move for each
    def jump(self, up=0, down=0, left=0, right=0, new=False):
        if new == False:
            self.end_line()
        x = (self.pos[0] + right) - left
        y = (self.pos[1] - up) + down

        # Update position
        self.pos = [x, y]
    

    def angle_to_dir(self):
        v_x = math.sin(math.radians(self.dir_angle))
        v_y = math.cos(math.radians(self.dir_angle))
        self.direction = (v_x, v_y)
    
    # ...NEEDS clean-up -- can make the if/elif neater, combining somehow?
    def angle_adjust(self):

        pi = math.pi
        radians = self.dir_angle * pi/180
        
        if radians > 2*pi:
            radians = radians-2*pi

        if radians <= (pi/8) or radians >= (15*pi/8):
            rad = 0
        elif radians < (3*pi/8):
            rad = pi/4
        elif radians <= (5*pi/8):
            rad = pi/2
        elif radians < (7*pi/8):
            rad = pi/4
        elif radians <= 9*pi/8:
            rad = 0
        elif radians < 11*pi/8:
            rad = pi/4
        elif radians <= 13*pi/8:
            rad = pi/2
        elif radians < 15*pi/8:
            rad = pi/4

        v_x = math.copysign(math.sin(rad), self.direction[0])
        v_y = math.copysign(math.cos(rad), self.direction[1])
        self.direction = (v_x, v_y)
    
    def get_dpos(self, dir_vector_x, dir_vector_y):
        v_x = dir_vector_x
        v_y = dir_vector_y
    
        if math.isclose(abs(v_x), abs(v_y)):
            v_x = math.copysign(v_y, v_x)
        
        d_x = 0
        d_y = 0

        if math.fabs(v_x) >= math.fabs(v_y):
            if v_x > 0:
                d_x = 1
            else:
                d_x = -1

        if math.fabs(v_y) >= math.fabs(v_x):
            if v_y > 0:
                d_y = -1
            else:
                d_y = 1
        
        pos = [self.pos[0] + d_x, self.pos[1] + d_y]
        return pos

    def bounce_angle(self, wall):
        self._bounce = True
        
        if wall == 'vertical':
            self.dir_angle= round(math.degrees(math.asin(-self.direction[0])))
            self.direction = [-self.direction[0], self.direction[1]]

        if wall == 'horizontal':
            self.dir_angle = round(math.degrees(math.acos(-self.direction[1])))
            self.direction = [self.direction[0], -self.direction[1]]

       

    # Animation (move marks by one):
    # (In-terminal scribe?)

class One_Trick_Scribe(TerminalScribe):
    def up(self):
        pos = [self.pos[0], self.pos[1]-1]
        if not self.canvas.hits_wall(pos):
            self.draw(pos)

    def down(self):
        pos = [self.pos[0], self.pos[1]+1]
        if not self.canvas.hits_wall(pos):
            self.draw(pos)

    def right(self):
        pos = [self.pos[0]+1, self.pos[1]]
        if not self.canvas.hits_wall(pos):
            self.draw(pos)

    def left(self):
        pos = [self.pos[0]-1, self.pos[1]]
        if not self.canvas.hits_wall(pos):
            self.draw(pos)

