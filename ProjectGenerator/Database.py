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
            CREATE (Car_stopping_Distance_on_a_Tabletop:Project {title: "Car_stopping_Distance_on_a_Tabletop",description:"Write a short story", time:210, complexity:"hard", integrants:5})
            CREATE (The_energetics_of_a_bouncing ball:Project {title: "The_energetics_of_a_bouncing ball",description:"calculating the energy of a bouncing ball", time:210, complexity:"hard", integrants:4})
            CREATE (Cotton_buds:Project {title: "Cotton_buds_momentum_and_impulse",description:"determinating momentum and impulse of cotton buds", time:510, complexity:"easy", integrants:5})
            CREATE (Bernoulli_Law:Project {title: "Bernoulli_Law",description:"A Bernoulli's Law Lab in a Bottle", time:210, complexity:"hard", integrants:5})
            CREATE (Archimedes_Principle:Project {title: "Archimedes_Principle",description:"Microcomputer-Based Laboratory for Archimedes Principle and Density of Liquids", time:210, complexity:"hard", integrants:5})
            CREATE (Radio:Project {title: "Radio",description:"Simulate a Radio using java language", time:110, complexity:"hard", integrants:2})
            CREATE (Calculator:Project {title: "Calculator",description:"Simulate a calculator using java language, the calculator interface must work for all main programs", time:210, complexity:"hard", integrants:5})
            CREATE (Sorts:Project {title: "Sorts",description:"using a profiler meassure the time that each sort spent sorting", time:210, complexity:"hard", integrants:2})
            CREATE (Design_patterns:Project {title: "Design_patterns",description:"Simulate a post-fix calculator using factory and singleton design patterns", time:210, complexity:"hard", integrants:2})
            CREATE (Simpy:Project {title: "Simpy",description:"Using simpy enviroment recreate the operation of a processor", time:210, complexity:"medium", integrants:2})
            CREATE (Cards:Project {title: "Cards",description:"recreate a card game using java language", time:210, complexity:"hard", integrants:2})
            CREATE (Dictionary:Project {title: "Dictionary",description:"Create a dictionary that can translate phrases with stored words", time:210, complexity:"hard", integrants:2})
            CREATE (movies:Project {title: "movies",description:"recreating movie recommendations depending on the movies viewed by the user", time:510, complexity:"hard", integrants:5})
            CREATE (Places:Project {title: "places",description:"recommend people places to visit in Guatemala", time:210, complexity:"hard", integrants:5})
            CREATE (Hospital:Project {title: "Hospital",description:"create a hospital system that allows patients to be stored and ordered in order of priority of illness", time:210, complexity:"easy", integrants:2})
            CREATE (Dicc:Project {title: "dicc",description:"Recreate a dictionary using binary trees", time:210, complexity:"hard", integrants:2})
            CREATE (Hexa:Project {title: "Hexa",description:"Recreate a calculator that conver decimal numbers to hexadecimal", time:210, complexity:"hard", integrants:1})
            CREATE (Planes:Project {title: "Planes",description:"create a program in java language that stores aircraft with your specifications", time:210, complexity:"hard", integrants:3})
            CREATE (students:Project {title: "Students",description:"calculate and order the averages of aspiring students to enter the university", time:210, complexity:"easy", integrants:1})
            CREATE (cinema:Project {title: "cinema",description:"Sort the data of a chain of movie theaters about visitors and raising money", time:210, complexity:"easy", integrants:1})
            CREATE (library:Project {title: "library",description:"create a program in java language to have control of book loans in a library", time:210, complexity:"easy", integrants:1})
            CREATE (ipod:Project {title: "ipod",description:"simulate the functionality of an ipod with an interface that can be used in different main programs in java language", time:210, complexity:"easy", integrants:1})
            CREATE (GUI:Project {title: "GUI",description:"learn to use graphical interface in java", time:210, complexity:"easy", integrants:1})
            CREATE (guards:Project {title: "guards",description:"create a program that keeps track of how many shifts a guard has to make per month", time:210, complexity:"easy", integrants:1})
            CREATE (radioactive:Project {title: "radioactive",description:"create a reactivity simulator of a compound to calculate how long it will take to stop being radioactive", time:210, complexity:"medium", integrants:1})
            CREATE (ticket:Project {title: "ticket",description:"create a simulator of a machine that generates tickets in java language", time:210, complexity:"easy", integrants:1})
            CREATE (figures:Project {title: "figures",description:"create figures that move from side to side using bluj", time:210, complexity:"easy", integrants:1})
            CREATE (Hollywood_Movies:Project {title: "Hollywood_Movies",description:"analyze Hollywood movies with statistical tools", time:210, complexity:"easy", integrants:1})
            CREATE (riddle:Project {title: "riddle",description:"create a program using python language to read a text and decipher a hidden code", time:210, complexity:"medium", integrants:1})
            CREATE (angle:Project {title: "angle",description:"create a program in python language that calculates the angles of a triangle", time:210, complexity:"hard", integrants:5})
            CREATE (Mongo:Project {title: "Mongo",description:"Short exercise using mongo db", time:210, complexity:"easy", integrants:1})
            CREATE (Texas_Holdem:Project {title: "Texas_Holdem",description:"Recreate the card game Texas Holdem using python language", time:210, complexity:"hard", integrants:1})
            CREATE (Menu:Project {title: "Menu",description:"Create a menu of food using python language", time:210, complexity:"easy", integrants:1})
            CREATE (Quiniela:Project {title: "Quiniela",description:"Create a program in python language that can recreate a football quiniela", time:210, complexity:"hard", integrants:1})
            CREATE (Law_Sines:Project {title: "Law_Sines",description:"Create a program in python language that calculate that use the law sines", time:210, complexity:"easy", integrants:1})
            CREATE (grades:Project {title: "grades",description:"create a program in python language that can calculate how much do you need to pass the class", time:210, complexity:"easy", integrants:1})
            CREATE (Frog:Project {title: "Frog",description:"simulate a game based in jumping frogs using python language", time:210, complexity:"hard", integrants:1})
            CREATE (canibals_and_missionaries:Project {title: "canibals_and_missionaries",description:"recreate the game canibals and missionaries using python language", time:210, complexity:"hard", integrants:1})
            CREATE (bill:Project {title: "bill",description:"create a program using python language to calculate a restaurant account", time:210, complexity:"easy", integrants:1})
            CREATE (Lost_items:Project {title: "Lost_items",description:"Create a program in python language that help the students in college to find their lost items", time:210, complexity:"hard", integrants:5})
            CREATE (frequency:Project {title: "frequency",description:"Create a program with python language that analyze sounds frequencies", time:210, complexity:"medium", integrants:1})
            CREATE (arithmetic:Project {title: "arithmetic",description:"Create a program in python language that can make all arithmetic operations", time:210, complexity:"easy", integrants:1})
            CREATE (Series:Project {title: "Series",description:"create a program in java language that can recommend series depending on the user's preferences", time:210, complexity:"hard", integrants:5})
            CREATE (Restaurants:Project {title: "Restaurants",description:"Create a program in java language that can recommend restaurants depending on the users tastes", time:210, complexity:"hard", integrants:5})
            CREATE (Videogames:Project {title: "Videogames",description:"Create a program in java language that can recommend videogames", time:210, complexity:"hard", integrants:5})
            CREATE (rurple:Project {title: "rurple",description:"Create a short maze with the robot to learn to use rurple", time:210, complexity:"easy", integrants:1})
            CREATE (chocolates:Project {title: "chocolates",description:"cook chocolates using liquid nitrogen", time:210, complexity:"hard", integrants:5})
            CREATE (autobiography:Project {title: "autobiography",description:"Write an autobiography using news from dates mentioned", time:210, complexity:"easy", integrants:1})
            CREATE (elevator:Project {title: "elevator",description:"With electronical knowledge simulate an elevator", time:210, complexity:"hard", integrants:2})
            CREATE (car_video_game:Project {title: "car_video_game",description:"Create a videogame that allow to play with physical components", time:210, complexity:"hard", integrants:5})
            CREATE (Pressure:Project {title: "Pressure",description:"Change in systolic pressure before and after the ingestion of an energizing drink", time:210, complexity:"hard", integrants:5})
            CREATE (classical_music:Project {title: "classical_music",description:"Effect of classical music on the memory of the elderly", time:210, complexity:"hard", integrants:5})
            CREATE (caffeine:Project {title: "caffeine",description:"Compare the reaction time with and without coffee intake", time:210, complexity:"hard", integrants:5})
            CREATE (decibels:Project {title: "decibels",description:"Comparison of the decibel level produced by the sound equipment of a car with closed windows and one with open windows", time:210, complexity:"hard", integrants:5})
            CREATE (nicotine:Project {title: "nicotine",description:"Efecto de la nicotina en el rendimiento de la condición física", time:210, complexity:"hard", integrants:5})
            CREATE (glues:Project {title: "glues",description:"Comparison between 2 types of glues", time:210, complexity:"hard", integrants:5})
            CREATE (blood_sugar:Project {title: "blood_sugar",description:"Blood sugar levels after eating", time:210, complexity:"hard", integrants:5})
            CREATE (drinks:Project {title: "drinks",description:"Comparison of blood sugar levels with two different beverages", time:210, complexity:"hard", integrants:5})
            CREATE (paint:Project {title: "paint",description:"Effectiveness level of a paint or waterproofing layer", time:210, complexity:"hard", integrants:5})
            CREATE (diet_coke:Project {title: "diet_coke",description:"There is a significant difference between the gas content between a normal cola water and its dietary counterpart", time:210, complexity:"hard", integrants:5})
            CREATE (milks:Project {title: "milks",description:"Is there significant difference in boiling time between two different types of milk", time:210, complexity:"hard", integrants:5})
            CREATE (Sanitary_nap:Project {title: "Sanitary_nap",description:"Is there a significant difference in absorption between two different types of sanitary napkins of the same brand", time:210, complexity:"hard", integrants:5})
            CREATE (batteries:Project {title: "batteries",description:"s there a significant difference in the duration of charging between alkaline batteries compared to traditional batteries", time:210, complexity:"hard", integrants:5})
            CREATE (boiling_fusion_point:Project {title: "boiling_fusion_point",description:"Determination of Boiling Point and Fusion Point", time:210, complexity:"easy", integrants:3})
            CREATE (liquid_liquid_extraction:Project {title: "liquid-liquid_extraction",description:"Liquid-liquid extraction of caffeine from an energy pill", time:210, complexity:"easy", integrants:2})
            CREATE (biofuel:Project {title: "biofuel",description:"Simple and Fractional Distillation Production of biofuel: Ethanol from several substrates", time:210, complexity:"hard", integrants:2})
            CREATE (Steam:Project {title: "Steam",description:"Steam Trap Distillation", time:210, complexity:"hard", integrants:2})
            CREATE (Chromatography:Project {title: "Chromatography",description:"Thin Layer and Column Chromatography", time:210, complexity:"hard", integrants:2})
            CREATE (Re_crystallization:Project {title: "Re-crystallization",description:"Re-crystallization", time:210, complexity:"hard", integrants:2})
            CREATE (Halogenation_Alquenos:Project {title: "Halogenation_Alquenos",description:"Halogenation of Alquenos", time:210, complexity:"hard", integrants:2})
            CREATE (Catalytic_hydrogenation:Project {title: "Catalytic_hydrogenation",description:"Catalytic hydrogenation using an electrochemical system", time:210, complexity:"hard", integrants:3})
            CREATE (SN2_strawberries:Project {title: "SN2_strawberries",description:"SN2: Synthesis of artificial flavor to strawberries and raspberries", time:210, complexity:"hard", integrants:2})
            CREATE (antacid:Project {title: "antacid",description:"Titration of an antacid tablet", time:210, complexity:"easy", integrants:4})
            CREATE (vinegar:Project {title: "vinegar",description:"determine acetic acid content in a vinegar sample", time:210, complexity:"easy", integrants:4})
            CREATE (junk_food:Project {title: "junk_food",description:"How many calories are in junk food", time:210, complexity:"easy", integrants:5})
            CREATE (Hess_law:Project {title: "Hess_law",description:"Verification of Hess's law", time:210, complexity:"hard", integrants:5})
            CREATE (Neutralization:Project {title: "Short_Story",description:"Heat of Neutralization", time:210, complexity:"hard", integrants:5})
            CREATE (The_Yodo_clock:Project {title: "The_Yodo_clock",description:"The Yodo clock", time:210, complexity:"hard", integrants:5})
            CREATE (Le_Chatelier:Project {title: "Le_Chatelier",description:"Constant balance and Le Chatelier", time:210, complexity:"hard", integrants:5})
            CREATE (kps:Project {title: "kps",description:"Measurement of the equilibrium constant of solubility of a compound", time:210, complexity:"hard", integrants:5})
            CREATE (pH:Project {title: "pH",description:"Determination of ph of certain solutions", time:210, complexity:"hard", integrants:5})
            CREATE (separation_mixture:Project {title: "separation_mixture",description:"Separation of compounds from a mixture", time:210, complexity:"easy", integrants:5})
            CREATE (chemical_reactions:Project {title: "Short_Story",description:"types of chemical reactions", time:210, complexity:"easy", integrants:5})
            CREATE (metathesis:Project {title: "metathesis",description:"Metathesis reactions in aqueous solution", time:210, complexity:"easy", integrants:5})
            CREATE (hydrate:Project {title: "hydrate",description:"Determination of the formula of a hydrate", time:210, complexity:"hard", integrants:5})
            CREATE (Stoichiometry:Project {title: "Stoichiometry",description:"Stoichiometry of a reaction", time:210, complexity:"easy", integrants:5})
            CREATE (R_constant:Project {title: "R_constant",description:"Calculation of the constant R", time:210, complexity:"hard", integrants:5})
            CREATE (Manganese_colors:Project {title: "Manganese_colors",description:"Knowing the colors of Manganese by redox titration", time:210, complexity:"easy", integrants:4})
            CREATE (performance:Project {title: "performance",description:"Percentage of reaction performance aluminum recycling", time:210, complexity:"hard", integrants:4})
            CREATE (Copper:Project {title: "Copper",description:"Percentage of reaction performance, Copper chemical transformations", time:210, complexity:"hard", integrants:4})
            CREATE (physical_properties:Project {title: "physical_properties",description:"Relationship between chemical bonds and physical properties", time:210, complexity:"hard", integrants:4})

            
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
            CREATE (Global_citizenship:Course {title: "Global_citizenship",Departament:"social Sciences  "})
            CREATE (POO:Course {title: "POO",Departament:"Computer Sciences"})
            CREATE (algorithms_and_basic_programming:Course {title: "algorithms_and_basic_programming",Departament:"Computer Sciences"})
            CREATE (botany1:Course {title: "botany1",Departament:"biology"})
            CREATE (genetic_resources:Course {title: "genetic_resources",Departament:"biology"})
            CREATE (system_and_evolution:Course {title: "system_and_evolution",Departament:"biology"})
            CREATE (forest_ecology:Course {title: "forest_ecology",Departament:"biology"})
            CREATE (biometrics:Course {title: "biometrics",Departament:"biology"})
            CREATE (histology_and_histochemistry:Course {title: "histology_and_histochemistry",Departament:"biology"})
            CREATE (introduction_to_molecular_biosciences:Course {title: "introduction_to_molecular_biosciences",Departament:"molecular biotechnology"})
            CREATE (biochemistry_of_macromolecules:Course {title: "biochemistry_of_macromolecules",Departament:"molecular biotechnology"})
            CREATE (microbiology1:Course {title: "microbiology1",Departament:"molecular biotechnology"})
            CREATE (general_inmunology:Course {title: "general_inmunology",Departament:"molecular biotechnology"})
            CREATE (molecular_biology:Course {title: "molecular_biology",Departament:"molecular biotechnology"})
            CREATE (bioinformatics:Course {title: "bioinformatics",Departament:"molecular biotechnology"})
            CREATE (biogeography:Course {title: "biogeography",Departament:"molecular biotechnology"})
            CREATE (databases:Course {title: "databases",Departament:"Computer sciences"})
            CREATE (statistics1:Course {title: "statistics1",Departament:"mathematics"})
            CREATE (statistics2:Course {title: "statistics2",Departament:"mathematics"})
            CREATE (life_sciences:Course {title: "life_sciences",Departament:"biology"})
            CREATE (IPC:Course {title: "IPC",Departament:"investigation"})
            CREATE (project_management:Course {title: "project_management",Departament:"administration"})
            CREATE (electrical_circuits:Course {title: "electrical_circuits",Departament:"electronics"})
            CREATE (analogic_electronics:Course {title: "analogic_electronics",Departament:"electronics"})
            CREATE (Design_Thinking:Course {title: "Design_Thinking",Departament:"investigation"})
            CREATE (electromagnetic_theory:Course {title: "electromagnetic_theory",Departament:"physic"})
            CREATE (thermodynamics1:Course {title: "thermodynamics1",Departament:"physic"})
            CREATE (thermodynamics:Course {title: "thermodynamics2",Departament:"physic"})
            CREATE (bioengineering:Course {title: "bioengineering",Departament:"chemistry"})
            CREATE (chemistry1:Course {title: "chemistry1",Departament:"chemistry"})
            CREATE (chemistry2:Course {title: "chemistry2",Departament:"chemistry"})
            CREATE (general_chemistry:Course {title: "general_chemistry",Departament:"chemistry"})
            CREATE (analytic_chemistry:Course {title: "analytic_chemistry",Departament:"chemistry"})
            CREATE (physical_chemistry:Course {title: "physical_chemistry",Departament:"chemistry"})
            CREATE (dynamic_mechanics:Course {title: "dynamic_mechanics",Departament:"mechanics"})
            CREATE (draw_CAD:Course {title: "draw_CAD",Departament:"Design"})
            
            
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
