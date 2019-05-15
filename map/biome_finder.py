#NEW ALGO
'''
Iterate through the list
Try to find tiles adjacent that have the same type. If those tiles have a 
"uid" tag, that is added to the current tile too. If not, a new
uid tag is created (for a new biome).
'''

import numpy as np
from classes import tile, biome
tagged_data = -1
i_row = [-1,-1,-1,1,1,1,0,0]
i_col = [-1,1,0,-1,1,0,-1,1]
uid = 0
dlen = -1
b_list = []
def parse_into_biomelist(data):
	global tagged_data, dlen
	dlen = data.shape[0]
	tagged_data = data
	for i in range(0, dlen):
		for j in range(0, dlen):
			tagCheck([i, j])
	#testing - delete later
	cumulative_coords = 0
	return b_list
			

def tagCheck(coords):
	global uid, tagged_data, dlen
	i = coords[0]
	j = coords[1]
	for k in range(0, len(i_row)):
		if((i + i_row[k]) >= 0 and (i + i_row[k]) <= dlen - 1 and (j + i_col[k]) >= 0 and (j + i_col[k]) <= dlen - 1):
			if ((tagged_data[i, j].type == tagged_data[i + i_row[k], j + i_col[k]].type) and (tagged_data[i + i_row[k], j + i_col[k]].tag != -1)):
				#adjacent has tag - add to adjacent's tag
				tagged_data[i, j].addtag(tagged_data[i + i_row[k], j + i_col[k]].tag)
				b_list[tagged_data[i + i_row[k], j + i_col[k]].tag].addc([i, j])
				return
	#no adjacents with same type and a tag - make new biome
	tagged_data[i, j].addtag(uid)
	b_list.append(biome(tagged_data[i, j].type, [i, j]))
	uid += 1
	return
	