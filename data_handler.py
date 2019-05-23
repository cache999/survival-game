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

	 file = open("data/data.map", 'w')
	 file.write("hello world") 
	'''
	#functions to add and modify data
	def setPlayer(self, chat_id, data, read_coords):
		import pickle
		if (read_coords):
			pfile = open('data/players/' + str(chat_id) + '.ec','wb')
		else:
			pfile = open('data/players/' + str(chat_id) + '.dt', 'wb')
		pickler = pickle.Pickler(pfile)
		pickler.dump(data)
		pfile.close()

	def setWorld(self, data, id_array, info, world_name):
		import pickle
		import numpy as np
		if (not(type(data) is int)):
			pfile = open('data/worlds/' + str(world_name) + '.map','wb')
			pickle.dump(data, pfile)
			pfile.close()
		if (not(type(id_array) is int)):
			np.save('data/worlds/' + str(world_name) + '.ids', id_array)
		if (not(type(info) is int)):
			pfile = open('data/worlds/' + str(world_name) + '.dt','wb')
			pickle.dump(info, pfile)
			pfile.close()
		return


	#functions to get data, READ-ONLY
	def getPlayer(self, chat_id, read_coords):
		import pickle
		if (read_coords):
			pfile = open('data/players/' + str(chat_id) + '.ec', 'rb')
		else:
			pfile = open('data/players/' + str(chat_id) + '.dt', 'rb')
		unpickler = pickle.Unpickler(pfile)
		return unpickler.load()

	def getPlayerWorld(self, chat_id):
		import pickle
		from map.classes import char
		return self.getPlayer(chat_id, 0).world

	def getMapDir(self, world_name):
		return 'data/worlds/' + str(world_name) + '.png'

	def getWorldMap(self, world_name):
		import pickle
		pfile = open('data/worlds/' + str(world_name) + '.map', 'rb')
		return pickle.Unpickler(pfile).load()
	def getWorldData(self, world_name):
		import pickle
		pfile = open('data/worlds/' + str(world_name) + '.dt', 'rb')
		return pickle.Unpickler(pfile).load()
	def getWorldBIDs(self, world_name):
		import numpy as np
		mmap_ids = np.load('data/worlds/' + str(world_name) + '.ids.npy', mmap_mode='r')
		return mmap_ids

	#functions to check
	def isWorld(self, world_name):
		import os
		return os.path.isfile("data/worlds/" + str(world_name) + '.map')

	def spawn_player(self, world_name):
		import numpy as np
		from map.classes import biome
		import random
		import matplotlib.pyplot as plt
		world_array = self.getWorldMap(world_name)
		invalid_biomes = [1, 2, 3, 4, 5, 7, 8, 9, 13, 16, 17, 18] #config later
		coord_array = np.array([[0,0]])
		for i in range(0, world_array.shape[0]):
			if (not(world_array[i].type in invalid_biomes)):
				coord_array = np.concatenate((coord_array, world_array[i].coords))
		coord_array = coord_array.T
		choice = random.randint(0, coord_array.shape[1])
		choice = [coord_array[0][choice], coord_array[1][choice]]
		return [choice[1], choice[0]]
		#get world
	def appendToPlayerCoords(self, chat_id, explored_coords):
		pass

	def worldList(self):
		import os
		import pickle
		from map.classes import world
		msg = ''
		for file in os.listdir("data/worlds/"):
			if file.endswith(".dt"):
				import pickle
				pfile = open('data/worlds/' + str(file), 'rb')
				wld = pickle.Unpickler(pfile).load()
				msg = msg + str(wld.name) + ': '
				msg = msg + str(len(wld.players)) + ' player(s)'
				pfile.close()
		return msg

	def getIDofPos(self, coords, world_name):
		import numpy as np
		mmap_ids = self.getWorldBIDs(world_name)
		return (mmap_ids[coords[1], coords[0]])[0]

	def getBiomeByID(self, bid, world_name):
		from map.classes import biome
		world_map = self.getWorldMap(world_name)
		return world_map[int(bid)]

	def updateBiomeByID(self, bid, world_name, updated_biome):
		from map.classes import biome
		world_map = self.getWorldMap(world_name)
		world_map[int(bid)] = updated_biome
		self.setWorld(world_map, -1, -1, world_name)
		return

	def resetBiomes(self, world_name):
		world = self.getWorldMap(world_name)
		for i in range(0, len(world)):
			world[i].resources = -1
		self.setWorld(world, -1, -1, world_name)



