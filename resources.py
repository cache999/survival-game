def generateResources(player_biome):
	import numpy as np
	from map.classes import biome
	import configparser
	import math
	'''
	Generates the resources the biome should have. Only use
	when someone initially does !gather in the biome.
	Input: map.classes.biome object
	Output: map.classes.biome object including
	resources: np.ndarray:
	[
	[1, 2, 3], (item ids)
	[69, 4, 1], (cap)
	[50, 2, 1] (current available items)
	]
	'''
	biome_size = player_biome.coords.shape[0]
	config = configparser.ConfigParser()
	config.readfp(open(r"map/biomes.cfg"))
	max_resources = config.get('res_max', str(player_biome.type))
	max_resources = max_resources.split(',')
	player_biome.resources = np.zeros((3, len(max_resources)))
	for i in range(0, len(max_resources)):
		max_resources[i] = max_resources[i].split(':')
		player_biome.resources[0, i] = float(max_resources[i][0])
		player_biome.resources[1, i] = math.ceil(float(max_resources[i][1]) * biome_size)
		player_biome.resources[2, i] = math.ceil(float(max_resources[i][1]) * biome_size)
	return player_biome

def calculateLoot(player_biome, time, equipment):
	import numpy as np
	from map.classes import biome
	import configparser
	'''
	Returns the amount of loot a player would get by
	gathering resources in the biome in a give time.
	Input: Time taken in minutes, map.classes.biome object
	Output: np.ndarray displaying loot:
	[[type,count], [type,count]]
	'''
	config = configparser.ConfigParser()
	config.readfp(open(r"map/biomes.cfg"))
	cfg_weights = config.get('res_search', str(player_biome.type)).split(',')
	weights = np.zeros((3, len(cfg_weights)), dtype=float)
	
	#print(player_biome.resources)

	for i in range(0, len(cfg_weights)):
		w = cfg_weights[i].split(':')
		if (w[3] == equipment or w[3] == 'none'):
			weights[0][i] = w[0]
			weights[1][i] = w[1]
			weights[2][i] = w[2]
	weights[1] /= np.sum(weights[1])
	loot = np.zeros(weights.shape[1])
	for i in range(0, int(time)):
		loot_iter = np.random.multinomial(1, weights[1]) * weights[2] * player_biome.resources[2] / player_biome.resources[1]
		player_biome.resources[2] -= loot_iter
		loot += loot_iter
	player_biome.resources[2] = np.floor(player_biome.resources[2])
	return np.array([weights[0], np.floor(loot)]).T, player_biome



