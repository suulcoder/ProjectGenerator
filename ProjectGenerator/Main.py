"""
Project Generator
Universidad del Valle de Guatemala
Saul Contreras
Michele Benvenuto
Jennifer
"""
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

	def on_text(self, instance, value):
		project = ProjectGenerator()
		self.root.suggestion_text = ''
		word_list = project.getAllNodes()
		val = value[value.rfind(' ') + 1:]
		if not val:
		    return
		try:
			word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
			if not word:
				return
			self.root.suggestion_text = word
		except IndexError:
			print("IndexError")

	def login(self):#When user press login
		project = ProjectGenerator()
		if(project.checkUser(self.ids.user.text,self.ids.password.text)):
			app = App.get_running_app()
			self.manager.transition = SlideTransition(direction="left")
			self.manager.current = 'connected'
			Connected.user = self.ids.user.text
			app.config.read(app.get_application_config())
			app.config.write()
		else:
			self.ids.defensive.text = "User or password is incorrect"

	def Sign(self):#When user press Sign up
		project = ProjectGenerator()
		if(self.ids.user.text!="" and self.ids.user.text!=""):
			if(project.writeUser(self.ids.user.text,self.ids.password.text)):
				app = App.get_running_app()
				self.manager.transition = SlideTransition(direction="right")
				self.manager.current = 'connected'
				Connected.user = self.ids.user.text
				app.config.read(app.get_application_config())
				app.config.write()
			else:
				self.ids.defensive.text = "This user is already registered"
		else:
			self.ids.defensive.text = "Data is empty"
	pass

#------------------------------------------------------------------------------------------------------------------------------
class Connected(Screen):
	
	user = ""
	project = ProjectGenerator()
	result = project.showNodes()
	result = result.values()#Convert to a list
	projects = []
	for node in result:#Print nodes in the result
		projects.append(node[0]["title"]) #The name of the atribute is setted in the second []	
	adapter = ListAdapter(data=projects,cls=ListItemButton)

	def showAll(self):
		project = ProjectGenerator()
		result = project.showNodes()
		result = result.values()#Convert to a list
		projects = []
		for node in result:#Print nodes in the result
			projects.append(node[0]["title"]) #The name of the atribute is setted in the second []	
		self.ids.project_list.adapter = ListAdapter(data=projects,cls=ListItemButton)

	def select(self):
		try:
			self.ids.name.text = self.ids.project_list.adapter.selection[0].text
			project = ProjectGenerator()
			result = project.getProject("title",self.ids.project_list.adapter.selection[0].text)
			result = result.values()#Convert to a list
			for node in result:
				self.ids.description.text =  node[0]["description"]
				self.ids.time.text = "Time in hours: " + str(node[0]["time"])
				self.ids.complexity.text = "Complexity: " + node[0]["complexity"]
				self.ids.integrants.text = "Integrants required: " + str(node[0]["integrants"])
			project.db.link("User","Project","name",project.encriptPassword(self.user),"title",self.ids.project_list.adapter.selection[0].text,"HAS_VIEWED")
		except:
			self.ids.name.text = "PROJECT GENERATOR"
			self.ids.description.text = "SELECT ONE PROJECT"
			self.ids.time.text = ""
			self.ids.complexity.text = ""
			self.ids.integrants.text = ""

	def recomend(self):
		project = ProjectGenerator()
		lista = project.getRecomendations(project.encriptPassword(self.user))
		for node in lista:
			print(node)
		toShow	= []
		for i in range(0,20):
			toShow.append(lista[i])
		self.ids.project_list.adapter = ListAdapter(data=toShow	,cls=ListItemButton) 

	def delete(self):
		project = ProjectGenerator()
		try:
			self.ids.name.text = self.ids.project_list.adapter.selection[0].text
			project.db.delete("Project","title",self.ids.project_list.adapter.selection[0].text)
			self.showAll()
		except:
			self.ids.name.text = "PROJECT GENERATOR"
			self.ids.description.text = "SELECT ONE PROJECT"

	def add(self):
		app = App.get_running_app()
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = 'add'
		app.config.read(app.get_application_config())
		app.config.write()

	def SignOut(self):
		app = App.get_running_app()
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = 'login'
		app.config.read(app.get_application_config())
		app.config.write()
	pass

#------------------------------------------------------------------------------------------------------------------------------
class AddNode(Screen):
	pass

	def save(self):
		try:
			if(self.ids.ProjectName.text!="" and self.ids.CourseName.text!="" and self.ids.ResourceName.text!=""):
				project = ProjectGenerator()
				if(project.db.getNode("Project","title",self.ids.ProjectName.text).single()==None):
					project.db.write("id","Project",{"title":self.ids.ProjectName.text,"description":self.ids.ProjectDescription.text,"integrants":int(self.ids.integrants.text),"time":int(self.ids.time.text),"complexity":self.ids.complexity.text})
					if(project.db.getNode("Resource","title",self.ids.ResourceName.text).single()==None):
						project.db.write("id","Resource",{"title":self.ids.ResourceName.text,"specifications":self.ids.ResourceDescription.text})
					if(project.db.getNode("Course","title",self.ids.CourseName.text).single()==None):
						project.db.write("id","Course",{"title":self.ids.CourseName.text,"Departament":self.ids.CourseDepartament.text})
					project.db.link("Project","Resource","title",self.ids.ProjectName.text,"title",self.ids.ResourceName.text,"USE_A")
					project.db.link("Project","Course","title",self.ids.ProjectName.text,"title",self.ids.CourseName.text,"PROJECT_FOR")
					app = App.get_running_app()
					self.manager.transition = SlideTransition(direction="left")
					self.manager.current = 'connected'
					app.config.read(app.get_application_config())
					app.config.write()
				else:
					self.ids.description.text = "PROJECT ALREADY EXISTS"	
			else:
				self.ids.description.text = "FILL ALL DATA"
		except:
			self.ids.description.text = "INVALID DATA"

	def cancel(self):
		app = App.get_running_app()
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = 'connected'
		app.config.read(app.get_application_config())
		app.config.write()

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
		manager.add_widget(AddNode(name='add'))
		return manager

#------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	Project_GeneratorApp().run()