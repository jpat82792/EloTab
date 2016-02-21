import song_section


class ToolBox2Logic:
    def __init__(self, manager, toolbox):
        self.manager = manager
        self.toolbox = toolbox

    def change_fretboard(self, btn):
        x = 0
        # Stores selected instructions
        for string in self.manager.first_screen_content.fretboard.neck:
            for note in string:
                if note.state == "down":
                    control = self.manager.first_screen_content.preview.label_array[x].operation
                    # This stores instruction in the event
                    if control != "No Instruction":
                        self.toolbox.holding_instructions[x] = self.manager.first_screen_content.translate_instruction(
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
                            self.toolbox.holding_notes[x] = self.toolbox.holding_notes[x] + str(i) + "-"
                        else:
                            self.toolbox.holding_notes[x] = self.toolbox.holding_notes[x] + str(i) + "-"
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
                            self.toolbox.holding_notes[x] = self.toolbox.holding_notes[x] + str(i) + "-"
                        else:
                            self.toolbox.holding_notes[x] = self.toolbox.holding_notes[x] + str(i) + "-"
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
            difference = self.toolbox.previous[-1]
            self.toolbox.previous.pop()
            for label in self.manager.first_screen_content.preview.label_array:
                temp = label.child_label.text[:difference]
                label.child_label.text = temp
        except IndexError:
            pass
# Leads back to section naming screen

    def confirm_section(self, btn):
        created_song_section = song_section.SongSection(name=self.manager.first_screen_content.section_name)
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
