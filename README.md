# ProjectGenerator
ProjectGenerator is a software that shows and recommend projects to people that need it.
ProjectGenerator uses Graph-Database of Neo4J

To run ProjectGenerator you must do the following steps:

	1. Open a cmd terminal and run the following commands:

		For windows:

			1. python -m pip install --upgrade pip wheel setuptools
			2. python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
			3. python -m pip install kivy.deps.gstreamer

			If you encounter a MemoryError while installing:

				python -m pip install kivy.deps.angle

			4. python -m pip install kivy

		For Ubuntu:

			1. Add one of the PPAs as you prefer

			    stable builds:	$ sudo add-apt-repository ppa:kivy-team/kivy
			    nightly builds:	$ sudo add-apt-repository ppa:kivy-team/kivy-daily

			2. Update your package list using your package manager

    			$ sudo apt-get update

			3. Install Kivy

			    Python2 - python-kivy:
			     	$ sudo apt-get install python-kivy
			    Python3 - python3-kivy:
			     	$ sudo apt-get install python3-kivy
			    optionally the examples - kivy-examples:
			     	$ sudo apt-get install kivy-examples
	

		Other:
			Search for kivy installation for your OS

	2. Visit https://neo4j.com/download/ y descargar Neo4J
	3. Afeter download Neo4J install Neo4j Python Driver

		For windows:
			pip install neo4j

	4. Open Neo4J desktop and create a new graph, set the name and password

		Check that the uri of the database is:bolt://localhost:7687

			1. Click in Start
			2. Click in Manage
			3. Click in Open Browser
			4. Run :server connect in Neo4J Browser Shell
			5. URL should be bolt://localhost:7687

				If the URL is not bolt://localhost:7687

					1. Open the repository folder ProjectGenerator
					2. Go to ProjectGenerator\ProjectGenerator\ProjectGenerator.py
					3. Change first parameter in code line 16 with the URI of the graph

	5.Create a new User

		1. On Neo4J browser shell run the following command :server user add
		2. Create a new user named 	"Default" with the following password "password", be sure that admin and editor roles are added to this user

			If  you want to set you own user data follow the following steps

				1. Open the repository folder ProjectGenerator
				2. Go to ProjectGenerator\ProjectGenerator\ProjectGenerator.py	
				3. Change the second parameter with the user, and the third parameter with the password


	6. Run Main.py

		1. Open a new cmd and go to Project Generator folder
		2. Open \ProjectGenerator\ProjectGenerator 	
		3. run the following command Python Main.py

	7. Enjoy Project Generator software

	ADVICES:

		1. If you want a recomendations and if you haven´t seen a project it will show you nothing. 
		2. Be patient getting the recomendations because the program is getting the data from the database
		3. You will be able to see the recomendations on the CMD and in the GUI

If you find problems running this software write us to con18409@uvg.edu.gt



