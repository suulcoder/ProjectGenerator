"""
The classes that model a node in our database
Project Generator
Universidad del Valle de Guatemala
Saul Contreras
Michele Benvenuto
Jennifer
"""


#---------------------------------------------------------------------------------------------------
class Project(object):
    """Project has tittle and description"""
    def __init__(self, title,description,_id):
        self._id = _id + ":Project"
        self.title = title
        self.description = description

#---------------------------------------------------------------------------------------------------
class Resource(object):
    """Resource has title and specification"""
    def __init__(self, title,specification,_id):
        self._id = _id + ":Resource"
        self.title =title
        self.specification = specification
        
#---------------------------------------------------------------------------------------------------
class User(object):
    """User has name and password"""
    def __init__(self, name,password,_id):
        self._id = _id+":User"
        self.name = name
        self.password = password
        
#---------------------------------------------------------------------------------------------------
class Topic(object):
    """Topic has departament and id"""
    def __init__(self, title,departament,_id):
        self._id = _id
        self.title = title
        self.departament = departament

#---------------------------------------------------------------------------------------------------
