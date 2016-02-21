from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
# This handles file browsing on the section selection/create pdf final screen


class BoxLayoutFileBrowser(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(BoxLayoutFileBrowser, self).__init__(**kwargs)
        self.manager = manager
        self.orientation = "horizontal"
        self.browser = FileChooserIconViewSaveLocation(size_hint=(.5, 1))
        self.browser_label = Label(text="Choose a location to save your PDF", size_hint=(.5, .20), pos_hint={"y": .315})
        self.add_widget(self.browser_label)
        self.add_widget(self.browser)
# Gathers path to chosen directory

    def get_path(self, btn):
        self.manager.second_screen_content.file_path = self.browser.path
        self.manager.switch_to(self.manager.first_screen)

# Initializes where the filebrowser views first. ie


class FileChooserIconViewSaveLocation(FileChooserListView):
    def __init__(self, **kwargs):
        super(FileChooserIconViewSaveLocation, self).__init__(**kwargs)
        self.path = "/"
