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

	def setWorld(self, data, info, world_name):
		import pickle
		if (not(type(data) is int)):
			pfile = open('data/worlds/' + str(world_name) + '.map','wb')
			pickle.dump(data, pfile)
			pfile.close()
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
		from main import char
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
		f = np.zeros((1024, 1024))
		f[coord_array[0], coord_array[1]]=0.3
		print(choice[0], choice[1])
		if (True):
			f[choice[0]+1, choice[1]+1]=1
			f[choice[0]+1, choice[1]-1]=1
			f[choice[0]+1, choice[1]]=1
			f[choice[0]-1, choice[1]+1]=1
			f[choice[0]-1, choice[1]-1]=1
			f[choice[0]-1, choice[1]]=1
			f[choice[0], choice[1]+1]=1
			f[choice[0], choice[1]-1]=1
			f[choice[0], choice[1]]=1


		fig = plt.figure()
		fig.set_size_inches((1,1))
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(f, aspect='equal', origin='lower')
		plt.savefig('valid_spawns.png', dpi=1024, vmin=0,vmax=255, origin='lower')
		coord_array = coord_array.tolist()
		coord_array.pop(0)
		
		return [choice[1], choice[0]]
		#get world
		'''
		print(coord_array.shape)
		coord_array = np.delete(coord_array, 0, axis=0)
		print(coord_array.shape)
		coord_array = coord_array.T
		print(coord_array.shape)
		choice = random.randint(0, coord_array.shape[1])
		#choice[1] = 1023 - choice[1]
		return [coord_array[0][choice], coord_array[1][choice]]
		#get world
		'''
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
