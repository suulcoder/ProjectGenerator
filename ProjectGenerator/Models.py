"""
The classes that model a node in our database
And the model relation that will be useful to get the algorithm
Project Generator
Universidad del Valle de Guatemala
Saul Contreras
Michele Benvenuto
Jennifer
"""

#---------------------------------------------------------------------------------------------------
class Project(object):
    """Project has tittle and description"""
    def __init__(self, title,description,_id,resource,topic):
        self._id = _id + ":Project"
        self.title = title
        self.description = description
        self.resource = resource
        self.topic = topic

#---------------------------------------------------------------------------------------------------
class Resource(object):
    """Resource has title and specification"""
    def __init__(self, title,specification):
        self.title =title
        self.specification = specification
        
#---------------------------------------------------------------------------------------------------
class Topic(object):
    """Topic has departament and title"""
    def __init__(self, title,departament):
        self.title = title
        self.departament = departament

#---------------------------------------------------------------------------------------------------
class Relation(object):
    """This will be useful for give the recomendation"""
    def __init__(self, project,value):
        self.project = project
        self.value = value
        
    def compare(self,project):
        return(project.title==self.project.title)