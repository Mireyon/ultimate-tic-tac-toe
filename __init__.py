import random
import time
import math
import numpy as np

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

from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Line, Color, Rectangle, Ellipse

from player import PlayerManager
from threading import Thread

# Global variables
N = 9                           # Tic Tac Toe size of 3x3
empty_cell = 10                 # Empty cell value
three_values = [-3, 3]          # Triple 1 or triple -1
width = 800
height = 700
playerManager = PlayerManager()
cross = 1 if(playerManager.player_2.token_value) else -1
circle = -1 if(playerManager.player_2.token_value) else 1

# Window configuration
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', height)
Config.set('graphics', 'width', width)