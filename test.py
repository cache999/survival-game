import numpy as np
m = np.zeros((2, 3))
n = np.zeros((1, 3))
o = np.concatenate((m, n), axis=0)
print(o)