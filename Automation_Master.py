#Kivy imports
import kivy
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextImport
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

#python imports
import os
import sys

def FileInput(BoxLayout):
	input_name = StringProperty()
	input_help = StringProperty()
	input_file = ObjectProperty()
	
	def __init__(self, **kwargs):
		super(FileInput, self).__init__(**kwargs)
		self.input_name = name
		self.input_help = help
	
	def open_popup():
		chooser = FileChooserIconView(multiselect=False)
		popup = Popup(title='Choose File', content=chooser)
		chooser.bind(on_submit=FileInput.save_file(chooser, popup.dismiss))
		popup.open()

	def save_file(chooser, dismiss_func):
		self.input_file = chooser.selection[0]
		dismiss_func()
		
def StringInput(BoxLayout):
	input_name = StringProperty()
	input_value = StringProperty()
	input_help = StringProperty()
	
	def __init__(self, **kwargs):
		super(StringInput, self).__init__(**kwargs)
		self.input_name = name
		self.input_help = help
		
	def get_input():
		return [input_name, input_value]

def ScriptPage(TabbedPanelItem):
	script_name = StringProperty()
	
	def __init__(self, **kwargs):
		super(ScriptPage, self).__init__(**kwargs)
		self.script_name = script
		for script_input in get_script_inputs(): #inputs should look like: "inputs = [['string', 'name', 'enter your name'], ['file', 'source file', 'select your source file']]"
			if script_input[0] == 'string':
				self.ids.mainview.add_widget(StringInput(name=script_input[1], help=script_input[2]))
			elif script_input[0] == 'file':
				self.ids.mainview.add_widget(FileInput(name=script_input[1], help=script_input[2]))
			else:
				sys.exit("Bad script inputs at " + self.script_name)
		
	def get_script_inputs():
		script = open(script_name, 'r')
		for line in list(script):
			if line[:7] = "inputs":
				return eval(line.split('=')[1])
		
		
		
		

def MainWindow(TabbedPanel):
	def __init__(self, **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		for curfile in os.listdir(os.getcwd())
			if curfile.endswith(".py"):
				self.add_widget(ScriptPage(script=curfile))
	

def AutomationApp(App):
	def build:
		return MainWindow()
