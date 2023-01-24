from __init__ import *

class GameRender:
    @staticmethod
    @mainthread
    def render_winner(instance, winner, playerManager):
        if(winner==0):
            GameRender.draw_hide(instance, "yellow")
            GameRender.draw_equal(instance)
        elif(winner==playerManager.player_1.token_value):
            GameRender.draw_hide(instance, "red")
            GameRender.draw_cross(instance)
        elif(winner==playerManager.player_2.token_value):
            GameRender.draw_hide(instance, "blue")
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

    @staticmethod
    def draw_equal(instance, width=100, line_width=4):
        with instance.canvas:
            Color(1,0.9,0,1, mode="rgba")
            Line(points=(instance.center_x-width/3, instance.center_y-width/4, instance.center_x+width/3, instance.center_y-width/4), width=line_width)
            Line(points=(instance.center_x-width/3, instance.center_y+width/4, instance.center_x+width/3, instance.center_y+width/4), width=line_width)
    
    @staticmethod
    def draw_hide(instance, color):
        with instance.canvas:
            if(color=="red"):
                Color(1,0,0,0.2, mode="rgba")
            elif(color=="blue"):
                Color(0,0,1,0.2, mode="rgba")
            elif(color=="yellow"):
                Color(1,1,0,0.2, mode="rgba")
            Rectangle(pos=instance.pos , size=instance.size)

    '''
    @staticmethod
    def draw_lines(instance, i, j, width):
        M = instance.children
        with instance.canvas:
            Color(0,0,0,1, mode="rgba")
            Line(points=(M[i].center_x, M[i].center_y, M[j].center_x, M[j].center_y), width=width)
    '''