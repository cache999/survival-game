#NEW CONFIG FORMAT:
'''
11: [
	{info:['Wood', 1, 1, -1],
	weight: 100}
	}
	]
'''
def generateResources(player_biome):
	import numpy as np
	from map.classes import biome
	import configparser
	import math
	import json
	import copy
	'''
	Generates the resources the biome should have. Only use
	when someone initially does !gather in the biome.
	Input: map.classes.biome object
	Output: map.classes.biome object including resources
	'''
	biome_size = player_biome.coords.shape[0]
	#with open(r"map/biome_resources.json") as biomes:
	#	biome_resources = json.load(biomes)[str(player_biome.type)]
	#weights = np.concatenate(list(map(lambda x: np.broadcast_to(x['info'], (x['weight'], 4)), biome_resources)), axis=0)
	with open(r"map/biome_resources.json") as biomes:
		biome_resources = json.load(biomes)[str(player_biome.type)]
	player_biome.resources_max = np.array(list(map(lambda x: x['max'] * biome_size, biome_resources)))
	player_biome.resources = copy.copy(player_biome.resources_max)

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
	'''
	return player_biome

def calculateLoot(player_biome, time, equipment, inventory):
	import numpy as np
	from map.classes import biome
	import configparser
	import json
	import random
	from items.item_classes import Item, Container
	'''
	Returns the amount of loot a player would get by
	gathering resources in the biome in a give time.
	Input: Time taken in minutes, map.classes.biome object
	gg actually good code
	'''
	chances = player_biome.resources / player_biome.resources_max
	with open(r"map/biome_resources.json") as biomes:
		biome_resources = json.load(biomes)[str(player_biome.type)]
	weights = np.array(list(map(lambda x: x['weight'], biome_resources)))
	weights = weights/weights.sum(0)
	infos = np.array(list(map(lambda x: x['info'], biome_resources)))
	loot = np.zeros(weights.shape[0])
	time_taken = -1
	for i in range(0, int(time)):
		choice = np.random.choice(np.arange(infos.shape[0]), p=weights)
		if (1 if random.random() < chances[choice] else 0): #successfully found an item
			#append to inven
			player_biome.resources[choice] -= 1
			chances[choice] = player_biome.resources[choice] / player_biome.resources_max[choice]
			iteminfo = infos[choice].tolist()
			if (iteminfo[0] != None):
				if (type(iteminfo[3]) != dict):
					iteminfo[3] = int(iteminfo[3])
				add = inventory + Item(iteminfo[0],iteminfo[1],iteminfo[2],iteminfo[3])
				if (type(add) != int):
					time_taken = i
					break
				else:
					loot[choice] += 1
	return time_taken, inventory, player_biome
	

if __name__ == "__main__":
	from map.classes import biome
	from items.item_classes import Item, Container
	import numpy as np
	inv = Container('inventory', 15)
	b = biome(11)
	b.coords = np.zeros((10, 2))
	b = generateResources(b)
	calculateLoot(b, 1440, 'damascus blade', inv)
		
