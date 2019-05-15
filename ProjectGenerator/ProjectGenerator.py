"""
Class ProjectGenerator
Project Generator
Universidad del Valle de Guatemala
Saul Contreras
Michele Benvenuto
Jennifer
"""
from Database import Database
from Models import *
class ProjectGenerator(object):

	user = ""

	def __init__(self):
		self.db = Database("bolt://localhost:7687", "Default","password")					#Set Conection to Database
		self.db.setDefault()		

	def encriptPassword(self,password):														#Encript Password
		newPassword = ""
		for letter in password:
			newPassword = newPassword +  chr(ord(letter) + ord(letter))                     #Ascii code * 2
		return newPassword

	def unencriptPassword(self,password):
		newPassword = ""
		for letter in password:
			newPassword = newPassword +  chr(int(ord(letter)/2))									#Ascii code / 2
		return newPassword		

	def checkUser(self,user,password):
		try:																						#If user doesn´t exist it will show an excpetion
			passwordToCheck = self.db.getNode("User","name",self.encriptPassword(user)).single()[0]["password"]
			if(self.unencriptPassword(passwordToCheck)==password):
				self.user=self.encriptPassword(user)
		except:
			return False
		return(self.unencriptPassword(passwordToCheck)==password)

	def writeUser(self,user,password):
		if(self.db.getNode("User","name",self.encriptPassword(user)).single()==None):
			self.db.write("user","User",{"name":self.encriptPassword(user),"password":self.encriptPassword(password)})
			self.user = user
			return True
		return False

	def showNodes(self):
		return self.db.getAllType("Project")

	def getAllNodes(self):
		toReturn = []
		list1 = self.db.getAllType("Project")
		for node in list1:
			toReturn.append(node[0]["title"])
		list1 = self.db.getAllType("Course")
		for node in list1:
			toReturn.append(node[0]["title"])
		list1 = self.db.getAllType("Resource")
		for node in list1:
			toReturn.append(node[0]["title"])
		return toReturn

	def getRecomendations(self,user):
		recomendations = []
		firstNodes = self.db.getNodesByLink("User","name",user,"HAS_VIEWED")
		for node in firstNodes:
			nodeResources = self.db.getNodesByLink("Project","title",node[0]["title"],"USE_A")         #Get resources of the project
			resources = []
			for resource in nodeResources:
				resources.append(Resource(resource[0]["title"],resource[0]["specifications"]))
			topicOfProject = self.db.getNodesByLink("Project","title",node[0]["title"],"PROJECT_FOR")	 #Get topic of the project
			topic = []
			for top in topicOfProject:
				topic.append(Topic(top[0]["title"],resource[0]["Departament"]))
			currentProject = Project(node[0]["title"],node[0]["description"],"id",resources,topic)       #Instantiate a Project with the DATA
			ADDNODE = True  #This variable will help us two take add the node, if it is false is pecause it is already in recomendations
			for allRecomendation in recomendations:
				if(allRecomendation.compare(currentProject)): #If the project is already recommended
					ADDNODE = False
					allRecomendation.value = allRecomendation.value + 25          #Relation project - 10
			if(ADDNODE):                                     #If the project is not already recommended
				relation = Relation(currentProject,25)		 #The relation will be Project - 10
				recomendations.append(relation)
		for recomedation in recomendations:                                                             #For each project that the user has viewed we will get some other projects based on resources
			ProjectsBasedOnTopic = self.db.getNodesByOther("Project","title",recomedation.project.title,"PROJECT_FOR")
			for node in ProjectsBasedOnTopic:
				nodeResources = self.db.getNodesByLink("Project","title",node[0]["title"],"USE_A")         #Get resources of the project
				resources = []
				for resource in nodeResources:
					resources.append(Resource(resource[0]["title"],resource[0]["specifications"]))
				topicOfProject = self.db.getNodesByLink("Project","title",node[0]["title"],"PROJECT_FOR")	 #Get topic of the project
				topic = []
				for top in topicOfProject:
					topic.append(Topic(top[0]["title"],resource[0]["Departament"]))
				currentProject = Project(node[0]["title"],node[0]["description"],"id",resources,topic)       #Instantiate a Project with the DATA
				ADDNODE = True  #This variable will help us two take add the node, if it is false is pecause it is already in recomendations
				for allRecomendation in recomendations:
					if(allRecomendation.compare(currentProject)): #If the project is already recommended
						ADDNODE = False
						allRecomendation.value = allRecomendation.value + 10          #Relation project - 10
				if(ADDNODE):                                     #If the project is not already recommended
					relation = Relation(currentProject,10)		 #The relation will be Project - 10
					recomendations.append(relation)
		for recomedation in recomendations:                                                             #For each project that the user has viewed we will get some other projects based on resources
			ProjectsBasedOnResource = self.db.getNodesByOther("Project","title",recomedation.project.title,"USE_A")
			for node in ProjectsBasedOnResource:
				nodeResources = self.db.getNodesByLink("Project","title",node[0]["title"],"USE_A")         #Get resources of the project
				resources = []
				for resource in nodeResources:
					resources.append(Resource(resource[0]["title"],resource[0]["specifications"]))
				topicOfProject = self.db.getNodesByLink("Project","title",node[0]["title"],"PROJECT_FOR")	 #Get topic of the project
				topic = []
				for top in topicOfProject:
					topic.append(Topic(top[0]["title"],resource[0]["Departament"]))
				currentProject = Project(node[0]["title"],node[0]["description"],"id",resources,topic)       #Instantiate a Project with the DATA
				ADDNODE = True  #This variable will help us two take add the node, if it is false is pecause it is already in recomendations
				for allRecomendation in recomendations:
					if(allRecomendation.compare(currentProject)): #If the project is already recommended
						ADDNODE = False
						allRecomendation.value = allRecomendation.value + 5          #Relation project - 5
				if(ADDNODE):                                     #If the project is not already recommended
					relation = Relation(currentProject,5)		 #The relation will be Project - 5
					recomendations.append(relation)	
		recomendations = self.sort(recomendations)
		toReturn = []
		for recomedation in recomendations:                                                             #For each project that the user has viewed we will get some other projects based on resources
			toReturn.append(recomedation.project.title)
		return toReturn

	def getProject(self,key,value):
		return self.db.getNode("Project",key,value)

	def sort(self,recomendationsList):
		recomendations=recomendationsList
		toReturn = []
		while(len(recomendations)!=0):
			highter = recomendations[0]
			for node in recomendations:
				if(node.value>highter.value):
					highter = node
			recomendations.remove(highter)
			toReturn.append(highter)
		return toReturn


