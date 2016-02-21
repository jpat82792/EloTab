from kivy.uix.togglebutton import ToggleButton
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
