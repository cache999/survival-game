#removes small biomes from a biome list
i_row = [-1,-1,-1,1,1,1,0,0]
i_col = [-1,1,0,-1,1,0,-1,1]
import numpy as np
import random
def rm_small_biomes(b_list, raw_data):
	cfg = get_config()
	for i in range(len(b_list)):
		if (len(b_list[i].coords) < cfg[b_list[i].type]):
			#change type of biome
			adj_list = find_adj(b_list[i], raw_data)
			b_list[i].type = random.choice(adj_list)
	return b_list


def get_config():
	import configparser
	config = configparser.ConfigParser()
	config.readfp(open(r'biomes.cfg'))
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

def find_adj(b, r):
	global i_row, i_col
	adj_list = []
	#input: a biome object
	#output: a list of adjacent biomes
	for i in range(0, len(b.coords)):
		for j in range(0, len(i_row)):
			#use raw_data
			if((b.coords[i][0] + i_row[j]) >= 0 and (b.coords[i][0] + i_row[j]) <= r.shape[0] - 1 and (b.coords[i][1] + i_col[j]) >= 0 and (b.coords[i][1] + i_col[j]) <= r.shape[1] - 1):
				t = r[b.coords[i][0] + i_row[j], b.coords[i][1] + i_col[j]]
				if (t != b.type):
					adj_list.append(t)
	return adj_list