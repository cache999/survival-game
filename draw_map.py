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
