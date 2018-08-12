# from kivy.uix.filechooser import FileChooserIconView
# from kivy.uix.popup import Popup
# from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import StringProperty, ObjectProperty
# class FileInput(BoxLayout):
#     input_name = StringProperty()
#     input_help = StringProperty()
#     input_file = ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super(FileInput, self).__init__(**kwargs)
#         self.input_name = name
#         self.input_help = help
#
#     def open_popup():
#         chooser = FileChooserIconView(multiselect=False)
#         popup = Popup(title='Choose File', content=chooser)
#         chooser.bind(on_submit=FileInput.save_file(chooser, popup.dismiss))
#         popup.open()
#
#     def save_file(chooser, dismiss_func):
#         self.input_file = chooser.selection[0]
#         dismiss_func()


from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
class StringInput(BoxLayout):
    input_name = StringProperty()
    input_value = StringProperty()
    default = StringProperty()

    def __init__(self, name, default):
        super(StringInput, self).__init__()
        self.input_name = name
        self.default = default


from kivy.uix.tabbedpanel import TabbedPanelItem
class ScriptPage(TabbedPanelItem):
    def __init__(self, script):
        super(ScriptPage, self).__init__()
        self.script_name = script
        self.params = self.parse_script_inputs()

        for param in self.params:
            print(param.annotation)
            self.add_widget(StringInput(param.name, param.default if param.default != param.empty else None))

    def parse_script_inputs(self):
        from importlib import import_module
        try:
            main = import_module('main', '.' + self.script_name)
        except ImportError:
            self.bad = True
            return []

        from inspect import Signature
        return Signature(main).parameters


from kivy.uix.tabbedpanel import TabbedPanel
class MainWindow(TabbedPanel):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        import os
        for curfile in os.listdir(os.getcwd()):
            if curfile.endswith(".py"):
                self.add_widget(ScriptPage(script=curfile))


from kivy.app import App
class AutomationApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    AutomationApp().run()
