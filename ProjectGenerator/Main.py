from kivy.app import App
from kivy.uix.widget import Widget
from Models import *
from ProjectGenerator import ProjectGenerator
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.boxlayout import BoxLayout
from kivy.adapters.dictadapter import ListAdapter
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

#------------------------------------------------------------------------------------------------------------------------------
class Start(Screen):

	def login(self):#When user press login
		project = ProjectGenerator()
		if(project.checkUser(self.ids.user.text,self.ids.password.text)):
			app = App.get_running_app()
			self.manager.transition = SlideTransition(direction="left")
			self.manager.current = 'connected'
			app.config.read(app.get_application_config())
			app.config.write()
		else:
			self.ids.defensive.text = "User or password is incorrect"

	def Sign(self):#When user press Sign up
		project = ProjectGenerator()
		if(self.ids.user.text!="" and self.ids.user.text!=""):
			if(project.writeUser(self.ids.user.text,self.ids.password.text)):
				self.manager.transition = SlideTransition(direction="right")
				self.manager.current = 'connected'
			else:
				self.ids.defensive.text = "This user is already registered"
		else:
			self.ids.defensive.text = "Data is empty"
	pass

#------------------------------------------------------------------------------------------------------------------------------
class Connected(Screen):
	def show(self):
		project = ProjectGenerator()
		result = project.showNodes()
		result = result.values()#Convert to a list
		projects = []
		for node in result:#Print nodes in the result
			print(node[0]["title"])
			projects.append(node[0]["title"]) #The name of the atribute is setted in the second []	
		adapter = ListAdapter(data=projects,cls=ListItemButton)
		self.ids.project_list.adapter = adapter

	def recomend(self):
		pass

	def add(self):
		pass

	pass

#------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------
class ProjectListButton(ListItemButton):
	pass

#------------------------------------------------------------------------------------------------------------------------------
class Project_GeneratorApp(App):
	title = "Project Generator"
	def build(self):
		manager = ScreenManager()
		manager.add_widget(Start(name='login'))
		manager.add_widget(Connected(name='connected'))
		return manager

#------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	Project_GeneratorApp().run()
	#db.setDefault()																	#Set default Database
	#DonebyUser = db.getNodesByOther("Project","title","Avengers","USE_A")
	#result = result.values()#Convert to a list
	#for node in result:#Print nodes in the result
	#	print(node[0]["title"]) #The name of the atribute is setted in the second []
	#db.close()
	#project = Project("second","Confidencial","proyecto")
	#db.write("second","Resource",{"title":"dfa","description":project.description})
	#db.write("id","Project",{"title":project.title,"description":project.description})
	#db.link("Project","Resource","title",project.title,"title","dfa","do_with")
	#db.deleteLink("Project","Resource","title",project.title,"title","dfa","do_with")
	#db.delete("Resource","title","dfa")
	#db.upgrade("Resource","title","dfa","prueba")
	#print(db.getNode("Project","titl",project.title).single())