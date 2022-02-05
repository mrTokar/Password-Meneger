from kivy.config import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window



class Main_menu(GridLayout):
    def __init__(self, **var_args):
        super(Main_menu, self).__init__(**var_args)

        #setting window size
        Window.size = (500, 700)

        #setting window title





# the Base Class of our Kivy App
class MyApp(App):
    def build(self):
        Config.set("kivy", "window_icon", "icon.ico")
        self.title = ("Pasword manager")
        return Main_menu()


if __name__ == '__main__':
    Config.set("kivy", "window_icon", "icon.ico")
    MyApp().run()