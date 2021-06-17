import numpy as np
f = np.zeros((1024,1024,2))
print(f.shape)
f = np.delete(f, 0, axis=2)
f = np.squeeze(f)
print(f.shape)