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
        self.first_screen_content = BoxLayoutTabCreation(manager=self)
        self.first_screen.add_widget(self.first_screen_content)
        self.second_screen = Screen(name="pdf_config")
        self.second_screen_content = BoxLayoutPDFConfig(manager=self)
        self.second_screen.add_widget(self.second_screen_content)
        self.third_screen = Screen(name="enter_section_name")
        self.third_screen_content = BoxLayoutEnterSectionName(manager=self)
        self.third_screen.add_widget(self.third_screen_content)
        self.add_widget(self.third_screen)
        self.fourth_screen = Screen(name="FileChooser")
        self.fourth_screen_content = BoxLayoutFileBrowser(manager=self)
        self.fourth_screen.add_widget(self.fourth_screen_content)
        self.fifth_screen = Screen(name="NamePDF")

# This handles file browsing on the section selection/create pdf final screen


class BoxLayoutFileBrowser(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutFileBrowser, self).__init__(**kwargs)
        self.manager = manager
        self.orientation = "horizontal"
        self.browser = FileChooserIconViewSaveLocation(size_hint=(.5, 1))
        self.browser_label = Label(text="Choose a location to save your PDF", size_hint=(.5, .20), pos_hint={"y": .315})
        self.add_widget(self.browser_label)
        self.add_widget(self.browser)
# Gathers path to chosen directory

    def get_path(self, btn):
        self.manager.second_screen_content.file_path = self.browser.path
        self.manager.switch_to(self.manager.first_screen)

# Initializes where the filebrowser views first. ie


class FileChooserIconViewSaveLocation(FileChooserListView):
    def __init__(self, **kwargs):
        super(FileChooserIconViewSaveLocation, self).__init__(**kwargs)
        self.path = "/"
# Default "Elothought" styled button, referred to as EloButton


