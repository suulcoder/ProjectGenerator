"""
Class ProjectGenerator
Project Generator
Universidad del Valle de Guatemala
Saul Contreras
Michele Benvenuto
Jennifer
"""
from Database import Database
class ProjectGenerator(object):

	def __init__(self):
		self.db = Database("bolt://localhost:7687", "Default","password")					#Set Conection to Database
		self.db.setDefault()																		#Set default Database			

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
			passwordToCheck = self.db.getNode("User","name",user).single()[0]["password"]
		except:
			return False
		return(self.unencriptPassword(passwordToCheck)==password)

	def writeUser(self,user,password):
		if(self.db.getNode("User","name",user).single()==None):
			self.db.write("user","User",{"name":user,"password":self.encriptPassword(password)})
			print("writen")
			return True
		return False


