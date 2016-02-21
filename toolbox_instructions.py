from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

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