def gen_rivers(input_array):
	import cv2
	import numpy as np
	from scipy import signal
	import random
	import matplotlib.pyplot as plt

	hmap = input_array #0-1
	n = 10
	maxes = []
	rivers = np.empty([1024, 1024])

	trhmap = np.transpose(hmap)
	realcoordrow = []
	realcoordcol = []

	def river(start):

		x = start[0] #col
		y = start[1] #row
		values = []
		path = []
		i = 0

		while ((hmap[y][x] > 0.5) and (i < 10)):
			i = i+1

			if ((0 < x < 1023) and (0 < y < 1023)):
				neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]

				for i in range(len(neighbors)):
					values.append(hmap[neighbors[i][1]][neighbors[i][0]] - hmap[y][x])

				path.append(neighbors[np.argmin(values)])
				x = neighbors[np.argmin(values)][0]
				y = neighbors[np.argmin(values)][1]
				hmap[y][x] = hmap[y][x]+0.005
				values = []

		return path

	for row in range(len(hmap)):
		#print("iteration row " + str(row) + " out of 1024, " + str(round(row/1024*1000)/10) + "%" + " done.")

		peakinrow = signal.find_peaks(hmap[row], height=0.65, distance=1, prominence=0.06, wlen=1000) #finds peaks in rows

		for i in range(len(peakinrow[0])):
			realcoordrow.append([row, peakinrow[0][i]]) #[row, colomn]

			for j in range(len(realcoordrow)): # iterate for each peak in row

				peakincol = signal.find_peaks(trhmap[realcoordrow[j][1]], height=0.65, distance=1, prominence=0.06, wlen=1000)
				# check if peak in row is a peak in col also
				for k in range(len(peakincol[0])): # for peaks in rows which are also peaks in cols
					realcoordcol.append([1023-peakincol[0][k], realcoordrow[j][0]])

				for r in range(len(realcoordrow)):

					if realcoordrow[r] in realcoordcol:
						maxes.append(realcoordrow[r])
						realcoordrow.pop(realcoordrow.index(realcoordrow[r]))

					else:
						realcoordrow.pop(realcoordrow.index(realcoordrow[r]))
	for row in range(len(hmap)):
		##print("iteration row " + str(row) + " out of 1024, " + str(round(row/1024*1000)/10) + "%" + " done.")

		peakinrow = signal.find_peaks(hmap[row], height=0.7, distance=1, prominence=0.08, wlen=1000) #finds peaks in rows

		for i in range(len(peakinrow[0])):
			realcoordrow.append([row, peakinrow[0][i]]) #[row, colomn]

			for j in range(len(realcoordrow)): # iterate for each peak in row

				peakincol = signal.find_peaks(trhmap[realcoordrow[j][1]], height=0.7, distance=1, prominence=0.08, wlen=1000)
				# check if peak in row is a peak in col also
				for k in range(len(peakincol[0])): # for peaks in rows which are also peaks in cols
					realcoordcol.append([1023-peakincol[0][k], realcoordrow[j][0]])

				for r in range(len(realcoordrow)):

					if realcoordrow[r] in realcoordcol:
						maxes.append(realcoordrow[r])
						realcoordrow.pop(realcoordrow.index(realcoordrow[r]))

					else:
						realcoordrow.pop(realcoordrow.index(realcoordrow[r]))


	for i in range(len(maxes)):

		#print("iteration path " + str(i) + " out of " +str(len(maxes))+ ", " + str(round(i/len(maxes)*1000)/10) + "%" + " done.")
		location = maxes[i]
		startrow = location[0]
		startcol = location[1]

		start = (location[1], location[0])
		path = river(start)
		
		for i in range(len(path)):
			rivers[path[i][1]][path[i][0]] = 1
	return rivers