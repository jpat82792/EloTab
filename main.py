from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.listview import ListView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import pdf_config
import enter_section_name
import tab_creation
from functools import partial
import logic
import add_courier
import win32timezone


Config.set("graphics", "resizable", "0")


'''Manager holds all screens. Through the manager you are able to access any aspect of the program if you choose'''


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.first_screen = Screen(name="main")
        self.first_screen_content = tab_creation.BoxLayoutTabCreation(manager=self)
        self.first_screen.add_widget(self.first_screen_content)
        self.second_screen = Screen(name="pdf_config")
        self.second_screen_content = pdf_config.BoxLayoutPDFConfig(manager=self)
        self.second_screen.add_widget(self.second_screen_content)
        self.third_screen = Screen(name="enter_section_name")
        self.third_screen_content = enter_section_name.BoxLayoutEnterSectionName(manager=self)
        self.third_screen.add_widget(self.third_screen_content)
        self.add_widget(self.third_screen)
        # self.fourth_screen = Screen(name="FileChooser")
        # self.fourth_screen_content = BoxLayoutFileBrowser(manager=self)
        # self.fourth_screen.add_widget(self.fourth_screen_content)
        # self.fifth_screen = Screen(name="NamePDF")


class TestApp(App):

    def build(self):
        self.title = "EloTab"
        Window.clearcolor = (0.04705, 0.1019, .10588, 1)
        self.icon = 'EloTabLogo16.png'
        return Manager()

if __name__ == "__main__":
    TestApp().run()
