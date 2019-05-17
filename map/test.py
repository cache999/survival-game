import numpy as np
f = np.array([0,1,2,2,3,4,5])
f[f==2]=3
print(f.tolist())