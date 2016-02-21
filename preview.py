from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class LabelPreview(ScrollView):
    def __init__(self, child_text, child_halign, child_pos_hint, **kwargs):
        super(LabelPreview, self).__init__(**kwargs)
        self.operation = "No Operation"
        self.text = StringProperty("")
        self.child_label = Label(text=child_text, halign=child_halign, pos_hint=child_pos_hint)
        self.add_widget(self.child_label)


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