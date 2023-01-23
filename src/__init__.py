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

from kivy.lang import Builder
from kivy.app import App 
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image

from kivy.clock import Clock, mainthread
from kivy.graphics import Line, Color, Rectangle, Ellipse, RoundedRectangle

from threading import Thread
from functools import partial
from abc import ABC, abstractmethod

# Global variables
N = 9                           # Tic Tac Toe size of 3x3
empty_cell = 10                 # Empty cell value
three_values = [-3, 3]          # Triple 1 or triple -1

if os.path.exists("../results/output.csv"):
    output = pd.read_csv("../results/output.csv", sep=";", index_col=0)
else:
    output = pd.DataFrame(index=['Player_1', 'Player_2'], data = {'win':0,'loss':0,'draw':0} )