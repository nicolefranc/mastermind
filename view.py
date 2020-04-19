import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

Window.fullscreen = "auto"
Window.resizable = 0

class WindowManager(ScreenManager):
  pass

class MenuScreen(Screen):
  pass

class GameScreen(Screen):
  # label = StringProperty("Test")
  rows = [
    {
      "pegs": [0, 1, 2, 4], "keys": 1
    },
    {
      "pegs": [1, 3, 5, 7], "keys": 1
    }
  ]*4

  def __init__(self, **kwargs):
    super(GameScreen, self).__init__(**kwargs)
    container = GridLayout(cols=3)
    self.add_widget(container)

    r_container = BoxLayout(orientation="vertical", spacing=20, padding=(75, 75))
    for row in self.rows:
      r_container.add_widget(Row(row))
    l2 = Actions()
    l3 = Label(text="Empty space")
    container.add_widget(r_container)
    container.add_widget(l2)
    container.add_widget(l3)

class Actions(BoxLayout):
  def __init__(self, **kwargs):
    super(Actions, self).__init__(**kwargs)
    self.orientation = "vertical"
    self.size_hint = (0.1, 1)
    self.spacing = 0
    self.padding = (0,75)
    colors = [[1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1], [0, 1, 0, 1], [0, 1, 1, 1], [0, 0, 1, 1], [1, 0, 1, 1], [1, 0.65, 0, 1]]
    
    # Color buttons
    c_container = BoxLayout(orientation="vertical", spacing=10)
    for color in colors:
      c_container.add_widget(Button(background_color=color, size_hint=(1, 0.5)))

    # Menu buttons
    # ok, undo, reset, quit
    m_container = BoxLayout(orientation="vertical", spacing=20, padding=(0,100))
    confirm_btn = Button(text="Confirm")
    undo_btn = Button(text="Undo")
    reset_btn = Button(text="Reset")
    quit_btn = Button(text="Quit")
    m_container.add_widget(confirm_btn)
    m_container.add_widget(undo_btn)
    m_container.add_widget(reset_btn)
    m_container.add_widget(quit_btn)

    self.add_widget(c_container)
    self.add_widget(m_container)


# class Palette():
#   def __init__(self, colors):
#     # for color in colors:
#     pass
      

class Row(BoxLayout):
  def __init__(self, row, **kwargs):
    super(Row, self).__init__(**kwargs)
    self.orientation = "horizontal"

    # Pegs
    for row in range(4):
      self.add_widget(Button(text="PEG"))

    # Keys  
    self.add_widget(Keys())

class Pegs(BoxLayout):
  def __init__(self, pegs, **kwargs):
    super(Pegs, self).__init__(**kwargs)
    for peg in pegs:
      self.add_widget(Button(text=str(peg)))

class Keys(GridLayout):
  def __init__(self, keys=range(4), **kwargs):
    super(Keys, self).__init__(**kwargs)
    self.cols = 2
    for key in keys:
      self.add_widget(Label(text="O"))

class MastermindApp(App):
  def build(self):
    sm = self.setup()
    return sm

  def setup(self):
    kv = Builder.load_file("mastermind.kv")
    sm = WindowManager()
    screens = [
      MenuScreen(name="menu"), GameScreen(name="game")
    ]
    for screen in screens:
      sm.add_widget(screen)

    sm.current = "game"
    return sm


if __name__ == "__main__":
  MastermindApp().run()