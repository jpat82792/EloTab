from kivy.uix.boxlayout import BoxLayout
import song_section
import dropdown_menu
import preview
import tab_creation_toolbox
import toggle_button_fretboard
import toolbox_instructions

# BoxLayoutTabCreation controls the gui for tab creation.
class BoxLayoutTabCreation(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutTabCreation, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.section_name = "None"
        self.toolbox = toolbox_instructions.BoxLayoutToolBox()
        self.toolbox2 = tab_creation_toolbox.BoxLayoutToolBox2(manager=manager)
        self.preview = preview.Preview(manager=manager, pos_hint={"y": .5})
        self.fretboard = toggle_button_fretboard.ToggleButtonLayout(preview_array=self.toolbox, preview_access=self.preview, pos_hint={"y": .5})
        self.hold = ""
        self.section_holder = []
        self.manager = manager
        self.dropdown_menu = dropdown_menu.DropDownMainMenu(manager=self.manager)
        self.text_label_array = 0
        self.switch_standard_12 = True
        self.add_widget(self.dropdown_menu.button_main)
        self.add_widget(self.toolbox)
        self.add_widget(self.toolbox2)
        self.add_widget(self.fretboard)
        self.add_widget(self.preview)

# User confirms section and is then led back to section naming screen

    def confirm_section(self, btn):
        created_song_section = song_section.SongSection(name=self.section_name)
        for label in self.preview.label_array:
            created_song_section.section.append(label.text)
        self.preview.label_array[0].text = "e|--"
        self.preview.label_array[1].text = "B|--"
        self.preview.label_array[2].text = "G|--"
        self.preview.label_array[3].text = "D|--"
        self.preview.label_array[4].text = "A|--"
        self.preview.label_array[5].text = "E|--"
        self.section_holder.append(created_song_section)
        self.manager.switch_to(self.manager.third_screen)

    def change_screen(self, btn):
        self.manager.switch_to("pdf_config")