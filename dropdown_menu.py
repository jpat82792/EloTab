from kivy.uix.dropdown import DropDown
import custom_button

class DropDownMainMenu(DropDown):
    def __init__(self, manager, **kwargs):
        super(DropDownMainMenu, self).__init__(**kwargs)
        button_create_pdf = custom_button.EloButton(text="Create PDF", size_hint=(None, None), height=20, width=100)
        button_create_pdf.bind(on_release=self.generate_popup)
        self.pos = (10, 10)
        self.add_widget(button_create_pdf)
        self.button_main = custom_button.EloButton(text="Main Menu", size_hint_y=None, height=20, size_hint_x=.125)
        self.button_main.bind(on_release=self.open)
        self.manager = manager

    def generate_popup(self, btn):
        for section in self.manager.first_screen_content.section_holder:
            self.manager.second_screen_content.section_options.append(section.name)
        self.manager.second_screen_content.spinner_sections.values = self.manager.second_screen_content.section_options
        self.manager.switch_to(self.manager.second_screen)
