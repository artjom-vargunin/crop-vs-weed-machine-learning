import os
from skimage import io
import numpy as np
import pandas as pd

from skimage.filters import threshold_triangle
from skimage.measure import regionprops,label


import matplotlib.pyplot as plt

def EXG(RED,GREEN,BLUE):
    return GREEN+RED+BLUE

def density_around(labels,label,d):
    props=regionprops(labels)
    x0=props[label]['centroid'][1]#x coord of label centroid  
    y0=props[label]['centroid'][0]#y coord of label centroid
    x0_0=0
    if (x0>d)&(labels.shape[1]-x0>d):
        x0_0=x0-np.random.uniform(low=0,high=d,size=1)[0]# x0-random_shift...x0-random_shift+d
    elif x0<=d:
        x0_0=np.random.uniform(low=0,high=x0,size=1)[0]
    else: #labels.shape[1]-x0<=d
        x0_0=np.random.uniform(low=x0,high=labels.shape[1],size=1)[0]-d
    y0_0=0
    if (y0>d)&(labels.shape[0]-y0>d):
        y0_0=y0-np.random.uniform(low=0,high=d,size=1)[0]# y0-random_shift...y0-random_shift+d
    elif y0<=d:
        y0_0=np.random.uniform(low=0,high=y0,size=1)[0]
    else: #labels.shape[0]-y0<=d
        y0_0=np.random.uniform(low=y0,high=labels.shape[0],size=1)[0]-d
    density=0
    area=0
    for i in range(labels.max()):
        if (props[i]['centroid'][1]>=x0_0)&(props[i]['centroid'][1]<=x0_0+d)&(props[i]['centroid'][0]>=y0_0)&(props[i]['centroid'][0]<=y0_0+d):
                density=density+1
                area=area+props[i]['area']
    return (density,area/d**2)


cwd = os.getcwd()
df = pd.DataFrame(columns=['area','perimeter','inertia11','inertia12','inertia21','inertia22','x','y','density_around','area_around','N','NW','img'])

image_number=-1
for filename in os.listdir(cwd):
	if filename.endswith(".tif"):
		print('processing '+filename,end='\r',flush=True)
		image_number=image_number+1
		image = io.imread(filename)
		TR,TG,TB,TNIR,TRE=[image[:,:,i] for i in range(5)]
		mexg=EXG(-0.884*TR,1.262*TG,-0.311*TB)
		tr_mexg= mexg > threshold_triangle(mexg)
		labels = label(tr_mexg)
		props=regionprops(labels)
		for lab in range(labels.max()):
			df = df.append({
    				'area': props[lab]['area'],
    				'perimeter': props[lab]['perimeter'],
    				'inertia11': props[lab]['inertia_tensor'][0,0],
    				'inertia12': props[lab]['inertia_tensor'][0,1],
    				'inertia21': props[lab]['inertia_tensor'][1,0],
    				'inertia22': props[lab]['inertia_tensor'][1,1],
    				'x': props[lab]['centroid'][1],
    				'y': props[lab]['centroid'][0],
    				'density_around': density_around(labels,lab,50)[0],
    				'area_around': density_around(labels,lab,50)[1],
    				'N': int(filename.split('_N')[2].split('_')[0]),
    				'NW': int(filename.split('_N')[1].split('W')[1]),
				'img': image_number
      			}, ignore_index=True)

df.to_csv('data.csv', index=False)  
