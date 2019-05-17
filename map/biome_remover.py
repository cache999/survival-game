#removes small biomes from a biome list
i_row = [-1,-1,-1,1,1,1,0,0]
i_col = [-1,1,0,-1,1,0,-1,1]
import numpy as np
import random
def rm_small_biomes(b_list, tagged_data):
	cfg = get_config()
	original = len(b_list)
	for i in range(len(b_list)):
		if (len(b_list[i].coords) < cfg[b_list[i].type]):
			#change type of biome
			adj_list = find_adj(b_list[i], tagged_data, i)
			rnd_biome = random.choice(adj_list)
			b_list[rnd_biome].coords = np.concatenate((b_list[rnd_biome].coords, b_list[i].coords))
			b_list[i].type = 0
			tagged_data[tagged_data==i] = rnd_biome

	#delete all flagged
	mask = np.ones(len(b_list), dtype=bool)
	for i in range(0, len(b_list)):
		if (b_list[i].type == 0):
			mask[i] = False
	b_list = b_list[mask]
	print(str(original - len(b_list)) + ' biomes yeeted out of existence')

	return b_list


def get_config():
	import configparser
	config = configparser.ConfigParser()
	config.readfp(open(r'map/biomes.cfg'))
	cfg = [0]
	cfg.append(int(config.get('min_size', 'deep_ocean_min')))
	cfg.append(int(config.get('min_size', 'shallow_ocean_min')))
	cfg.append(int(config.get('min_size', 'coral_reef_min')))
	cfg.append(int(config.get('min_size', 'kelp_forest_min')))
	cfg.append(int(config.get('min_size', 'ice_min')))
	cfg.append(int(config.get('min_size', 'tiaga_min')))
	cfg.append(int(config.get('min_size', 'tundra_min')))
	cfg.append(int(config.get('min_size', 'sand_beach_min')))
	cfg.append(int(config.get('min_size', 'steppe_min')))
	cfg.append(int(config.get('min_size', 'plains_min')))
	cfg.append(int(config.get('min_size', 'forest_min')))
	cfg.append(int(config.get('min_size', 'swamp_min')))
	cfg.append(int(config.get('min_size', 'desert_min')))
	cfg.append(int(config.get('min_size', 'savanna_min')))
	cfg.append(int(config.get('min_size', 'rainforest_min')))
	cfg.append(int(config.get('min_size', 'mountain_min')))
	cfg.append(int(config.get('min_size', 'mountain_min')))
	cfg.append(int(config.get('min_size', 'river_min')))
	return cfg

def find_adj(b, r, b_index):
	global i_row, i_col
	adj_list = []
	#r is tagged_data
	#input: a biome object
	#output: a list of adjacent biomes
	for i in range(0, len(b.coords)):
		for j in range(0, len(i_row)):
			#use tagged_data
			if((b.coords[i][0] + i_row[j]) >= 0 and (b.coords[i][0] + i_row[j]) <= r.shape[0] - 1 and (b.coords[i][1] + i_col[j]) >= 0 and (b.coords[i][1] + i_col[j]) <= r.shape[1] - 1):
				t = r[b.coords[i][0] + i_row[j], b.coords[i][1] + i_col[j]]
				if (t != b_index):
					adj_list.append(t)
	return adj_list




