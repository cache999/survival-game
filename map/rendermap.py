import numpy as np
import matplotlib.pyplot as plt
import math
from classes import tile, biome

def get_biome_type(h, p, t, r):
    #recieves h, t, m, r, returns biome ID 

    if (h < 0 and t < -0.5):
        return tile(5) #ice
    if (h < -0.3):
        return tile(1) #deep sea
    if (h < -0.1):
        return tile(2) #shallow ocean
    if (h < 0):#very shallow ocean
        if (t < 0.3):
            return tile(2)
        if (t < 0.7):
            if (r < 0):
                return tile(2)# ocean
            else:
                return tile(4) #kelp forest
        else:
            if (r < 0.4):
                return tile(2) # ocean
            else:
                return tile(3) #coral reef
    if (h < 0.1):
        if (t < -0.5):
            return tile(5) # icy beach - ice
        return tile(8) #beach - do gravel beach later
    if (h < 0.5): #main shit
        if (t < -0.2): #cold
            if (p < -0.2):
                return tile(7) #tundra
            else:
                return tile(6) #tiaga
        elif (t < 0.6): #moderate temp
            if (p < -0.5):
                return tile(9) #steppe
            if (p < 0.65):
                if (r < 0):
                    return tile(10) #plains
                else:
                    return tile(11) #forest
            else:
                return tile(12) #swamp
        else: #high temp
            if (p < -0.7):
                return tile(13) #desert
            if (p < -0.1):
                return tile(14) #savannah
            else:
                return tile(15) #rainforest
    else:
        if (t < -0.5):
            return tile(17) # snowy mountain
        return tile(16) #mountain

def display(biomelist):
    data = np.zeros((1024, 1024, 3), dtype=int)
    id_colours = [
    [153, 235, 255],
    [0, 163, 204],
    [0, 184, 230],
    [255, 102, 204],
    [0, 76, 59],
    [153, 229, 253],
    [98, 247, 210],
    [223, 102, 102],
    [255, 255, 153],
    [187, 168, 23],
    [173, 235, 173],
    [0, 102, 0],
    [50, 51, 1],
    [238, 175, 106],
    [182, 204, 12],
    [70, 169, 56],
    [77, 77, 77],
    [230, 255, 255],
    ]
    for i in range(0, len(biomelist)):
        for j in range(0, len(biomelist[i].coords)):
            data[biomelist[i].coords[j][0], biomelist[i].coords[j][1]] = id_colours[biomelist[i].type]
    fig = plt.figure()
    fig.set_size_inches((1,1))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, aspect='equal')
    plt.savefig('map.png', dpi=4096, vmin=0,vmax=255)

def append_rivers(data, rivers):
    c = 0
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            if (rivers[i, j] != 0):
                c += 1
                data[i, j] = tile(0)
    print(str(c) + ' river tiles added to map')
    return data
#function to call to generate map, height, moisture, temperature, and random should
#all be 1024x1024 arrays of perlin noise
def generate_map(height, moisture, temperature, random, name, seed='random'):
    import matplotlib.pyplot as plt
    if (seed != 'random'):
        np.random.seed(seed)
    
    data = np.empty(shape=(height.shape[0], height.shape[1]), dtype=object)
    for i in range(0, height.shape[0]):
        temp_sin = (math.sin(i / (1024 / math.pi)) * 1.5) - 0.75
        for j in range(0, height.shape[1]):
            data[i, j] =  get_biome_type(height[i, j], moisture[i, j], (temp_sin + (temperature[i,j] * 0.25)), random[i,j])
    #generate rivers
    print('building terrain... done')
    from waterbodies import gen_rivers
    
    positive_height = (height - np.min(height))/np.ptp(height)
    rivers = gen_rivers(positive_height)
    print('creating rivers... done')
    #append rivers
    data = append_rivers(data, rivers)
    print('adding rivers to map... done')
    #make into biome list
    from biome_finder import parse_into_biomelist
    biome_list = parse_into_biomelist(data)
    print('parsing map data... done')
    #display using biome list
    print('displaying map...')
    display(biome_list)



