from kivy.uix.button import Button

# Default "Elothought" styled button, referred to as EloButton


class EloButton(Button):
    def __init__(self, **kwargs):
        super(EloButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_color = [.019607, .2705, .29019, 1]
        self.background_down = ""
