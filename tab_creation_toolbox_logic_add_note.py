class ToolBox2LogicAddNote:
    def __init__(self, manager, toolbox):
        self.manager = manager
        self.toolbox = toolbox

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
                        if control != "No Instruction":
                            self.toolbox.holding_instructions[x] = self.translate_instruction(
                                self.manager.first_screen_content.preview.label_array[x].operation)
                        else:
                            self.toolbox.holding_instructions[x] = ""
                x += 1
            # This sees which instruction is the longest
            for i in range(0, 6):
                if len(self.toolbox.holding_instructions[i]) > longest_string2:
                    longest_string2 = len(self.toolbox.holding_instructions[i])

            # 2nd loop
            for i in range(0, 6):
                if longest_string2 > len(self.toolbox.holding_instructions[i]):
                    difference = longest_string2 - len(self.toolbox.holding_instructions[i])
                    self.toolbox.holding_instructions[i] += (difference * "-")
            # 3rd loop
            x = 0
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 0
                for note in string:
                    if note.state == "down":
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.\
                                                                 label_array[x].child_label.text
                        if i >= 10:
                            self.toolbox.holding_notes[x] = str(i) + "-"
                        else:
                            self.toolbox.holding_notes[x] = str(i) + "-"
                        note.state = "normal"
                    i += 1
                x += 1
            longest_string = 0
            # 4th loop
            fourth_loop = 0
            for i in range(0, 6):
                if len(self.toolbox.holding_notes[i]) > longest_string:
                    longest_string = len(self.toolbox.holding_notes[i])
                fourth_loop += 1

            # 5th loop
            fifth_loop = 0
            for i in range(0, 6):
                difference = longest_string - len(self.toolbox.holding_notes[i])
                self.toolbox.holding_notes[i] += (difference * "-")
                fifth_loop += 1
            x = 0
            self.toolbox.previous.append(len(self.manager.first_screen_content.preview.label_array[0].child_label.text))
            for label in self.manager.first_screen_content.preview.label_array:
                label.child_label.text = label.child_label.text + self.toolbox.holding_instructions[x] + \
                                         self.toolbox.holding_notes[x]
                x += 1

            self.toolbox.holding_notes = ["", "", "", "", "", ""]
            self.toolbox.holding_instructions = ["", "", "", "", "", ""]

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
                            self.toolbox.holding_instructions[x] = self.translate_instruction(
                                self.manager.first_screen_content.preview.label_array[x].operation)
                        else:
                            self.toolbox.holding_instructions[x] = ""
                x += 1

                # This sees which instruction is the longest
            for i in range(0, 6):
                if len(self.toolbox.holding_instructions[i]) > longest_string2:
                    longest_string2 = len(self.toolbox.holding_instructions[i])

            # 2nd loop

            for i in range(0, 6):
                if longest_string2 > len(self.toolbox.holding_instructions[i]):
                    difference = longest_string2 - len(self.toolbox.holding_instructions[i])
                    self.toolbox.holding_instructions[i] += (difference * "-")

            # 3rd loop
            x = 0
            for string in self.manager.first_screen_content.fretboard.neck:
                i = 12
                for note in string:
                    if note.state == "down":
                        self.manager.first_screen_content.hold = self.manager.first_screen_content.preview.label_array[x].child_label.text
                        if i >= 10:
                            self.toolbox.holding_notes[x] = str(i) + "-"
                        else:
                            self.toolbox.holding_notes[x] = str(i) + "-"
                        note.state = "normal"
                    i += 1
                x += 1
            longest_string = 0

            # 4th loop
            for i in range(0, 6):
                if len(self.toolbox.holding_notes[i]) > longest_string:
                    longest_string = len(self.toolbox.holding_notes[i])

            # 5th loop
            for i in range(0, 6):
                difference = longest_string - len(self.toolbox.holding_notes[i])
                self.toolbox.holding_notes[i] += (difference * "-")

            self.toolbox.previous.append(len(self.manager.first_screen_content.preview.label_array[0].child_label.text))
            x = 0
            for label in self.manager.first_screen_content.preview.label_array:
                label.child_label.text = label.child_label.text + self.toolbox.holding_instructions[x] + self.toolbox.holding_notes[x]
                x += 1

            self.toolbox.holding_notes = ["", "", "", "", "", ""]
            self.toolbox.holding_instructions = ["", "", "", "", "", ""]
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