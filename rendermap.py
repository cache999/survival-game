import cv2
import numpy as np

global p
a = cv2.imread('map.png',0);
[ty,tx] = a.shape;
o = np.zeros((ty+2,tx+2),dtype=np.int)
o[1:ty+1,1:tx+1] = (255 -a);
c = np.asarray(o);
p = np.count_nonzero(c)
[ay , ax] = c.shape;
z = np.zeros(c.shape, dtype=np.int)

def startTrace(yt,xt):
    global p
    cv2.imshow('image',z);
    z[yt,xt] = 255;
    c[yt,xt] =0;
    p = np.count_nonzero(c)
    if((yt < ay-1) and (xt < ax -1)): 
        if (c[yt, xt+1] > 0):
            startTrace(yt,xt+1)
        elif (c[yt+1,xt+1] > 0):
            startTrace(yt+1,xt+1)
        elif (c[yt+1,xt] > 0):
            startTrace(yt+1,xt)
        elif (c[yt+1,xt-1] >0) :
            startTrace(yt+1,xt-1)
        elif (c[yt,xt-1] >0):
            startTrace(yt,xt-1)
        elif (c[yt-1,xt-1] > 0):
            startTrace(yt-1,xt-1)
        elif (c[yt-1,xt] > 0):
            startTrace(yt-1,xt)
        elif (c[yt-1,xt+1] > 0):
            startTrace(yt-1,xt+1)


while (p > 0):
    for y in range(1,ay-2):
        for x in range(1,ax-2):
            if (c[y,x] > 0) :
                startTrace(y,x);