import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import OrderedDict

def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3
    
    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:  ,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:  ].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:  ,1:  ].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]  )) * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]  )) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)
        
def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (frequency*res[0], frequency*res[1]))
        frequency *= 2
        amplitude *= persistence
    return noise
    


    #arr = np.load('array.npy', mmap_mode='r')



def make_image(data, outputname, size=(1, 1), dpi=4096):
    import matplotlib.pyplot as plt
    snow = cm.get_cmap('gray', 1)
    tundra = cm.get_cmap('Reds', 128)
    forest = cm.get_cmap('Greens', 128)
    grassland = cm.get_cmap('Greens', 128)
    sand = cm.get_cmap('Oranges', 128)
    water = cm.get_cmap('Blues', 128)

    mapcolors = np.vstack((snow(np.linspace(0, 1, 30)),
                        tundra(np.linspace(0, 0.2, 20)),
                        forest(np.linspace(0.5, 0.4, 34)),
                        grassland(np.linspace(0.3, 0.1, 26)),
                        sand(np.linspace(0, 0.1, 16)),
                        water(np.linspace(0.2, 0.3, 0))))


    mapcmp = ListedColormap(mapcolors, name='map')

    bottom = cm.get_cmap('gray', 1)
    top = cm.get_cmap('gray', 255)
    colors = np.vstack((top(np.linspace(0, 1, 116)),
                        bottom(np.linspace(0, 1, 140))))
    grays = ListedColormap(colors, name='grays')

    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, aspect='equal', cmap = mapcmp)
    plt.savefig(outputname, dpi=dpi)

    ax.imshow(data, aspect='equal', cmap = grays)
    plt.savefig('gray.png', dpi=dpi)


def generate_map(size, seed='random'):
    import matplotlib.pyplot as plt
    if (seed != 'random'):
        np.random.seed(seed)

    terrain = generate_fractal_noise_2d((size, size), (8, 8), 8)
    moisture = generate_fractal_noise_2d((size, size), (8, 8), 8)


    import json

    wld = open("/Users/student/desktop/map/map_1.txt", 'w')
    wld.write(json.dumps(terrain.tolist()))
    make_image(terrain, 'map.png')
generate_map(1024)
