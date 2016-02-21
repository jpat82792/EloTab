from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from functools import partial
import custom_button
import file_browsing
import logic


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
        self.button_confirm_pdf = custom_button.EloButton(text="Create PDF", size_hint=(None, None), width=200,
                                                          height=50, pos_hint={"y": .5, "x": .5})
        self.button_confirm_pdf.bind(on_release=self.confirm_sections)
        self.button_back = custom_button.EloButton(text="Back", size_hint=(None, None), width=200, height=50,
                                     pos_hint={"y": .5, "x": 6})
        self.button_back.bind(on_release=self.back_button)
        self.model_holder = ""
        self.add_section = custom_button.EloButton(text="Add", size_hint=(.3, .4), pos_hint={"y": .6})
        self.add_section.bind(on_release=self.change_selected_section)
        self.remove_section = custom_button.EloButton(text="Remove", size_hint=(.3, .4), pos_hint={"y": .6})
        self.remove_section.bind(on_release=self.change_selected_section)
        self.label_save_pdf = Label(text="Enter Name of PDF", size_hint=(.2, None))
        self.file_browser = file_browsing.BoxLayoutFileBrowser(manager=manager)
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