import numpy as np
f = np.array([[0, 3],[1,5]]).T
g = np.zeros((10, 10))
g[f[0], f[1]] = 1
print(g)
