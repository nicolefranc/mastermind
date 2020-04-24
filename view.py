import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import libdw.sm as sm

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
    self.current_row = 0
    self.current_peg = 0
    self.rows = list()

    # View
    container = GridLayout(cols=3)
    self.add_widget(container)

    r_container = BoxLayout(orientation="vertical", spacing=20, padding=(75, 75))
    for i in range(8):
      row = Row()
      self.rows.append(row)
      r_container.add_widget(row)
    l2 = Actions()
    l3 = Button(text="Testing Button", background_color=[1,1,1,1])
    # l2.bind(selected_color=l3.setter('background_color'))
    l2.bind(selected_color=self.on_color_select)
    container.add_widget(r_container)
    container.add_widget(l2)
    container.add_widget(l3)

  # Logic
  def on_color_select(self, instance, selected_color):
    # take current row
    # take current peg based on row
    peg_instance = self.rows[self.current_row].pegs[self.current_peg]
    # change color of peg
    peg_instance.background_color = selected_color[self.current_peg]
    # if last peg, last row -> row,
    #   last peg only -> move to next row (row++), peg back to pos 0
    if self.current_peg == 3:
      if self.current_row == 7:
        return
      self.current_row += 1
      self.current_peg = 0
      # reset the Action object pegs holder 
      instance.pegs = list()
    # else move counter to next peg
    else:
      self.current_peg += 1
    print("Clicked: ", selected_color)


class Actions(BoxLayout):
  selected_color = ListProperty(None)

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
      c_container.add_widget(Button(background_color=color, size_hint=(1, 0.5), on_release=self.on_color_select))

    # Menu buttons
    # ok, undo, reset, quit
    m_container = BoxLayout(orientation="vertical", spacing=20, padding=(0,100,0,0))
    confirm_btn = Button(text="Confirm", background_color=[1, 0, 1, 1])
    undo_btn = Button(text="Undo")
    reset_btn = Button(text="Reset")
    quit_btn = Button(text="Quit")
    m_container.add_widget(confirm_btn)
    m_container.add_widget(undo_btn)
    m_container.add_widget(reset_btn)
    m_container.add_widget(quit_btn)

    self.add_widget(c_container)
    self.add_widget(m_container)

    # Logic
    self.pegs = list()

  def on_color_select(self, instance):
    # self.selected_color = instance.background_color
    self.pegs.append(instance.background_color)
    self.selected_color = self.pegs
    print("confirm is clicked")
    print(instance.background_color)


class Row(BoxLayout):
  def __init__(self, **kwargs):
    super(Row, self).__init__(**kwargs)
    self.orientation = "horizontal"
    self.pegs = list()

    # Pegs
    for row in range(4):
      peg = Button(text="PEG", background_color=[1,1,1,1])
      self.pegs.append(peg)
      self.add_widget(peg)

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

class MastermindApp(App, sm.SM):
  def build(self):
    screen_manager = self.setup()
    return screen_manager

  def setup(self):
    kv = Builder.load_file("mastermind.kv")
    screen_manager = WindowManager()
    screens = [
      MenuScreen(name="menu"), GameScreen(name="game")
    ]
    for screen in screens:
      screen_manager.add_widget(screen)

    screen_manager.current = "game"
    return screen_manager


if __name__ == "__main__":
  MastermindApp().run()