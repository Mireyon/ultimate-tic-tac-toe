import random
import time
import os
import math
import numpy as np
import pandas as pd

from kivy.config import Config
width = 800
height = 700
# Window configuration
Config.set('kivy','window_icon','../assets/icon.png')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', height)
Config.set('graphics', 'width', width)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image

from kivy.clock import Clock, mainthread
from kivy.graphics import Line, Color, Rectangle, Ellipse

from player import PlayerManager
from threading import Thread
from functools import partial

# Global variables
N = 9                           # Tic Tac Toe size of 3x3
empty_cell = 10                 # Empty cell value
three_values = [-3, 3]          # Triple 1 or triple -1
playerManager = PlayerManager()

if os.path.exists("../results/output.csv"):
    output = pd.read_csv("../results/output.csv", sep=";", index_col=0)
else:
    output = pd.DataFrame(index=['Player_1', 'Player_2'], data = {'win':0,'loss':0,'draw':0} )
cross = 1 if(playerManager.player_2.token_value) else -1
circle = -1 if(playerManager.player_2.token_value) else 1