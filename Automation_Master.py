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


from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
class StringInput(TextInput):
    input_name = StringProperty()
    input_value = StringProperty()
    default = StringProperty()

    def __init__(self, name, default):
        super(StringInput, self).__init__()
        self.input_name = name
        self.default = default


from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import StringProperty, ObjectProperty, ListProperty
class ScriptPage(TabbedPanelItem):
    script_name = StringProperty()
    main = ObjectProperty()
    status = StringProperty()
    output = ListProperty()

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
            module = import_module(self.script_name.split('.')[0])
            self.main = getattr(module, 'main')
        except ImportError as e:
            print(e)
            self.status = 'ERROR!'
            return []
        self.status = 'Script Loaded'

        from inspect import signature
        return signature(self.main).parameters

    def run_script(self):
        from CaptureStdout import CaptureStdout
        with CaptureStdout() as output:
            self.main(*[child.input_value for child in self.children])
        self.output = output


from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import ObjectProperty
class ManageScripts(TabbedPanelItem):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        from kivy.uix.popup import Popup
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        import os
        self.parent.add_script(os.path.join(path, filename[0]))

        self.dismiss_popup()


from kivy.uix.tabbedpanel import TabbedPanel
class MainWindow(TabbedPanel):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.add_widget(ManageScripts())

    def add_script(self, script_name):
        self.add_widget(ScriptPage(script=script_name))


from kivy.app import App
class AutomationApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    AutomationApp().run()
