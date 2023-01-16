from __init__ import *

# Draw the lines when a cell is complete (todo : draw big O and big X)
class GameRender:
    @staticmethod
    @mainthread
    def render_winner(instance, winner):
        if(winner==0):
            # GameRender.draw_circle(instance)
            pass
        elif(winner==cross):
            # pass
            GameRender.draw_cross(instance)
        elif(winner==circle):
            # pass
            GameRender.draw_circle(instance)

    @staticmethod
    def draw_cross(instance, width=100, line_width=4):
        with instance.canvas:
            Color(1,0,0,1, mode="rgba")
            Line(points=(instance.center_x-width/2, instance.center_y-width/2, instance.center_x+width/2, instance.center_y+width/2), width=line_width)
            Line(points=(instance.center_x-width/2, instance.center_y+width/2, instance.center_x+width/2, instance.center_y-width/2), width=line_width)

    @staticmethod
    def draw_circle(instance, width=100, line_width=4):
        with instance.canvas:
            Color(0,0,1,1, mode="rgba")
            Line(ellipse=(instance.center_x-width/2, instance.center_y-width/2, width, width), width=line_width)
    
    '''
    @staticmethod
    def draw_lines(instance, i, j, width):
        M = instance.children
        with instance.canvas:
            Color(0,0,0,1, mode="rgba")
            Line(points=(M[i].center_x, M[i].center_y, M[j].center_x, M[j].center_y), width=width)
    '''