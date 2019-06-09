#stuff that would clutter up the main script
def find_endpoint(string, mag, start_coords):
	import re
	import numpy as np
	import math
	#find endpoint of the vector
	n = np.array([0, len(re.findall('n', string))])
	e = np.array([len(re.findall('e', string)), 0])
	s = np.array([0, -1 * len(re.findall('s', string))])
	w = np.array([-1 * len(re.findall('w', string)), 0])
	vector = (n+e+s+w).tolist()
	multiplier = mag/math.sqrt(vector[0]**2 + vector[1]**2)
	vector[0] *= multiplier
	vector[1] *= multiplier
	final = [int(start_coords[0] + vector[0]), int(start_coords[1] + vector[1])]
	if (final[0]<0 or final[0] > 1023 or final[1]<0 or final[1] > 1023):
		return -1
	return final

def find_uncovered(start, end):
	import skimage as sk
	import numpy as np
	a, b = sk.draw.line(start[0], start[1], end[0], end[1])
	return np.vstack((a, b)).T

