from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.listview import ListView
import custom_button

class BoxLayoutEnterSectionName(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutEnterSectionName, self).__init__(**kwargs)
        # GUI for first screen where song name is entered
        self.orientation = "horizontal"
        self.pos_hint = {"y": .85}
        self.textinput_song_name = TextInput(text="Enter Song Section Name (Make each name unique)",
                                             size_hint=(.333, .15), pos_hint={'center_x': .3, "y": 0})
        self.button_confirm_section_name = custom_button.EloButton(text="Confirm Section Name", size_hint=(.333, .15),
                                                     pos_hint={'center_x': .6, "y": 0}, text_size=(180, 50),
                                                     valign="middle")
        self.button_confirm_section_name.bind(on_release=self.confirm_section_name)
        self.array_created_section = ["Created Sections"]
        self.listview_created_section = ListView(item_strings=self.array_created_section,  size_hint=(.333, .15),
                                                 pos_hint={'center_x': .8, "y": 0})
        self.add_widget(self.textinput_song_name)
        self.add_widget(self.button_confirm_section_name)
        self.add_widget(self.listview_created_section)
        self.manager = manager

    def confirm_section_name(self, btn):
        confirm_section = False
        for item in self.array_created_section:
            # If any section is identically named, the program would break when the user selects what sections to place
            # in the pdf. This throws a warning to the user and prevents this from happening.
            if self.textinput_song_name.text == item:
                confirm_section = False
                temp = btn.text
                temp += " * Need a unique name *"
                btn.text = temp
                break
            else:
                confirm_section = True
                self.button_confirm_section_name.text = "Confirm Section Name"
# Only enter this block if the name is confirmed as unique
        if confirm_section:
            self.manager.first_screen_content.section_name = self.textinput_song_name.text
            self.array_created_section.append(self.textinput_song_name.text)
            self.listview_created_section.item_strings = self.array_created_section
            self.manager.switch_to(self.manager.first_screen)
