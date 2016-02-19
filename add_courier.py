from kivy.core.text import LabelBase
import sys
import os
# from kivy.core.tex

#You added this, remove it if it doesn't work

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

LabelBase.register(name="courier new",
                   fn_regular=resource_path(os.path.join('', 'Courier New.ttf')))
LabelBase.DEFAULT = "courier new"
# C:/Users/Jonathan/PycharmProjects/EloTab/