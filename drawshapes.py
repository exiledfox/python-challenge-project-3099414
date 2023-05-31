from project import TerminalScribe
import math

class Shape_Scribe(TerminalScribe):
    pass

class Line(Shape_Scribe):
    def __init__(self, canvas, default_length=4, **kwargs):
        super().__init__(canvas, **kwargs)
        self.default_length = default_length

    def draw_line(self, length=None, angle=90, new=False, end=False):
        if length == None:
            length = self.default_length
        if new == True:
            self.start_new_line()
           
        for _ in range(length):
            if self._bounce == True:
                angle = self.dir_angle
                self._bounce = False
            self.forward(angle)
        
        if end == True:
            self.end_line()
        
        # Reset variables
        self.dir_angle = None
        self._bounce = False

    def draw_diag_up(self, length=2, direction='right'):
        if direction == 'right' or direction == 'r':
            angle = 45
        elif direction == 'left' or direction == 'l':
            angle = 315
        # errors to catch here: direction is none of above
        
        self.draw_line(length, angle)

    def draw_diag_down(self, length=2, direction='right'):
        if direction == 'right' or direction == 'r':
            angle = 135
        elif direction == 'left' or direction == 'l':
            angle = 225
        # errors to catch here: direction is none of above
        
        self.draw_line(length, angle)

class Polygon(Shape_Scribe):
    def __init__(self, canvas, default_sides=4, default_length=4, **kwargs):
        super().__init__(canvas, **kwargs)
        self.default_length = default_sides
        self.default_length = default_length

    def draw_rectangle(self, width, height):
        self.start_new_line()
        w = int(round(width)) - 1
        h = int(round(height)) - 1
        self.draw_line(w, 90)
        self.draw_line(h, 180)
        self.draw_line(w, 270)
        self.draw_line(h, 0)

        # To maybe add... ability to choose which corner to start drawing from? 
        # Plus draw direction (clockwise, counter-clockwise)...
    
    def draw_triangle(self, sides):
        b = 2*sides
        self.start_new_line()
        self.draw_line(sides, 135)
        self.draw_line(b, 270)
        self.draw_line(sides, 45)

    # Draw_poly_even currently can draw shapes with even number of sides, up to 8 sides

    def draw_poly_even(self, sides=4, length=3, angle_offset=90, clockwise=True):
        #errors to catch... - arguments non-integers, or sides < 3
        if clockwise:
            d = 1
        else: 
            d = -1
        
        l = length - 1
        angle_int = d*(int((sides-2)*180/sides))
        angle = 180 + angle_offset - angle_int
        
        if sides % 2 == 0 and sides > 3:
            for _ in range(sides):
                self.draw_line(l, angle)
                angle_offset = angle
                angle = 180 + angle_offset - angle_int
        else:
            print('Sides must be an even number, between 4-8.')

class Circle(Shape_Scribe):
    
    def __init__(self, canvas, default_radius=4, **kwargs):
        super().__init__(canvas, **kwargs)
        self.default_length = default_radius

    def draw_circle(self, r, center=None):
        if r == None:
            r == self.default_size
        ## Set starting position, direction, and iteration values:
        if center == None:
                    # or alt, have center at [self.pos[0] + r, self.pos[1]]?
            center = self.pos
        pos_0 = (center[0] - round(r), center[1])
        self.dir_angle = 0
        self.angle_to_dir()
        self.angle_adjust()

        total_angle_change = 0
        pos = 0
        moves = 0
        d_angle = 45

        self.start_new_line(pos_0)

        ## Iterate until completed full turn, and final move meets the starting position:
        while total_angle_change < 360 and pos != pos_0:
            if moves < (6 * r):
                
                # Test 2 possible next-points -- same as current direction, and current dir + 45
                # Move forward towards point that is closest to r
                angle_2 = self.dir_angle + d_angle
                positions = self.get_test_positions(angle_2)
                if self.test_pos_against_r(r, center, *positions):
                    total_angle_change = total_angle_change + d_angle
                    self.forward(angle_2, bounce=False)
                else:
                    self.forward(self.dir_angle, bounce=False)
                
                pos = self.pos
                moves = moves + 1
            else:
                break
            
        self.end_line()

    def get_test_positions(self, angle_2, angle_1=None):

        if angle_1 is None or angle_1==self.dir_angle:
            p_1 = self.get_dpos(*self.direction)
        else:
            v1_x = math.sin(math.radians(angle_1))
            v1_y = math.cos(math.radians(angle_1))
            p_1 = self.get_dpos(v1_x, v1_y)
        
        v2_x = math.sin(math.radians(angle_2))
        v2_y = math.cos(math.radians(angle_2))
        p_2 = self.get_dpos(v2_x, v2_y)
        
        return [p_1, p_2]
    

    def test_pos_against_r(self, r, center, position_1, position_2):

        d1_sq = (position_1[0]-center[0])**2 + (position_1[1]-center[1])**2
        d2_sq = (position_2[0]-center[0])**2 + (position_2[1]-center[1])**2
        
        if math.fabs(d1_sq - r**2) > math.fabs(d2_sq - r**2):
            return True
