import numpy as np
f = np.array([0, 1, 2])
g = np.array(['p', 'q', 'r'], dtype=str)

a = np.zeros((2, 3), dtype=object)
a[0], a[1] = np.array([f, g])
a = a.T
print(a)