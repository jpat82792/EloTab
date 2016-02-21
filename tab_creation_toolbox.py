import custom_button
from kivy.uix.boxlayout import BoxLayout
import tab_creation_toolbox_logic
import tab_creation_toolbox_logic_add_note
import tab_creation_toolbox_logic


class BoxLayoutToolBox2(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutToolBox2, self).__init__(**kwargs)
        self.cols = 5
        self.spacing = 5
        self.orientation = "horizontal"
        self.pos_hint = {"y": 1.375}
        self.current = []
        self.toolbox2_logic = tab_creation_toolbox_logic.ToolBox2Logic(manager=manager, toolbox=self)
        self.add_note = tab_creation_toolbox_logic_add_note.ToolBox2LogicAddNote(manager=manager, toolbox=self)
        self.previous = []
        self.manager = manager
        self.button_height_per = .2
        button_height_per = .27
        button_width_per = .9
        self.button_height = 40
        self.button_width = 150
        self.trial_button = custom_button.EloButton(text="Add Note(s)",
                                                    size_hint=(button_width_per, button_height_per),
                                                    pos_hint=self.pos_hint)
        self.trial_button.bind(on_release=self.add_note.add_note)
        self.button_confirm_section = custom_button.EloButton(text="Confirm Section",
                                                              size_hint=(button_width_per,button_height_per),
                                                              pos_hint=self.pos_hint)
        self.button_confirm_section.bind(on_release=self.toolbox2_logic.confirm_section)
        self.button_remove_last_chord = custom_button.EloButton(text="Remove Last",  size_hint=(button_width_per,
                                                                button_height_per),
                                                                pos_hint=self.pos_hint)
        self.button_remove_last_chord.bind(on_release=self.toolbox2_logic.remove_last_note)
        self.button_0_12 = custom_button.EloButton(text="Fretboard 0-12",
                                                   size_hint=(button_width_per, button_height_per),
                                                   pos_hint=self.pos_hint)
        self.button_0_12.bind(on_release=self.toolbox2_logic.change_fretboard)
        self.button_12_24 = custom_button.EloButton(text="Fretboard 12-24",
                                                    size_hint=(button_width_per, button_height_per),
                                                    pos_hint=self.pos_hint)
        self.button_12_24.bind(on_release=self.toolbox2_logic.change_fretboard)
        self.holding_notes = ["", "", "", "", "", ""]
        self.holding_instructions = ["", "", "", "", "", ""]
        self.add_widget(self.trial_button)
        self.add_widget(self.button_confirm_section)
        self.add_widget(self.button_remove_last_chord)
        self.add_widget(self.button_0_12)
        self.add_widget(self.button_12_24)
