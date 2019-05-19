class database:
	import pickle
	'''
	 - DATA STRUCTURE:
	 Each player is part of ONE world only.

	 Each player's info is stored in /data/players.
	 The object will contain info on the world the
	 player is in.

	 The worlds are files stored in /data/worlds.
	 World names are always unique.
	 
	 get player's world (might just add function)
	 updateWorld(getPlayer(sender).world)

	 file = open("data/data.txt", 'w')
	 file.write("hello world") 
	'''
	#functions to add and modify data
	def setPlayer(self, chat_id, data):
		import pickle
		pfile = open('data/players/' + str(chat_id) + '.txt','wb')
		pickler = pickle.Pickler(pfile)
		for e in data:
			pickler.dump(e)

		pfile.close()


	def setWorld(self, data, world_name):
		import pickle
		pfile = open('data/worlds/' + str(world_name) + '.txt','wb')
		pickle.dump(data, pfile)
		pfile.close()
		pass

	def updateWorld(self, data, world_name):
		pass

	#functions to get data, READ-ONLY
	def getPlayer(self, chat_id, read_coords):
		import pickle
		pfile = open('data/players/' + str(chat_id) + '.txt', 'rb')
		unpickler = pickle.Unpickler(pfile)
		if (read_coords):
			unpickler.load()
		return unpickler.load()

	def getPlayerWorld(self, chat_id):
		import pickle


	def getWorldFull(self, world_name):
		import pickle
		pfile = open('data/worlds/' + str(world_name) + '.txt', 'rb')
		return pickle.Unpickler(pfile).load()

	#functions to check
	def isWorld(self, world_name):
		import os
		return os.path.isfile("data/worlds/" + str(world_name) + '.txt')

	def spawn_player(self, world_name):
		import numpy as np
		from map.classes import biome
		import random
		world_array = self.getWorldFull(world_name)
		invalid_biomes = [1, 2, 3, 4, 5, 7, 8, 9, 13, 16, 17, 18] #config later
		coord_array = np.array([[0,0]])
		for i in range(0, world_array.shape[0]):
			if (not(world_array[i].type in invalid_biomes)):
				coord_array = np.concatenate((coord_array, world_array[i].coords))
		coord_array = coord_array.tolist()
		coord_array.pop(0)
		return random.choice(coord_array)
		#get world


