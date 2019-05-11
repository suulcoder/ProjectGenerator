"""
Projecto Neo4j
Project Generator
"""
from neo4j import GraphDatabase, basic_auth


#---------------------------------------------------------------------------------------------------
class Database(object):
    """Set database driver"""
    def __init__(self, uri,user,password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))        

    """Close database"""
    def close(self):
        self._driver.close()

    """
    This method is used to write a node in database and receives 3 arguments:
    _id: is the identifier that you want to be saved on database, should be an string without spaces
    nodeType: Is the type of node that you want, it must be a String, its first letter must be Uppercase
    arguments: It containds the atributes of the node. It must be a dictionary where the key is the name of the atribute and the value must be the value of the atribute"""
    def write(self,_id,nodeType,arguments):
        result = ""
        argumentsList = []
        if(nodeType!=None):
            result = result + "CREATE (" + _id + ":" + nodeType + ")\n"
            counter = 0
            for variable in arguments:
                argumentsList.append(arguments[variable])
                result = result + "SET " +  _id + "." + variable + " = $arguments[" + str(counter)  + "]\n"
                counter = counter+1
        with self._driver.session() as session:
            session.write_transaction(self._create,argumentsList,result)

    """
    This method is used to make a conection between two nodes and receives 7 parameters:
    type1 and type2: Type of node 1 and 2 and must be an string, its first letter must be Uppercase      
    VariableName1 and VariableName2: It has the name of the key to be checked of the nodes. It must be a string withoud spaces
    variable1  and variable2: contains the value of the Variables setted above, must be a string
    linkName: it has the name that will have the link. Must be an string without spaces.""" 
    def link(self,type1,type2,variableName1,variable1,VariableName2,variable2,linkName):
        result = "MATCH (a:" + type1 + "),(b:" + type2 + ")\nWHERE a." + variableName1 + "= $variable1 AND b."+ VariableName2 + "= $variable2\nCREATE (a)-[:"+linkName+"]->(b)"
        with self._driver.session() as session: 
            session.write_transaction(self._connect,result,variable1,variable2)
    
    """
    This method is for delete an specific node it has 3 parameters
    nodeType: it receives the type of node you want to delete, must be an string and its first letter must be uppercase
    key: it receives a key or a reference that the node has. 
    value: it recives de value of the reference key."""
    def delete(self,nodeType,key,value):
        result = "MATCH (a:" + nodeType + ")\nWHERE a." + key + "= $value\nDETACH DELETE (a)"
        with self._driver.session() as session: 
            session.write_transaction(self._delete,result,value)

    """
    This method is for delete a relationship between nodes it has 7 parameters
    type1 and type2: Type of node 1 and 2 and must be an string, its first letter must be Uppercase      
    VariableName1 and VariableName2: It has the name of the key to be checked of the nodes. It must be a string withoud spaces
    variable1  and variable2: contains the value of the Variables setted above, must be a string
    linkName: it has the name that will be deleted. Must be an string without spaces.""" 
    def deleteLink(self,type1,type2,variableName1,variable1,VariableName2,variable2,linkName):
        result = "MATCH (a:" + type1 + "),(b:" + type2 + ")\nWHERE a." + variableName1 + "= $variable1 AND b."+ VariableName2 + "= $variable2\nMATCH (a)-[r:"+linkName+"]->(b)\nDELETE r"
        with self._driver.session() as session: 
            session.write_transaction(self._deleteLink,result,variable1,variable2)

    """
    This method is for upgrade an specific atribute on a node it has 3 parameters
    nodeType: it receives the type of node you want to upgrade, must be an string and its first letter must be uppercase
    key: it receives a key or a reference that the node has. 
    value: it recives de value of the reference key.
    newValue: it recieves de value that will be setted"""
    def upgrade(self,nodeType,key,value,newValue):
        result = "MATCH (a:" + nodeType + ")\nWHERE a." + key + "= $value\nSET a." + key + "= $newValue"
        with self._driver.session() as session: 
            session.write_transaction(self._upgrade,result,value,newValue)

    """
    This method is used to get a node it has three parameters
    nodeType: it receives the type of node where you want to get information, must be an string and its first letter must be uppercase
    key: it receives a key or a reference that the node has. 
    value: it recives de value of the reference key.
    It will return a StatementResult type, that behaives like a java-map, you have to make an iterator to get informations"""
    def getNode(self,nodeType,key,value):
        result = "MATCH (a:" + nodeType + ")\nWHERE a." + key + "=$value\nRETURN a"
        with self._driver.session() as session: 
            return session.write_transaction(self._getNode,result,value)        

    @staticmethod
    def _getNode(tx,result,value):
        return tx.run(result,value=value)

    @staticmethod
    def _upgrade(tx,result,value,newValue):
        result = tx.run(result,value=value,newValue=newValue)

    @staticmethod
    def _deleteLink(tx,result,variable1,variable2):
        result = tx.run(result,variable1=variable1,variable2=variable2) 

    @staticmethod
    def _delete(tx,result,value):
        result = tx.run(result,value=value)            

    @staticmethod
    def _connect(tx,result,variable1,variable2):
        result = tx.run(result,variable1=variable1,variable2=variable2) 

    """This method is used by write"""
    @staticmethod
    def _create(tx,arguments,result):
        result = tx.run(result,arguments=arguments)
        
#---------------------------------------------------------------------------------------------------
class Project(object):
    """docstring for Proje"""
    def __init__(self, title,description,_id):
        self._id = _id + ":Project"
        self.title = title
        self.description = description

#---------------------------------------------------------------------------------------------------
class Resource(object):
    """docstring for Resource"""
    def __init__(self, title,specification,_id):
        self._id = _id + ":Resource"
        self.title =title
        self.specification = specification
        
#---------------------------------------------------------------------------------------------------
class User(object):
    """docstring for User"""
    def __init__(self, name,password,_id):
        self._id = _id+":User"
        self.name = name
        self.password = password
        
#---------------------------------------------------------------------------------------------------
class Topic(object):
    """docstring for Tema"""
    def __init__(self, title,departament,_id):
        self._id = _id
        self.title = title
        self.departament = departament

#---------------------------------------------------------------------------------------------------
project = Project("second","Confidencial","proyecto")
db = Database("bolt://localhost:7687", "SuulCoder","password")
#db.write("second","Resource",{"title":"dfa","description":project.description})
#db.write("id","Project",{"title":project.title,"description":project.description})
#db.link("Project","Resource","title",project.title,"title","dfa","do_with")
#db.deleteLink("Project","Resource","title",project.title,"title","dfa","do_with")
#db.delete("Resource","title","dfa")
#db.upgrade("Resource","title","dfa","prueba")
print(db.getNode("Project","title",project.title).single())
db.close()