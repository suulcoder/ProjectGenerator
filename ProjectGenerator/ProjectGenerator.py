from Database import Database
from Models import *

project = Project("second","Confidencial","proyecto")
db = Database("bolt://localhost:7687", "Default","password")
#db.write("second","Resource",{"title":"dfa","description":project.description})
#db.write("id","Project",{"title":project.title,"description":project.description})
#db.link("Project","Resource","title",project.title,"title","dfa","do_with")
#db.deleteLink("Project","Resource","title",project.title,"title","dfa","do_with")
#db.delete("Resource","title","dfa")
#db.upgrade("Resource","title","dfa","prueba")
#print(db.getNode("Project","titl",project.title).single())
db.setDefault()
result = db.getNodesByOther("Project","title","Avengers","USE_A")
result = result.values()#Convert to a list
for node in result:#Print nodes in the result
	print(node[0]["title"]) #The name of the atribute is setted in the second []
db.close()