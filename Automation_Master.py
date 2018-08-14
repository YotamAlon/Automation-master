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

    def __init__(self, name, default=None):
        super(StringInput, self).__init__()
        self.input_name = name
        self.default = 'None' if default is None else default
        if default is not None:
            self.input_value = default


from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import StringProperty, ObjectProperty, ListProperty
class ScriptPage(TabbedPanelItem):
    script_name = StringProperty()
    script_path = StringProperty()
    main = ObjectProperty()
    status = StringProperty()
    output = ListProperty()

    def __init__(self, script_name, script_path):
        super(ScriptPage, self).__init__()
        self.script_name = script_name
        self.script_path = script_path
        self.params = self.parse_script_inputs()

        for param in self.params:
            self.add_widget(StringInput(param.name, param.default if param.default != param.empty else None))

    def parse_script_inputs(self):
        from importlib.util import spec_from_file_location, module_from_spec
        try:
            import os
            spec = spec_from_file_location('main', os.path.join(self.script_path, self.script_name))
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            self.main = getattr(module, 'main')
        except ImportError as e:
            print(e)
            self.status = 'ERROR!'
            return []
        self.status = 'Script Loaded'

        from inspect import signature
        return signature(self.main).parameters.values()

    def run_script(self):
        from CaptureStdout import CaptureStdout
        with CaptureStdout() as output:
            self.main(*[child.input_value for child in self.children])
        self.output = output


from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
class LoadDialog(FloatLayout):
    dismiss = ObjectProperty()


from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import ObjectProperty
class ManageScripts(TabbedPanelItem):
    loadfile = ObjectProperty()
    savefile = ObjectProperty()
    text_input = ObjectProperty()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(dismiss=self.dismiss_popup)
        from kivy.uix.popup import Popup
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty, ObjectProperty
class MainWindow(TabbedPanel):
    db = ObjectProperty()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_db()
        self.add_widget(ManageScripts())
        print(list(self.db.scripts.find()))
        for script in self.db.scripts.find():
            self.add_script(script_path=script['path'], script_names=[script['name']])

    def add_script(self, script_path, script_names, action=None):
        for script_name in script_names:
            self.add_widget(ScriptPage(script_name=script_name.split('/')[-1], script_path=script_path))
            if not self.db.scripts.find_one({'name': script_name.split('/')[-1], 'path': script_path}):
                self.db.scripts.insert_one({'name': script_name.split('/')[-1], 'path': script_path})
        if action is not None:
            action()

    def load_db(self):
        from pymongo import MongoClient
        client = MongoClient()
        self.db = client.AM


from kivy.app import App
from kivy.properties import ObjectProperty
class AutomationApp(App):
    window = ObjectProperty()

    def build(self):
        self.window = MainWindow()
        return self.window


if __name__ == "__main__":
    AutomationApp().run()
