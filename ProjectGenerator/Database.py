"""
Class Databae will be util to make conection with Neo4J 
Project Generator
Universidad del Valle de Guatemala
Saul Contreras
Michele Benvenuto
Jennifer
"""

from neo4j import GraphDatabase, basic_auth

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

    """This method is useful to get all nodes that are connected by the same link to a node m connected with the same link to a node of reference
    nodeType: it receives the type of node of reference, must be an string and its first letter must be uppercase
    key: it receives a key or a reference that the node has. 
    value: it recives de value of the reference key.
    link: receives the link name, must be a string without spaces
    """
    def getNodesByOther(self,nodeType,key,value,link):
        result= "MATCH (a:" + nodeType + ")\nWHERE a." + key + "=$value\nMATCH (a)-[:" + link + "]->(m)<-[:" + link + "]-(r)\nRETURN r"
        with self._driver.session() as session: 
            return session.write_transaction(self._getNodes,result,value)

    """This method is useful to get all nodes connect to one of reference with an specific link
    nodeType: it receives the type of node of reference, must be an string and its first letter must be uppercase
    key: it receives a key or a reference that the node has. 
    value: it recives de value of the reference key.
    link: receives the link name, must be a string without spaces"""
    def getNodesByLink(self,nodeType,key,value,link):
        result= "MATCH (a:" + nodeType + ")\nWHERE a." + key + "=$value\nMATCH (a)-[:" + link + "]->(m)\nRETURN m"
        with self._driver.session() as session: 
            return session.write_transaction(self._getNodes,result,value)

    """This method is useful to get all nodes from the same type
    nodeType: receives the String of the node type"""
    def getAllType(self,nodeType):
        result= "MATCH (a:" + nodeType + ")\nRETURN a"
        with self._driver.session() as session: 
            return session.write_transaction(self._Default,result)        

    """This method is used two now if there ara nodes on the database.
    It will return None the database is empty"""
    def getDefault(self):
        result = "MATCH (n) return n"
        with self._driver.session() as session: 
            resultado = session.write_transaction(self._Default,result)        
            return resultado

    """This method is used two set the default database, you should change the string result two change it. The cod must be in Cypher"""
    def setDefault(self):
        if (self.getDefault().single()==None):#We check if the database is empty
            result = """
            CREATE (ProjectGenerator:Project {title: "Project_Generator",description:"This project is about the creation of a software to generate projects. You need to know how to code.", time:11, complexity:"medium", integrants:2 })
            CREATE (SunRotation:Project {title: "Sun_Rotation",description:"Calculate the angular velocity of the sun, coding", time:7, complexity:"low", integrants:3 })
            CREATE (Behaviorism:Project {title: "Behaviorism",description:"Experiment with people and theory of behaviorism", time:210, complexity:"easy", integrants:1})
            CREATE (Gestalt:Project {title: "Gestalt",description:"Experiment to avoid extintion", time:2102400000, complexity:"hard", integrants:55})
            CREATE (Avengers:Project {title: "Avengers",description:"Social experiment where a superhero is near of you", time:210, complexity:"medium", integrants:5})
            CREATE (CACAP:Project {title: "CACAP",description:"Centro de Administracion y Control Automatico de Papel", time:210, complexity:"hard", integrants:5})
            CREATE (SpaceWars:Project {title: "SpaceWars",description:"Make an space war", time:11, complexity:"medium", integrants:2 })
            CREATE (Notizen:Project {title: "NOTIZEN",description:"Make an app to take notes", time:7, complexity:"low", integrants:3 })
            CREATE (Simulator:Project {title: "SIMULATE_WITH_PHYSICS",description:"Simulate with unity a phenomenom of classic physics", time:210, complexity:"easy", integrants:1})
            CREATE (RRasberry:Project {title: "Robot_with_Raspberry",description:"Make a robot using a rapberry", time:210, complexity:"medium", integrants:5})
            CREATE (RArduino:Project {title: "Robot_with_arduino",description:"Make a robot using an arduino", time:210, complexity:"hard", integrants:5})
            CREATE (Story:Project {title: "Short_Story",description:"Write a short story", time:210, complexity:"hard", integrants:5})
            CREATE (ElasticConstat:Project {title: "A Simple Experiment for Determining the Elastic Constant of a Fine Wire",description:"Determining the Elastic Constant of a Fine Wire", time:210, complexity:"hard", integrants:4})
            CREATE (HollywoodPhysics:Project {title: "HollywoodPhysics",description:"Analyze hollywood movies with physics", time:210, complexity:"hard", integrants:3})
            CREATE (BrominationA:Project {title: "Bromination of alkanes",description:"Bromination of alkanes", time:3, complexity:"medium",integrants:2})
            CREATE (Halogenation:Project {title: "A Safe Simple Halogenation Experiment",description:"halogenation of alkanes", time:4, complexity:"hard", integrants:2})
            CREATE (Hydrogenation:Project {title: "Catalytic Hydrogenation of Organic Compounds without H2 Supply: An Electrochemical System",description:"Catalytic hydrogenation using a Electrochemical Cell", time:5, complexity:"hard", integrants:2})
            CREATE (SN2:Project {title: "A Simple SN2 Reaction for the Undergraduate Organic Laboratory",description:"making a bimolecular sustitution ", time:5, complexity:"hard", integrants:3})
            CREATE (Lisp:Project {title: "Lisp_Interpreter",description:"Recreate a lisp interpreter using java", time:210, complexity:"hard", integrants:3})
            CREATE (Recommendation:Project {title: "Recomendation_Algorithm",description:"Recreate an algorithm capable to make recommendations", time:210, complexity:"hard", integrants:3})
            CREATE (Sodium:Project {title: "Determination of sodium in Swiss cheese through the method of volhard",description:"Analyzing Swiss cheese", time:210, complexity:"hard", integrants:4})
            CREATE (Sanitary_Napkins_absorption:Project {title: "comparison of absorption of sanitary napkins of different brands",description:"Write a short story", time:210, complexity:"hard", integrants:5})
            CREATE (Aluminum_Recycling:Project {title: "Recycling of aluminum chip produced in UVG mechanics workshop",description:"Recycling aluminum for alum formation", time:110, complexity:"hard", integrants:5})
            CREATE (Inhibition_Klebsiella:Project {title: "Inhibition of Klebsiella pneumoniae biofilm through chamomile extract",description:"inhibit the growth of a bacterium by means of chamomile extract", time:510, complexity:"hard", integrants:5})
            CREATE (biomimic:Project {title: "Helmet simulating an armadillo",description:"make a motorcycle helmet that mimics one of the characteristics of the armadillo", time:410, complexity:"hard", integrants:5})
            CREATE (Fable:Project {title: "Fable",description:"write a story and dramatize it in class", time:210, complexity:"hard", integrants:8})
            CREATE (Reports:Project {title: "make reports over the internet",description:"create a program that allows to make denunciations by Internet", time:250, complexity:"hard", integrants:5})
            CREATE (Sonic_Pi:Project {title: "My own music",description:"create a song using sonic pi", time:510, complexity:"hard", integrants:4})
            CREATE (Pokultura:Project {title: "Pokultura",description:"a simple card game that involves culture", time:510, complexity:"medium", integrants:6})
            CREATE (mechanical_workshop:Project {title: "mechanical_workshop",description:"Create a program that organizes the information of a mechanical workshop", time:210, complexity:"hard", integrants:4})
            CREATE (political_parties:Project {title: "political_parties",description:"create political parties", time:310, complexity:"medium", integrants:9})
            CREATE (massacres_of_the_jungle:Project {title: "massacres_of_the_jungle",description:"historical book analysis", time:210, complexity:"medium", integrants:4})
            CREATE (Simon_says:Project {title: "Simon_says",description:"Simon game implementation says using ARM language", time:310, complexity:"hard", integrants:2})
            CREATE (slot_machines:Project {title: "slot_machines",description:"implementation of a slot game using ARM language", time:100, complexity:"medium", integrants:2})
            CREATE (Alarm_clock:Project {title: "Alarm_clock",description:"Alarm clock implemented in ARM language", time:510, complexity:"hard", integrants:2})
            CREATE (Timer:Project {title: "descending_counter.",description:"Timer: descending counter", time:315, complexity:"hard", integrants:2})
            CREATE (Piano:Project {title: "Piano",description:"implementation of a piano from electronic components and ARM language", time:410, complexity:"hard", integrants:2})
            CREATE (Stepper:Project {title: "Stepper_motor_controller",description:"implementation of a Stepper motor controller ARM language", time:210, complexity:"hard", integrants:2})
            CREATE (ALU:Project {title: "ALU",description:"Each switch will represent an arithmetic or logical operation: AND, OR, ADD and SUB", time:210, complexity:"hard", integrants:2})
            CREATE (revolutions_of_a_stepper:Project {title: "revolutions_of_a_stepper",description:"implementation of a Stepper knowing the number of revolutions and direction", time:310, complexity:"hard", integrants:2})
            CREATE (Angular_velocity:Project {title: "Angular_velocity",description:"direct measurement using a Smartphone", time:100, complexity:"medium", integrants:4})
            CREATE (Youngs_Modulus_of_a_Marshmallow:Project {title: "Youngs_Modulus_of_a_Marshmallow",description:"determining Young's Modulus of a Marshmallow", time:50, complexity:"easy", integrants:4})
            CREATE (Slipping_Tipping:Project {title: "Slipping_and_Tipping",description:"Measuring Static Friction with a Straightedge", time:110, complexity:"medium", integrants:4})
            CREATE (Rotational_energy:Project {title: "Rotational_energy",description:"determinating Rotational energy in a physical pendulum", time:200, complexity:"medium", integrants:4})
            CREATE (Torque:Project {title: "A_New_Twist_on_Torque Labs.",description:"Measure the force that must act on the end of a pivoted rule", time:60, complexity:"easy", integrants:5})
            CREATE (Stability:Project {title: "Stability_of_a_Can_of_Soda",description:"determinating the stability of a can soda in a car", time:110, complexity:"hard", integrants:5})
            CREATE (Angular_Momentum:Project {title: "Which_reaches_the_bottom_first",description:"Using your knowledge of the dynamics of rotation, determine which object will first reach the bottom of an inclined plane.", time:75, complexity:"easy", integrants:4})
            CREATE (Center_of_gravity:Project {title: "Center_of_gravity_of_a_student",description:"Use two bathroom scales to determine the location of the center of gravity using two different assemblies", time:510, complexity:"hard", integrants:5})
            CREATE (Sun_Rotation:Project {title: "Sun_Rotation",description:"Using the Solar & Heliospheric Observatory Satellite (SOHO) to Determine the Rotation of the Sun", time:310, complexity:"hard", integrants:5})
            CREATE (Torque_Angle:Project {title: "Torque_Angle",description:"Obtain experimentally the dependence of the sinus torque of the angle.", time:210, complexity:"hard", integrants:5})
            CREATE (Jumping_frogs:Project {title: "Jumping_frogs",description:"Game simulation using electronic components and ARM language", time:510, complexity:"hard", integrants:2})
            CREATE (word_leak:Project {title: "word_leak",description:"Game simulation using electronic components and ARM language,the game consists in generating incomplete words and the user must complete them", time:310, complexity:"hard", integrants:2})
            CREATE (four_in_line:Project {title: "four_in_line",description:"Game simulation using electronic components and ARM language", time:210, complexity:"hard", integrants:2})
            CREATE (Race:Project {title: "Race_with_obstacles",description:"Game simulation using electronic components and ARM language, the game consist in get to the goal first", time:510, complexity:"hard", integrants:2})
            CREATE (greater_or_lesser:Project {title: "greater_or_lesser",description:"Game simulation using electronic components and ARM language, the game consist in roll two dice and win the one with the largest number", time:320, complexity:"hard", integrants:2})
            CREATE (2_Pics_1_Word:Project {title: "2_Pics_1_Word",description:"Game simulation using electronic components and ARM language, the game consist in show images that have a common theme and below disordered words which must be ordered in relation to the images", time:210, complexity:"hard", integrants:3})
            CREATE (Battleship:Project {title: "Battleship",description:"Game simulation using electronic components and ARM language, recreating the famous game of the same name", time:210, complexity:"hard", integrants:3})
            CREATE (Minesweep:Project {title: "Minesweep",description:"Game simulation using electronic components and ARM language, recreating the famous game of the same name", time:310, complexity:"hard", integrants:3})
            CREATE (Rabbit_Chase:Project {title: "Rabbit_Chase",description:"Game simulation using electronic components and ARM language, recreating the famous game of the same name", time:210, complexity:"hard", integrants:3})
            CREATE (GO:Project {title: "GO",description:"Game simulation using electronic components and ARM language, recreating the famous game of the same name", time:210, complexity:"medium", integrants:3})
            CREATE (pair_odd:Project {title: "pair_odd",description:"Game simulation using electronic components and ARM language, recreating the famous game of the same name", time:210, complexity:"hard", integrants:3})
            CREATE (Uplift_count:Project {title: "Uplift_count_from_0_to_9",description:"Using circuit knowledge create an ascending counter from 0 to 9", time:210, complexity:"medium", integrants:4})
            CREATE (Descending_count:Project {title: "Descending_count_of_9_to_0",description:"Using circuit knowledge create a descending counter from 9 to 0", time:210, complexity:"medium", integrants:3})
            CREATE (Active_bit_shift:Project {title: "Active_bit_shift",description:"Using circuit knowledge simulate a logic circuit with 8 output bits that performs the bit shift (active bit, issay, bit on and the others off)", time:210, complexity:"hard", integrants:3})
            CREATE (Inactive_bit_shift:Project {title: "Inactive_bit_shift",description:"Using circuit knowledge simulate a logic circuit with 8 output bits that performs the bit shift", time:210, complexity:"hard", integrants:3})
            CREATE (Bit_accumulator:Project {title: "Bit_accumulator",description:"Using circuit knowledge simulate a logic circuit that represents a bit accumulator", time:210, complexity:"hard", integrants:3})
            CREATE (traffic_light:Project {title: "traffic_light",description:"a two way traffic light", time:210, complexity:"hard", integrants:2})
            CREATE (stone_paper_or_scissors:Project {title: "stone_paper_or_scissors",description:"Design and simulate a logic circuit that implements the game of stone paper or scissors, using gates,dip-switches and LEDs, which complies with the established rules: scissors beats paper, paper beats stoneand stone beats scissors", time:210, complexity:"hard", integrants:2})
            CREATE (AU:Project {title: "Arithmetic_Unit",description:"Design and simulate a circuit that implements the behavior of an Arithmetic Unit", time:210, complexity:"hard", integrants:3})
            CREATE (Turn_signals:Project {title: "Turn_signals",description:"Design and simulate a logic circuit that implements the behavior of the directional lights of a car", time:210, complexity:"hard", integrants:3})
            CREATE (Comparator_of_Numbers:Project {title: "Comparator_of_Numbers",description:"Design and simulate a circuit that has as input two numbers from 0 to 7 signed in addition to 2.", time:210, complexity:"hard", integrants:3})
            CREATE (Totito:Project {title: "Totito",description:"Design and simulate a circuit that represents the characteristic grid of the game, using LEDS, switches and gates", time:210, complexity:"hard", integrants:4})
            CREATE (LLS:Project {title: "LLS",description:"Design and simulate a circuit that represents the process of logically running a binary number towards the left", time:210, complexity:"hard", integrants:3})
            CREATE (LRS:Project {title: "LRS",description:"Design and simulate a circuit that represents the process of logically running a binary number towards the right", time:210, complexity:"hard", integrants:3})
            CREATE (Address_decoder:Project {title: "Address_decoder",description:"Design and simulate a circuit that decodes a 3-bit binary address and selects the position correct cell within a memory", time:210, complexity:"hard", integrants:3})
            CREATE (Binary_to_vowel_converter:Project {title: "Binary_to_vowel_converter",description:"Design and simulate a circuit that shows the vowels A, E, I, O, U. A binary number of 3 bits represents each vowel", time:210, complexity:"hard", integrants:3})
                
            CREATE (Computer:Resource {title: "Computer", specifications: "A computer with an ide to code"})
            CREATE (Unity:Resource {title: "Unity", specifications: "Software Unity"})
            CREATE (Arduino:Resource {title: "Arduino", specifications: "Arduino a mini-computer"})
            CREATE (AndroidStudio:Resource {title: "AndroidStudio", specifications: "Android Studio software"})
            CREATE (Fruit:Resource {title: "fruit", specifications: "A fresh fruit"})
            CREATE (Vegetable:Resource {title: "vegetable", specifications: "A fresh vegetable"})
            CREATE (Subjects:Resource {title: "subjects", specifications: "Humans for investigation"})
            CREATE (Custom:Resource {title: "custom", specifications: "a custom or suit"})
            CREATE (Raspberry:Resource {title: "raspberry", specifications: "a mini-computer with raspberry"})
            CREATE (Paper:Resource {title: "Paper", specifications: "Paper to write"})

            CREATE (DataStructure:Course {title: "Data Structure",Departament: "Computer Science"})
            CREATE (Physics2:Course {title: "Physics 2",Departament: "Physics"})
            CREATE (Physics1:Course {title: "Physics 1",Departament: "Physics"})
            CREATE (Psicology:Course {title: "Basic psicology",Departament:"Psicology"})
            CREATE (Humanity:Course {title: "Humanity Sciences",Departament:"Social studies"})
            CREATE (Code:Course {title: "Basic coding",Departament:"Computer Sciences"})
            CREATE (VideoGames:Course {title: "VideoGames",Departament:"Computer Sciences"})
            CREATE (MobilePlataforms:Course {title: "Mobile Plataforms",Departament:"Computer Sciences"})
            CREATE (Assembler:Course {title: "Assembler",Departament:"Computer Sciences"})
            CREATE (Letters:Course {title: "Writing",Departament:"Languages"})
            CREATE (Organic1:Course {title: "Organic Chemistry",Departament:"Chemistry"})
            
            CREATE
                (ProjectGenerator)-[:PROJECT_FOR]->(DataStructure),
                (Story)-[:PROJECT_FOR]->(Letters),
                (Story)-[:USE_A]->(Paper),
                (Story)-[:USE_A]->(Computer),
                (Notizen)-[:PROJECT_FOR]->(Code),
                (RRasberry)-[:PROJECT_FOR]->(Code),
                (RArduino)-[:PROJECT_FOR]->(Code),
                (RRasberry)-[:USE_A]->(Raspberry),
                (RArduino)-[:USE_A]->(Arduino),
                (RRasberry)-[:USE_A]->(Computer),
                (RArduino)-[:USE_A]->(Computer),
                (Simulator)-[:USE_A]->(Unity),
                (Simulator)-[:USE_A]->(Computer),
                (HollywoodPhysics)-[:USE_A]->(Computer),
                (HollywoodPhysics)-[:USE_A]->(Paper),
                (SpaceWars)-[:USE_A]->(Unity),
                (SpaceWars)-[:USE_A]->(Computer),
                (Notizen)-[:USE_A]->(AndroidStudio),
                (Notizen)-[:USE_A]->(Computer),
                (ElasticConstat)-[:USE_A]->(Paper),
                (HollywoodPhysics)-[:PROJECT_FOR]->(Physics2),
                (RRasberry)-[:PROJECT_FOR]->(Assembler),
                (ElasticConstat)-[:PROJECT_FOR]->(Physics2),
                (RArduino)-[:PROJECT_FOR]->(Assembler),
                (Notizen)-[:PROJECT_FOR]->(MobilePlataforms),
                (Simulator)-[:PROJECT_FOR]->(Code),
                (Simulator)-[:PROJECT_FOR]->(VideoGames),
                (Simulator)-[:PROJECT_FOR]->(Physics2),
                (Simulator)-[:PROJECT_FOR]->(Physics1),
                (SpaceWars)-[:PROJECT_FOR]->(Code),
                (SpaceWars)-[:PROJECT_FOR]->(VideoGames),
                (SunRotation)-[:PROJECT_FOR]->(Physics2),
                (SunRotation)-[:PROJECT_FOR]->(DataStructure),
                (SunRotation)-[:PROJECT_FOR]->(Code),
                (Gestalt)-[:USE_A]->(Computer),
                (Gestalt)-[:PROJECT_FOR]->(Humanity),
                (SunRotation)-[:USE_A]->(Computer),
                (Gestalt)-[:USE_A]->(Subjects),
                (ProjectGenerator)-[:USE_A]->(Computer),
                (Behaviorism)-[:PROJECT_FOR]->(Psicology),
                (Behaviorism)-[:USE_A]->(Vegetable),
                (Behaviorism)-[:USE_A]->(Fruit),
                (Behaviorism)-[:USE_A]->(Subjects),
                (Avengers)-[:USE_A]->(Subjects),
                (Avengers)-[:PROJECT_FOR]->(Psicology),
                (Avengers)-[:USE_A]->(Custom),
                (CACAP)-[:USE_A]->(Raspberry),
                (CACAP)-[:PROJECT_FOR]->(Code)"""
            with self._driver.session() as session: 
                return session.write_transaction(self._Default,result)


    @staticmethod
    def _Default(tx,result):
        return tx.run(result)

    @staticmethod
    def _getNodes(tx,result,value):
        return tx.run(result,value=value)

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
