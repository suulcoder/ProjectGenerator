from kivy.app import App
from kivy.uix.widget import Widget
from Models import *
from ProjectGenerator import ProjectGenerator
from kivy.uix.textinput import TextInput

#------------------------------------------------------------------------------------------------------------------------------
class Start(Widget):
	def login(self):#When user press login
		project = ProjectGenerator()
		if(project.checkUser(self.ids.user.text,self.ids.password.text)):
			return Projects()

	def Sign(self):#When user press Sign in
		project = ProjectGenerator()
		if(project.writeUser(self.ids.user.text,self.ids.password.text)):
			return Projects()
	pass

#------------------------------------------------------------------------------------------------------------------------------
class Project_GeneratorApp(App):
	title = "Project Generator"
	def build(self):
		return Start()

#------------------------------------------------------------------------------------------------------------------------------
class Projects(Widget):
	pass

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