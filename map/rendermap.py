import numpy as np
import matplotlib.pyplot as plt
import math
from classes import biome

def get_biome_type(h, p, t, r):
    #recieves h, t, m, r, returns biome ID 

    if (h < 0 and t < -0.5):
        return 5 #ice
    if (h < -0.3):
        return 1 #deep sea
    if (h < -0.1):
        return 2 #shallow ocean
    if (h < 0):#very shallow ocean
        if (t < 0.3):
            return 2
        if (t < 0.7):
            if (r < 0):
                return 2# ocean
            else:
                return 4 #kelp forest
        else:
            if (r < 0.4):
                return 2 # ocean
            else:
                return 3 #coral reef
    if (h < 0.1):
        if (t < -0.5):
            return 5 # icy beach - ice
        return 8 #beach - do gravel beach later
    if (h < 0.5): #main shit
        if (t < -0.2): #cold
            if (p < -0.2):
                return 7 #tundra
            else:
                return 6 #tiaga
        elif (t < 0.6): #moderate temp
            if (p < -0.5):
                return 9 #steppe
            if (p < 0.65):
                if (r < 0):
                    return 10 #plains
                else:
                    return 11 #forest
            else:
                return 12 #swamp
        else: #high temp
            if (p < -0.7):
                return 13 #desert
            if (p < -0.1):
                return 14 #savannah
            else:
                return 15 #rainforest
    else:
        if (t < -0.5):
            return 17 # snowy mountain
        return 16 #mountain

def display(biomelist, filename):
    from classes import colours
    data = np.zeros((1024, 1024, 3), dtype=int)
    id_colours = colours()
    for i in range(0, len(biomelist)):
        for j in range(0, len(biomelist[i].coords)):
            data[biomelist[i].coords[j][0], biomelist[i].coords[j][1]] = id_colours[biomelist[i].type]
    fig = plt.figure()
    fig.set_size_inches((1,1))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, aspect='equal')
    plt.savefig(filename, dpi=1024, vmin=0,vmax=255)

def display_sequentially(biomelist):
    #debug
    from classes import colours
    id_colours = colours()
    for i in range(0, len(biomelist)):
        data = np.zeros((1024, 1024, 3), dtype=int)
        for j in range(0, len(biomelist[i].coords)):

            data[biomelist[i].coords[j][0], biomelist[i].coords[j][1]] = id_colours[biomelist[i].type]
        fig = plt.figure()
        fig.set_size_inches((1,1))
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(data, aspect='equal')
        plt.savefig('biome_' + str(i) + '.png', dpi=1024, vmin=0,vmax=255)

    


def append_rivers(data, rivers):
    c = 0
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            if (rivers[i, j] != 0):
                c += 1
                data[i, j] = 18
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
    from biome_finder import make_list
    biome_list = make_list(data)
    print('parsing map data... done')
    #delete small biomes

    from biome_remover import rm_small_biomes
    biome_list = rm_small_biomes(biome_list, data)
    print('removing small biomes... done')
    #display using biome list
    print('displaying map...')
    display(biome_list, 'map')



