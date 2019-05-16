from scipy.ndimage import label, generate_binary_structure
import numpy as np
#inefficient algo!
def make_list(data):
	s = generate_binary_structure(2,2)
	dlen = data.shape[0]
	from map.classes import colours, biome
	b_len = len(colours()) #0s are useless
	biome_list = np.array([])
	for b in range(1, b_len):
		d = np.array(data, copy=True)
		d[d != b] = 0
		d[d == b] = 1
		lb_data, num_features = label(d.tolist(), structure=s)
		b_array = np.empty(num_features, dtype=object)
		#add biome objects to num_features
		for i in range(1, num_features + 1):
			b_array[i-1] = biome(b)
			b_array[i-1].setc(np.argwhere(lb_data==i).tolist())
		biome_list = np.concatenate((biome_list, b_array))
		print('finished biome ' + str(b) + ' out of ' + str(b_len-1))
	return biome_list