class EloButton(Button):
    def __init__(self, **kwargs):
        super(EloButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_color = [.019607, .2705, .29019, 1]
        self.background_down = ""
# Child of ToggleButton with added attributes.


class ToggleButtonFretBoard(ToggleButton):
    def __init__(self, tool_state, preview_labels, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        self.tool_state = tool_state
        self.instruction = "No Instruction"
        self.preview = preview_labels
        self.background_normal = ""
        self.background_color = [.019607, .2705, .29019, 1]
# "change_instruction" changes instruction for guitar tab.

    def change_instruction(self, btn):
        if btn.group == 'e':
            self.preview.label_array[0].operation = self.tool_state.state_container
        if btn.group == 'B':
            self.preview.label_array[1].operation = self.tool_state.state_container
        if btn.group == "G":
            self.preview.label_array[2].operation = self.tool_state.state_container
        if btn.group == "D":
            self.preview.label_array[3].operation = self.tool_state.state_container
        if btn.group == "A":
            self.preview.label_array[4].operation = self.tool_state.state_container
        if btn.group == "E":
            self.preview.label_array[5].operation = self.tool_state.state_container
        self.instruction = self.tool_state.state_container


class BoxLayoutEnterSectionName(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutEnterSectionName, self).__init__(**kwargs)
        # GUI for first screen where song name is entered
        self.orientation = "horizontal"
        self.pos_hint = {"y": .85}
        self.textinput_song_name = TextInput(text="Enter Song Section Name (Make each name unique)",
                                             size_hint=(.333, .15), pos_hint={'center_x': .3, "y": 0})
        self.button_confirm_section_name = EloButton(text="Confirm Section Name", size_hint=(.333, .15),
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


class BoxLayoutPDFConfig(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutPDFConfig, self).__init__(**kwargs)
        # GUI for pdf configuration and creation
        self.orientation = "vertical"
        self.padding = 5
        self.spacing = 5
        self.manager = manager
        self.gridlayout_buttons = GridLayout()
        self.gridlayout_buttons.size_hint = (1, 1)
        self.file_path = "/"
        self.listview_array = ["Selected Sections"]
        self.listview_test = ListView(item_strings=self.listview_array, size_hint=(.3, 1), pos_hint={"y": 0})
        self.selected_sections = []
        self.section_options = []
        colored_dropdown = partial(DropDown, bar_color=(1, .2705, .29019, 1))

        self.spinner_sections = Spinner(text="Sections", values=self.section_options,
                                        size_hint=(.3, .4), pos_hint={"y": .6},
                                        background_normal="",
                                        background_color=[.019607, .2705, .29019, 1],
                                        dropdown_cls=colored_dropdown)
        self.button_confirm_pdf = EloButton(text="Create PDF", size_hint=(None, None), width=200, height=50,
                                            pos_hint={"y": .5, "x": .5})
        self.button_confirm_pdf.bind(on_release=self.confirm_sections)
        self.button_back = EloButton(text="Back", size_hint=(None, None), width=200, height=50,
                                     pos_hint={"y": .5, "x": 6})
        self.button_back.bind(on_release=self.back_button)
        self.model_holder = ""
        self.add_section = EloButton(text="Add", size_hint=(.3, .4), pos_hint={"y": .6})
        self.add_section.bind(on_release=self.change_selected_section)
        self.remove_section = EloButton(text="Remove", size_hint=(.3, .4), pos_hint={"y": .6})
        self.remove_section.bind(on_release=self.change_selected_section)
        self.label_save_pdf = Label(text="Enter Name of PDF", size_hint=(.2, None))
        self.file_browser = BoxLayoutFileBrowser(manager=manager)
        self.textinput_pdf_name = TextInput(size_hint=(.2, None))
        self.boxlayout_first_row = BoxLayout(orientation="horizontal")
        self.boxlayout_first_row.add_widget(self.spinner_sections)
        self.boxlayout_first_row.add_widget(self.add_section)
        self.boxlayout_first_row.add_widget(self.remove_section)
        self.boxlayout_first_row.add_widget(self.listview_test)
        self.add_widget(self.boxlayout_first_row)
        self.add_widget(self.file_browser)
        self.boxlayout_second_row = BoxLayout(orientation="horizontal")
        self.boxlayout_second_row.add_widget(self.label_save_pdf)
        self.boxlayout_second_row.add_widget(self.textinput_pdf_name)
        self.add_widget(self.boxlayout_second_row)
        self.boxlayout_third_row = BoxLayout(orientation="horizontal", pos_hint={"x": .25})
        self.boxlayout_third_row.add_widget(self.button_confirm_pdf)
        self.boxlayout_third_row.add_widget(self.button_back)
        self.add_widget(self.boxlayout_third_row)
# Either adds section or deletes. btn returns the button. The text is used to confirm the operation

    def change_selected_section(self, btn):
        if btn.text == "Add":
            self.listview_array.append(self.spinner_sections.text)
            self.listview_test.item_strings = self.listview_array
        else:
            try:
                # If block prevents deletion of name of listview
                if len(self.listview_array) == 1:
                    print("Don't delete me!!")
                # Else block removes added sections
                else:
                    self.listview_array.pop()
                    self.listview_test.item_strings = self.listview_array
            except IndexError:
                pass
# Permits you to go back to the tab creation portion of app

    def back_button(self, btn):
        self.manager.switch_to(self.manager.first_screen)
# Confirms the sections are correct and then the pdf is generated!!

    def confirm_sections(self, btn):
        if self.listview_array[0] == "Selected Sections":
            self.listview_array.pop(0)

        if self.textinput_pdf_name.text != "":
            self.model_holder = logic.ModelGeneratePDF(manager=self.manager, path=self.file_browser.browser.path,
                                                       file_name=self.textinput_pdf_name.text)
            self.label_save_pdf.text = " Enter Name of PDF"
            self.model_holder.gather_sections()
            self.model_holder.draw_sections_to_pdf()
        else:
            temp = self.label_save_pdf.text
            temp += " ** Please name your PDF **"
            self.label_save_pdf.text = temp
        self.listview_array.insert(0, "Selected Sections")
# BoxLayoutTabCreation controls the gui for tab creation.


class BoxLayoutTabCreation(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutTabCreation, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.section_name = "None"
        self.toolbox = BoxLayoutToolBox()
        self.toolbox2 = GridLayoutToolBox2(manager=manager)
        self.preview = Preview(manager=manager, pos_hint={"y": .5})
        self.fretboard = ToggleButtonLayout(preview_array=self.toolbox, preview_access=self.preview, pos_hint={"y": .5})
        self.hold = ""
        self.section_holder = []
        self.manager = manager
        self.dropdown_menu = DropDownMainMenu(manager=self.manager)
        self.dropdown_menu = DropDownMainMenu(manager=self.manager)
        self.text_label_array = 0
        self.switch_standard_12 = True
        self.add_widget(self.dropdown_menu.button_main)
        self.add_widget(self.toolbox)
        self.add_widget(self.toolbox2)
        self.add_widget(self.fretboard)
        self.add_widget(self.preview)
# Translates instructions for guitar tab

    def translate_instruction(self, instruction):
        if instruction == "Hammer On":
            return "h"
        if instruction == "Pull Off":
            return "p"
        if instruction == "Slide Up":
            return "/"
        if instruction == "Slide Down":
            return "\\"
        if instruction == "Harmonic":
            return "*"
        if instruction == "Mute":
            return "X"
        if instruction == "Tremelo":
            return "~"
# User confirms section and is then led back to section naming screen

    def confirm_section(self, btn):
        created_song_section = SongSection(name=self.section_name)
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

# Holds button to add/remove notes, to confirm section, create new section


class GridLayoutToolBox2(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(GridLayoutToolBox2, self).__init__(**kwargs)
        self.cols = 5
        self.spacing = 5
        self.orientation = "horizontal"
        self.pos_hint = {"y": 1.375}
        self.current = []
        self.previous = []
        self.manager = manager
        self.button_height_per = .2
        button_height_per = .27
        button_width_per = .9
        self.button_height = 40
        self.button_width = 150
        self.trial_button = EloButton(text="Add Note(s)", size_hint=(button_width_per, button_height_per),
                                      pos_hint=self.pos_hint)
        self.trial_button.bind(on_release=self.add_note)
        self.button_confirm_section = EloButton(text="Confirm Section", size_hint=(button_width_per, button_height_per),
                                                pos_hint=self.pos_hint)
        self.button_confirm_section.bind(on_release=self.confirm_section)
        self.button_remove_last_chord = EloButton(text="Remove Last",  size_hint=(button_width_per, button_height_per),
                                                  pos_hint=self.pos_hint)
        self.button_remove_last_chord.bind(on_release=self.remove_last_note)
        self.button_0_12 = EloButton(text="Fretboard 0-12", size_hint=(button_width_per, button_height_per),
                                     pos_hint=self.pos_hint)
        self.button_0_12.bind(on_release=self.change_fretboard)
        self.button_12_24 = EloButton(text="Fretboard 12-24", size_hint=(button_width_per, button_height_per),
                                      pos_hint=self.pos_hint)
        self.button_12_24.bind(on_release=self.change_fretboard)
        self.holding_notes = ["", "", "", "", "", ""]
        self.holding_instructions = ["", "", "", "", "", ""]
        self.add_widget(self.trial_button)
        self.add_widget(self.button_confirm_section)
        self.add_widget(self.button_remove_last_chord)
        self.add_widget(self.button_0_12)
        self.add_widget(self.button_12_24)

    def change_fretboard(self, btn):
        x = 0
        # Stores selected instructions
        for string in self.manager.first_screen_content.fretboard.neck:
            for note in string:
                if note.state == "down":
                    control = self.manager.first_screen_content.preview.label_array[x].operation
                    # This stores instruction in the event
                    # if control == "Hammer On" or control == "Pull Off" or control == "Slide Up" or\
                    #    control == "Slide Down" or control == "Harmonic":
                    if control != "No Instruction":
                        self.holding_instructions[x] = self.manager.first_screen_content.translate_instruction(
                            self.manager.first_screen_content.preview.label_array[x].operation)
            x += 1

        if btn.text == "Fretboard 12-24":
            x = 0
            # Gathers pressed notes and changes the button state back to normal
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 0
                for note in string:
                    if note.state == "down":
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.\
                            label_array[x].child_label.text
                        if i >= 10:
                            self.holding_notes[x] = self.holding_notes[x] + str(i) + "-"
                        else:
                            self.holding_notes[x] = self.holding_notes[x] + str(i) + "-"
                        note.state = "normal"
                    i += 1
                x += 1
            self.manager.first_screen_content.switch_standard_12 = False
            # Changes fretboard
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 12
                for note in string:
                    note.text = str(i)
                    i += 1
        elif btn.text == "Fretboard 0-12":
            x = 0
            # Gathers pressed notes and changes the button state back to normal
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 12
                for note in string:
                    if note.state == "down":
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.\
                            label_array[x].child_label.text
                        if i >= 10:
                            self.holding_notes[x] = self.holding_notes[x] + str(i) + "-"
                        else:
                            self.holding_notes[x] = self.holding_notes[x] + str(i) + "-"
                        note.state = "normal"
                    i += 1
                x += 1
            self.manager.first_screen_content.switch_standard_12 = True
            # Changes fretboard
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 0
                for note in string:
                    note.text = str(i)
                    i += 1
# This removes the last note(s). Has a try catch to avoid program crashing when user presses button and there is nothing
# to remove

    def remove_last_note(self, btn):
        try:
            difference = self.previous[-1]
            self.previous.pop()
            for label in self.manager.first_screen_content.preview.label_array:
                temp = label.child_label.text[:difference]
                label.child_label.text = temp
        except IndexError:
            pass
# Leads back to section naming screen

    def confirm_section(self, btn):
        created_song_section = SongSection(name=self.manager.first_screen_content.section_name)
        for label in self.manager.first_screen_content.preview.label_array:
            created_song_section.section.append(label.child_label.text)
        self.manager.first_screen_content.preview.label_array[0].child_label.text = "e|--"
        self.manager.first_screen_content.preview.label_array[1].child_label.text = "B|--"
        self.manager.first_screen_content.preview.label_array[2].child_label.text = "G|--"
        self.manager.first_screen_content.preview.label_array[3].child_label.text = "D|--"
        self.manager.first_screen_content.preview.label_array[4].child_label.text = "A|--"
        self.manager.first_screen_content.preview.label_array[5].child_label.text = "E|--"
        self.manager.first_screen_content.section_holder.append(created_song_section)
        self.manager.switch_to(self.manager.third_screen)

    ''' This loop gathers instructions if any instructions are pressed.
    1. Appends instructions to preview.label.child_text.
    2. This ensures notes line up, regardless of differences of instruction length
    3. Checks if not is pressed. If pressed, records note
    4. Finds longest label.child_label.text
    5. Finds difference between longest text and current string '''
    def add_note(self, btn):
        if self.manager.first_screen_content.switch_standard_12:
            x = 0
            longest_string2 = 0
            # 1st loop
            for string in self.manager.first_screen_content.fretboard.neck:
                for note in string:
                    if note.state == "down":
                        control = self.manager.first_screen_content.preview.label_array[x].operation
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.\
                            label_array[x].child_label.text
                        # if control == "Hammer On" or control == "Pull Off" or control == "Slide Up" \
                        #         or control == "Slide Down" or control == "Harmonic":
                        if control != "No Instruction":
                            self.holding_instructions[x] = self.manager.first_screen_content.translate_instruction(
                                self.manager.first_screen_content.preview.label_array[x].operation)
                        else:
                            self.holding_instructions[x] = ""
                x += 1
            # This sees which instruction is the longest
            for i in range(0, 6):
                if len(self.holding_instructions[i]) > longest_string2:
                    longest_string2 = len(self.holding_instructions[i])


            # 2nd loop
            for i in range(0, 6):
                if longest_string2 > len(self.holding_instructions[i]):
                    difference = longest_string2 - len(self.holding_instructions[i])
                    self.holding_instructions[i] += (difference * "-")
            # 3rd loop
            x = 0
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 0
                for note in string:
                    if note.state == "down":
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.\
                                                                 label_array[x].child_label.text
                        if i >= 10:
                            self.holding_notes[x] = str(i) + "-"
                        else:
                            self.holding_notes[x] = str(i) + "-"
                        note.state = "normal"
                    i += 1
                x += 1
            longest_string = 0
            # 4th loop
            fourth_loop = 0
            for i in range(0, 6):
                if len(self.holding_notes[i]) > longest_string:
                    longest_string = len(self.holding_notes[i])
                fourth_loop += 1

            # 5th loop
            fifth_loop = 0
            for i in range(0, 6):
                difference = longest_string - len(self.holding_notes[i])
                self.holding_notes[i] += (difference * "-")
                fifth_loop += 1
            x = 0
            self.previous.append(len(self.manager.first_screen_content.preview.label_array[0].child_label.text))
            for label in self.manager.first_screen_content.preview.label_array:
                label.child_label.text = label.child_label.text + self.holding_instructions[x] + self.holding_notes[x]
                x += 1

            self.holding_notes = ["", "", "", "", "", ""]
            self.holding_instructions = ["", "", "", "", "", ""]

        else:
            x = 0
            longest_string2 = 0
            # 1st loop
            for string in self.manager.first_screen_content.fretboard.neck:
                for note in string:
                    if note.state == "down":
                        control = self.manager.first_screen_content.preview.label_array[x].operation
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.\
                            label_array[x].child_label.text
                        # if control == "Hammer On" or control == "Pull Off" or control == "Slide Up" or \
                        #    control == "Slide Down" or control == "Harmonic":
                        if control != "No Instruction":
                            self.holding_instructions[x] = self.manager.first_screen_content.translate_instruction(
                                self.manager.first_screen_content.preview.label_array[x].operation)
                        else:
                            self.holding_instructions[x] = ""
                x += 1

                # This sees which instruction is the longest
            for i in range(0, 6):
                if len(self.holding_instructions[i]) > longest_string2:
                    longest_string2 = len(self.holding_instructions[i])

            # 2nd loop

            for i in range(0, 6):
                if longest_string2 > len(self.holding_instructions[i]):
                    difference = longest_string2 - len(self.holding_instructions[i])
                    self.holding_instructions[i] += (difference * "-")

            # 3rd loop
            x = 0
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 12
                for note in string:
                    if note.state == "down":
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.label_array[x].child_label.text
                        if i >= 10:
                            self.holding_notes[x] = str(i) + "-"
                        else:
                            self.holding_notes[x] = str(i) + "-"
                        note.state = "normal"
                    i += 1
                x += 1
            longest_string = 0

            # 4th loop
            for i in range(0, 6):
                if len(self.holding_notes[i]) > longest_string:
                    longest_string = len(self.holding_notes[i])

            # 5th loop
            for i in range(0, 6):
                difference = longest_string - len(self.holding_notes[i])
                self.holding_notes[i] += (difference * "-")

            self.previous.append(len(self.manager.first_screen_content.preview.label_array[0].child_label.text))
            x = 0
            for label in self.manager.first_screen_content.preview.label_array:
                label.child_label.text = label.child_label.text + self.holding_instructions[x] + self.holding_notes[x]
                x += 1

            self.holding_notes = ["", "", "", "", "", ""]
            self.holding_instructions = ["", "", "", "", "", ""]


class LabelPreview(ScrollView):
    def __init__(self, child_text, child_halign, child_pos_hint, **kwargs):
        super(LabelPreview, self).__init__(**kwargs)
        self.operation = "No Operation"
        self.text = StringProperty("")
        self.child_label=Label(text=child_text, halign=child_halign, pos_hint=child_pos_hint)
        self.add_widget(self.child_label)


class SongSection:
    def __init__(self, name):
        self.section = []
        self.name = name


class DropDownMainMenu(DropDown):
    def __init__(self, manager, **kwargs):
        super(DropDownMainMenu, self).__init__(**kwargs)
        button_create_pdf = EloButton(text="Create PDF", size_hint=(None, None), height=20, width=100)
        button_create_pdf.bind(on_release=self.generate_popup)
        self.pos = (10, 10)
        self.add_widget(button_create_pdf)
        self.button_main = EloButton(text="Main Menu", size_hint_y=None, height=20, size_hint_x=.125)
        self.button_main.bind(on_release=self.open)
        self.manager = manager

    def generate_popup(self, btn):
        for section in self.manager.first_screen_content.section_holder:
            self.manager.second_screen_content.section_options.append(section.name)
        self.manager.second_screen_content.spinner_sections.values = self.manager.second_screen_content.section_options
        self.manager.switch_to(self.manager.second_screen)


class Preview(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(Preview, self).__init__(**kwargs)
        self.rows = 6
        self.orientation = "horizontal"
        self.current_font_size = 18
        self.font_label = "courier new"
        self.pos_hint = {"y": 0}
        self.boxlayout_container = BoxLayout(orientation="vertical", pos_hint={"y": .9})
        hint_for_children = {"y":1.5}

        self.temp1 = LabelPreview(child_text="e|--", child_halign="left", child_pos_hint=hint_for_children)
        self.temp1.child_label.bind(size=self.temp1.child_label.setter('texture_size'))
        self.temp1.child_label.font_name = self.font_label
        self.temp1.child_label.text_size = (770,0)
        self.temp1.child_label.texture_size = [600, 18]
        self.boxlayout_container.add_widget(self.temp1)
        self.temp2 = LabelPreview(child_text="B|--",  child_halign="left", child_pos_hint=hint_for_children)
        self.temp2.child_label.font_name = self.font_label
        self.temp2.child_label.texture_size = [600, 18]
        self.temp2.child_label.text_size = (770, 0)
        self.temp2.bind(size=self.temp2.child_label.setter('texture_size'))
        self.temp2.child_label.texture_update()
        self.boxlayout_container.add_widget(self.temp2)

        self.temp3 = LabelPreview(child_text="G|--", child_halign="left", child_pos_hint=hint_for_children)
        self.temp3.child_label.font_name = self.font_label
        self.temp3.child_label.text_size = (770, 0)
        self.temp3.child_label.texture_size = [600, 18]
        self.temp3.bind(size=self.temp3.child_label.setter("texture_size"))
        self.boxlayout_container.add_widget(self.temp3)

        self.temp4 = LabelPreview(child_text="D|--",  child_halign="left", child_pos_hint=hint_for_children)
        self.temp4.child_label.font_name = self.font_label
        self.temp4.child_label.text_size = (770, 0)
        self.temp4.child_label.texture_size = [600, 18]
        self.temp4.bind(size=self.temp4.child_label.setter("texture_size"))
        self.boxlayout_container.add_widget(self.temp4)

        self.temp5 = LabelPreview(child_text="A|--", child_halign="left", child_pos_hint=hint_for_children)
        self.temp5.child_label.font_name = self.font_label
        self.temp5.child_label.text_size = (770, 0)
        self.temp5.child_label.texture_size = [600, 18]
        self.temp5.bind(size=self.temp5.child_label.setter("texture_size"))
        self.boxlayout_container.add_widget(self.temp5)

        self.temp6 = LabelPreview(child_text="E|--",  child_halign="left", child_pos_hint=hint_for_children)
        self.temp6.child_label.font_name = self.font_label
        self.temp6.child_label.text_size = (770, 0)
        self.temp6.child_label.texture_size = [600, 18]
        self.temp6.bind(size=self.temp6.child_label.setter("texture_size"))
        self.boxlayout_container.add_widget(self.temp6)
        self.add_widget(self.boxlayout_container)
        self.label_array = [self.temp1, self.temp2, self.temp3, self.temp4, self.temp5, self.temp6]


class ToggleButtonLayout(BoxLayout):
    def __init__(self, preview_array, preview_access, **kwargs):
        super(ToggleButtonLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 5
        self.e_string = []
        self.b_string = []
        self.g_string = []
        self.d_string = []
        self.a_string = []
        self.E_string = []
        self.pos_hint = {"center_y": 8}
        self.neck = [self.e_string, self.b_string, self.g_string,
                     self.d_string, self.a_string, self.E_string]
        self.array_rows = [BoxLayout(orientation="horizontal", pos_hint=self.pos_hint, spacing=5),
                           BoxLayout(orientation="horizontal", pos_hint=self.pos_hint, spacing=5),
                           BoxLayout(orientation="horizontal", pos_hint=self.pos_hint, spacing=5),
                           BoxLayout(orientation="horizontal", pos_hint=self.pos_hint, spacing=5),
                           BoxLayout(orientation="horizontal", pos_hint=self.pos_hint, spacing=5),
                           BoxLayout(orientation="horizontal", pos_hint=self.pos_hint, spacing=5)]
        self.cols = 13
        self.i = 0
        j = 0
        while self.i <= 12:
            temp1 = ToggleButtonFretBoard(text=str(self.i), group="e", tool_state=preview_array,
                                          preview_labels=preview_access, size_hint_x=.07629, pos_hint=self.pos_hint)
            temp1.bind(on_press=temp1.change_instruction)
            temp2 = ToggleButtonFretBoard(text=str(self.i), group="B", tool_state=preview_array,
                                          preview_labels=preview_access, size_hint_x=.07629, pos_hint=self.pos_hint)
            temp2.bind(on_press=temp2.change_instruction)
            temp3 = ToggleButtonFretBoard(text=str(self.i), group="G", tool_state=preview_array,
                                          preview_labels=preview_access, size_hint_x=.07629, pos_hint=self.pos_hint)
            temp3.bind(on_press=temp3.change_instruction)
            temp4 = ToggleButtonFretBoard(text=str(self.i), group="D", tool_state=preview_array,
                                          preview_labels=preview_access, size_hint_x=.07629, pos_hint=self.pos_hint)
            temp4.bind(on_press=temp4.change_instruction)
            temp5 = ToggleButtonFretBoard(text=str(self.i), group="A", tool_state=preview_array,
                                          preview_labels=preview_access, size_hint_x=.07629, pos_hint=self.pos_hint)
            temp5.bind(on_press=temp5.change_instruction)
            temp6 = ToggleButtonFretBoard(text=str(self.i), group="E", tool_state=preview_array,
                                          preview_labels=preview_access, size_hint_x=.07629, pos_hint=self.pos_hint)
            temp6.bind(on_press=temp6.change_instruction)
            self.neck[0].append(temp1)
            self.neck[1].append(temp2)
            self.neck[2].append(temp3)
            self.neck[3].append(temp4)
            self.neck[4].append(temp5)
            self.neck[5].append(temp6)
            self.i += 1
        for button in self.neck:
            for note in button:
                self.array_rows[j].add_widget(note)
            j += 1
        for string in self.array_rows:
            self.add_widget(string)


class BoxLayoutToolBox(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayoutToolBox, self).__init__(**kwargs)
        self.spacing = 5
        self.padding = 5
        self.orientation = "horizontal"
        self.button_height = 50
        self.button_width = 100
        self.pos_hint = {"y": 0.7}
        self.state_container = "No Instruction"
        hammer = ToggleButton(text="Hammer On", group="tools", size_hint_y=.3, pos_hint=self.pos_hint,
                              background_normal="", background_color=[.019607, .2705, .29019, 1])
        hammer.bind(on_press=self.change_state)
        pull = ToggleButton(text="Pull Off", group="tools", size_hint_y=.3, pos_hint=self.pos_hint,
                            background_normal="", background_color=[.019607, .2705, .29019, 1])
        pull.bind(on_press=self.change_state)
        slide_up = ToggleButton(text="Slide Up", group="tools", size_hint_y=.3, pos_hint=self.pos_hint,
                                background_normal="", background_color=[.019607, .2705, .29019, 1])
        slide_up.bind(on_press=self.change_state)
        slide_down = ToggleButton(text="Slide Down", group="tools", size_hint_y=.3, pos_hint=self.pos_hint,
                                  background_normal="", background_color=[.019607, .2705, .29019, 1])
        slide_down.bind(on_press=self.change_state)
        mute = ToggleButton(text="Mute", group="tools", size_hint_y=.3, pos_hint=self.pos_hint, background_normal="",
                            background_color=[.019607, .2705, .29019, 1])
        mute.bind(on_press=self.change_state)
        trem = ToggleButton(text="Tremelo", group="tools", size_hint_y=.3, pos_hint=self.pos_hint, background_normal="",
                            background_color=[.019607, .2705, .29019, 1])
        trem.bind(on_press=self.change_state)
        harmonic = ToggleButton(text="Harmonic", group="tools", size_hint_y=.3, pos_hint=self.pos_hint,
                                background_normal="", background_color=[.019607, .2705, .29019, 1])
        harmonic.bind(on_press=self.change_state)
        self.family = [hammer, pull, slide_up, slide_down, mute, trem, harmonic]

        for btn in self.family:
            self.add_widget(btn)

    def change_state(self, btn):
        if self.state_container == btn.text:
            self.state_container = "No Instruction"
        else:
            self.state_container = btn.text
        print(self.state_container)


class TestApp(App):

    def build(self):
        self.title = "EloTab"
        Window.clearcolor = (0.04705, 0.1019, .10588, 1)
        return Manager()

if __name__ == "__main__":
    TestApp().run()
