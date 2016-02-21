from kivy.uix.boxlayout import BoxLayout
import toggle_button_custom

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
            temp1 = toggle_button_custom.ToggleButtonFretBoard(text=str(self.i), group="e", tool_state=preview_array,
                                                               preview_labels=preview_access, size_hint_x=.07629,
                                                               pos_hint=self.pos_hint)
            temp1.bind(on_press=temp1.change_instruction)
            temp2 = toggle_button_custom.ToggleButtonFretBoard(text=str(self.i), group="B", tool_state=preview_array,
                                                               preview_labels=preview_access, size_hint_x=.07629,
                                                               pos_hint=self.pos_hint)
            temp2.bind(on_press=temp2.change_instruction)
            temp3 = toggle_button_custom.ToggleButtonFretBoard(text=str(self.i), group="G", tool_state=preview_array,
                                                               preview_labels=preview_access, size_hint_x=.07629,
                                                               pos_hint=self.pos_hint)
            temp3.bind(on_press=temp3.change_instruction)
            temp4 = toggle_button_custom.ToggleButtonFretBoard(text=str(self.i), group="D", tool_state=preview_array,
                                                               preview_labels=preview_access, size_hint_x=.07629,
                                                               pos_hint=self.pos_hint)
            temp4.bind(on_press=temp4.change_instruction)
            temp5 = toggle_button_custom. ToggleButtonFretBoard(text=str(self.i), group="A", tool_state=preview_array,
                                                                preview_labels=preview_access, size_hint_x=.07629,
                                                                pos_hint=self.pos_hint)
            temp5.bind(on_press=temp5.change_instruction)
            temp6 = toggle_button_custom.ToggleButtonFretBoard(text=str(self.i), group="E", tool_state=preview_array,
                                                               preview_labels=preview_access, size_hint_x=.07629,
                                                               pos_hint=self.pos_hint)
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
