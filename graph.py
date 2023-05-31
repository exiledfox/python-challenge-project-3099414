from project import Canvas, TerminalScribe

class Canvas_Graph(Canvas):
    def __init__(self, *args):
        if type(args[0]) is Canvas:
            self.__dict__ = args[0].__dict__.copy()
        else:
            super(Canvas_Graph, self).__init__(*args[:2])

        self._x = self._x + 1
        self._y = self._y + 1

        self._center = self.get_center()
        self._vertex = self._center
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]
        
        self.show_axis = self.set_axis(True)
    
     # Calculate ~middle point of graph. 
     # For even canvas widths, errs on the side of 1 more unit to right and above "center" (than number of units to left or below)
    def get_center(self):
        self._center = [int(round((self._x-2)/2)), int(round((self._y - 1)/2))]
        return self._center
    

    # Set self._center to new point, or re-set to ~center of canvas if no point given
    def set_vertice(self, point):
        pos = point
        print(pos)
        print(bool(point))
        if bool(point) is False:
            pos = self._center
        
        if self.show_axis:
            self.clear_axis()
            self._vertex = pos
            self.set_graph()
        else:
            self._vertex = pos
        return self._vertex    


    def set_axis(self, bool):
        self.show_axis = bool
        #print(self.show_axis)
        self.set_graph()
        return bool
    

    def clear_axis(self):
        self._canvas = [[y.replace('-', ' ').replace('|', ' ') for y in x] for x in self._canvas]
    

    def set_graph(self):
        pos = self._vertex
        print(f'Vertice at: {pos}')
        # Adds axis marks to the stored self._canvas
        if self.show_axis:
            for y in range(self._y):
                self._canvas[pos[0]][y] = '|'
            for x in range(self._x):
                self._canvas[x][pos[1]] = '-'
            
        # Replaces axis marks with ' '
        elif self.show_axis == False:
            self.clear_axis()
    

    def clear_graph(self):
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]


    ## To-Do (future, maybe): 
    #       -  ...Would be cool to add "scale", somehow -- so if scale by 5, could plot, for example, a unit
    #          circle function so the point on the +x-axis is 5 spaces from center, instead of 1
    #       -  Add option to put numbers along the graph axes, and choose the spacing (like every-other, or every 5, or every .5).
    #          If implement scale, make sure numbers match the actual values, and not the relative size of the graphed function 
    #          (i.e., for unit circle scaled to 5, axis shows 1 at 5 spaces mark)

class Terminal_Graph(TerminalScribe):
    def __init__(self, *args):
        super().__init__(args[0])
        
        self.canvas = Canvas_Graph(args[0])
        # ^if type(args) is ..., then...

    def plot_func(self, function, x_axis=None, y_axis=None, show_axis=True, max_points=None, x_initial=None, graph_canvas=True, clear=True):
        points_list = self.plot_func_set(function, x_axis, y_axis, show_axis, max_points, x_initial, graph_canvas, clear)
        self.plot_points(points_list)
    
    def plot_func_set(self, function, x_axis=None, y_axis=None, show_axis=True, max_points=None, x_initial=None, graph_canvas=True, clear=True):
        # ^x_axis and y_axis are how much of +x and +y want on graph --> affects where the axis vertex is on the canvas
        # Default vertex, with graph canvas for is self.canvas.get_center().

        vertice = self.set_param(x_axis, y_axis, show_axis, graph_canvas, clear)
        # Calculate points from function in given range -- from initial x, and max x (or max number of points)
        x_range = self.get_range(vertice, 'x', x_initial, max_points)
        points = self.get_func_points_in_range(function, *x_range)
        if bool(points) is False:
            return print('Points out of canvas range. Please increase canvas size.')
        else:
            points_list = self.get_filtered_points(points, vertice)
            return points_list

    
    
    def set_param(self, x_axis=None, y_axis=None, show_axis=True, graph_canvas=True, clear=True):
        ## (To Test:)
        if type(self.canvas) is not Canvas_Graph:
            if graph_canvas == True:
                # Set canvas as a Canvas_Graph, with same dims as current canvas
                self.canvas = Canvas_Graph(self.canvas)
        
        # Canvas and vertices set-up
        if type(self.canvas) is Canvas_Graph:
            self.graph_setup(x_axis, y_axis, show_axis, clear=clear)
            vertice = self.canvas._vertex
        else:
            vertice = self.get_vertice(x_axis=x_axis, y_axis=y_axis)
        
        return vertice


    def get_filtered_points(self, points, vertice):
        # Adjust points relative to axis vertex, before plotting
        for point in points:
            point[0] = point[0] + vertice[0]
            point[1] = -point[1] + vertice[1]
        #print(f'Points, after adjust: {points}')

        # Create new filtered list of points in range of canvas dimensions.
        points_list=[]
        for point in points: 
            if self.canvas.hitsWall(point) == None:
                points_list.append(point)
        #print(f'Filtered points list: {points_list}')
        return points_list
        

    def graph_setup(self, x_axis, y_axis, show_axis, clear=True):
        if clear == True:
            self.canvas.clear_graph()

        # Set the x-y vertices (points plotted relative to that). Change vertex from default if needed.
        vert_x = self.canvas._center[0]
        vert_y = self.canvas._center[1]
        vertice = self.get_vertice(vert_x, vert_y, x_axis, y_axis)
        self.canvas.set_vertice(vertice)
                
        # Toggle axis on/off
        if self.canvas.show_axis != show_axis:
            self.canvas.set_axis(show_axis)

    # Returns x-y vertice   
    def get_vertice(self, vert_x=None, vert_y=None, x_axis=None, y_axis=None):
        
        if vert_x is None:
            vert_x = self.pos[0]
        if vert_y is None:
            vert_y = self.pos[1]

        if x_axis is not None:
            if x_axis >= self.canvas._x:
                vert_x = 0
            else:
                vert_x = self.canvas._x - 1 - x_axis

        if y_axis is not None:
            if y_axis  >= self.canvas._y:
                vert_y = self.canvas._y
            else:
                vert_y = y_axis
        
        return [vert_x, vert_y]
    

    # Returns range of given component (x or y) relative to a vertice
    def get_range(self, vertice, component, initial, points_max):
        if component == 'x':
            x_max = self.canvas._x - vertice[0]
            x_0 = -vertice[0]
            x_max = self.canvas._x - vertice[0]
            
            if initial != None:
                x_0 = initial

            if points_max != None:
                x_max = x_0 + points_max

            return [x_0, x_max]
        
        elif component == 'y':
            print(f'y: True')
            y_0 = -1*(self.canvas._y - vertice[1])
            y_max = self.canvas._y
            
            if initial != None:
                y_0 = initial

            if points_max != None:
                y_max = y_0 + points_max
        
            return [y_0, y_max]


    def get_func_points_in_range(self, function, x_min, x_max):
        points=[]
        
        for x in range(x_min, x_max):
            pos = [x, round(function(x))]
            points.append(pos)

        return points


    def plot_points(self, points):
        if bool(points) is False:
            return print('Points out of canvas range. Please increase canvas size.')
        
        self.pos = points[0]
        self.start_new_line()

        for point in points[1:]:
            self.draw(point)
        self.end_line()

#canvas = Canvas(15,19)
#graph = Terminal_Graph(canvas)
#graph.plot_func(y_axis=18)