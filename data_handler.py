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
		pickle.dump(data, pfile)
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
	def getPlayer(self, chat_id):
		import pickle
		return pickle.load(open('data/players/' + str(chat_id) + '.txt', 'rb'))

	def getWorld(self, world_name):
		pass

	#functions to check
	def isWorld(self, world_name):
		import os
		return os.path.isfile("data/worlds/" + str(world_name) + '.txt')

