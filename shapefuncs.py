from project import Canvas, TerminalScribe
#from drawshapes import Shape_Scribe, Line, Polygon, Circle
from graph import Canvas_Graph, Terminal_Graph
from collections import defaultdict
from shapesdict import shape_scribes, classes


def main():
    #canvas = Canvas(20, 20)
    #s = Shape_Scribe(canvas)
    #s.draw_circle(9, [10, 10])
    #s.end_line()
    

    canvas = Canvas(30, 21)
    call_shape(canvas, 'TerminalScribe', 'Triskele')

    
    #def sin(x):
    #    return 5*math.sin(x/3 + 10)
        
    #def cos(x):
    #    return 5*math.cos(x/3 + 10)
    
    #def x_sq(x):
    #    return x**2

    #canvas = Canvas(30, 20)
    #functions = [cos, sin, x_sq]
    #plot_multi_function(canvas, functions, clear=False)


def call_shape(canvas, scribe_class, shape_name, pos_shift=[]):
    #pos_shift is coordinates relative to pre-set shape start position (so [-2, 3] == move the shape's start-point 2 left, and 3 down.)

    # Create scribes
    shape_data = shape_scribes[shape_name]
    for scribe in shape_data:
        attributes = scribe['Attributes']
        if bool(pos_shift):
            pos = [attributes['position'][0] + pos_shift[0], attributes['position'][1] + pos_shift[1]]
            attributes['position'] = pos
        scribe['Scribe Name'] = classes[scribe_class](canvas, **attributes)

        # Start position = shape position + shift
        #pos = [scribe['Position'][0] + pos_shift[0], scribe['Position'][1] + pos_shift[1]]
        #scribe['Scribe Name'].set_position(pos)
        
        scribe['Move Set']=defaultdict(list)
        scribe['Move Set']=[]
        for moves in scribe['Movements']:
            if moves['all args'] is not None:
                for arg_set in moves['all args']:
                    for _ in range(arg_set['reps']):
                        scribe['Move Set'].append({'func': moves['func'], 'args': arg_set['args']})
            else:
                scribe['Move Set'].append({'func': moves['func'], 'args': None})
   
    max_moves = max([len(scribe['Move Set']) for scribe in shape_data])
    
    for n in range(max_moves):
        for scribe in shape_data:
            s = scribe['Scribe Name']
            move_set = scribe['Move Set']
            
            if n < len(move_set):
                make_it_go(move_set[n]['func'], s, move_set[n]['args'])

def make_it_go(func, scribe, args):
    if args is not None:
        func(scribe, **args)
    else:
        func(scribe)


## BUG -- plots functions simultaneously, but each function is cleared as soon as it's finished
# (only last function to have a dot print stays visible)
# Possibly to do with the settings/functions in the Canvas_Graph? 
# Or just a "clear = False" I missed in Terminal_Graph...

def plot_multi_function(canvas, functions, **plot_args):
    #scribe_list = defaultdict(list)
    scribe_list = [{'Func': function} for function in functions]
    
    #for function in functions:
    #    scribe_list.append({'Func': function})
    print(scribe_list)
    
    for scribe in scribe_list:

        scribe['Scribe Name'] = Terminal_Graph(canvas)
        print(scribe_list)
        scribe['Points'] = scribe['Scribe Name'].plot_func_set(scribe['Func'], **plot_args)
        #Add scribe position start -> self.pos = points_list[0]
    
    max_points = max([len(scribe['Points']) for scribe in scribe_list])

    #Add scribe start_new_line -> self.start_new_line()
    for n in range(max_points):
        for scribe in scribe_list:

            s = scribe['Scribe Name']
            points = scribe['Points']
            
            if n < len(points):
                s.draw(points[n])
    
    #End_line -> self.end_line()

if __name__ == "__main__":
    main()