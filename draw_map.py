def draw_pos(chat_id, coords, world_name):

	import numpy as np
	import cv2

	x = coords[0]
	y = 1023-coords[1]
	vrange = 20

	bounds = [[x+vrange, y+vrange],[x-vrange, y-vrange]]

	path = "data/worlds/" + world_name + ".png"
	world = np.full((1124, 1124, 3), [255, 255, 255])
	world[50:1074,50:1074] = cv2.imread(path, 1)

	pos_map = world[50+bounds[1][1]:50+bounds[0][1]+1, 50+bounds[1][0]:50+bounds[0][0]+1]
	pos_map[vrange][vrange] = [0, 0, 255]


	pos_map = cv2.resize(pos_map,(200, 200),fx=0, fy=0, interpolation = cv2.INTER_NEAREST)

	cv2.imwrite('data/players/' + str(chat_id) + '.png', pos_map)
	#cv2.imwrite('data/worlds/shit.png', world)
	return

def draw_map(chat_id, explored, world_name):
	import numpy as np
	import cv2
	import PIL
	from PIL import ImageEnhance, Image
	backgroundcolor = [210, 240, 250]
	vrange = 20
	total = cv2.imread("data/worlds/" + world_name + ".png", 1)

	world = np.full((1124, 1124, 3), backgroundcolor)
	world[50:1074,50:1074] = total

	visible = np.zeros((1124, 1124))
	totalmap = np.full((1124, 1124, 3), backgroundcolor)

	for i in range(len(explored)):

		x = explored[i][0] + 50
		y = 1023-explored[i][1] + 50

		visible[y-vrange:y+vrange, x-vrange:x+vrange] = 1

	for i in range(len(visible)):
		for j in range(len(visible)):
			if visible[i][j] == 1:
				totalmap[i][j] = world[i][j]

	poi = np.transpose(np.nonzero(visible))

	rows = []
	cols = []

	for i in range(len(poi)):
		rows.append(poi[i][0])
		cols.append(poi[i][1])

	hrow = max(rows)
	lrow = min(rows)
	hcol = max(cols)
	lcol = min(cols)

	im = Image.fromarray(totalmap[lrow:hrow, lcol:hcol].astype('uint8'))
	im = PIL.ImageEnhance.Color(im).enhance(0.1)
	im = np.array(im)
	im = cv2.resize(im,(800, 800),fx=0, fy=0, interpolation = cv2.INTER_NEAREST)

	cv2.imwrite("data/players/" + str(chat_id) + ".png", im)
