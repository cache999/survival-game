#[[],[],[],[]]

def draw_pos(chat_id, coords, world_name):
	#coords in this form [x, y]
	import cv2

	x = coords[0]
	y = 1023 - coords[1]
	vrange = 20

	bounds = [[x+vrange, y+vrange],[x-vrange, y-vrange]]
	
	if (x+vrange > 1023):
		bounds[0][0] = 1023

	if (x-vrange < 0):
		bounds[1][0] = 0

	if (y+vrange > 1023):
		bounds[0][1] = 1023

	if (y-vrange < 0):
		bounds[1][1] = 0

	path = "data/worlds/" + world_name + ".png"
	world = cv2.imread(path, 1)
	pos_map = world[bounds[1][1]:bounds[0][1]+1, bounds[1][0]:bounds[0][0]+1]
	pos_map[vrange][vrange] = [0, 0, 255]
	pos_map = cv2.resize(pos_map,(200, 200),fx=0, fy=0, interpolation = cv2.INTER_NEAREST)

	cv2.imwrite('data/players/' + str(chat_id) + '.png', pos_map)
	return


