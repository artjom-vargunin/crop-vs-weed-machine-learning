import os
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

def EXG(RED,GREEN,BLUE):
    return GREEN+RED+BLUE

cwd = os.getcwd()
for filename in os.listdir(cwd):
	if filename.endswith(".tif"):
		image = io.imread(filename)
		TR,TG,TB,TNIR,TRE=[image[:,:,i] for i in range(5)]
		mexg=EXG(-0.884*TR,1.262*TG,-0.311*TB)
		plt.imsave('mexg_'+os.path.splitext(filename)[0]+'.jpg',arr=mexg,cmap='binary',vmin=np.min(mexg),vmax=np.max(mexg))