from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import StringProperty,ObjectProperty,ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior,ButtonBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.checkbox import CheckBox
from kivy import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import SpinnerOption,Spinner
from kivy.factory import Factory
from kivy.graphics import Canvas,Color,Rectangle
from kivymd.uix.picker import MDDatePicker
from kivymd.theming import ThemeManager
from datetime import datetime as dt, timedelta,datetime
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatIconButton,MDRectangleFlatIconButton,MDFillRoundFlatIconButton
import pymysql
import hashlib



try:
    con = pymysql.connect("Localhost", "root", "", "afsczim")
    cur = con.cursor()
except Exception:
   pass









