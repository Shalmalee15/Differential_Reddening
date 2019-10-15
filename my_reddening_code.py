# This is a part of the program which removes the effect of the Differential Reddening from the main sequence of the masive star clusters. 
# Reference: A. Milone et al (2012)
# The steps: 1. Plot a CMD, 2. Rotate the main sequence using theta = A_Filter_1/(A_Filter_I - A_Filter_II); A = Absorption Coefficients (Ref. Jansen et al 1#994)

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import pandas as pd

# Read the data from the data file
my_data = np.loadtxt('cluster.dat')
x_data = my_data[:,2] # Separate the columns 
y_data = my_data[:,0] # Separate the columns
#print(x_data, y_data)
#print(x_data.shape, y_data.shape)
print("********* THIS IS CMD FOR NGC 1783 ************")
plt.figure()
plt.scatter(x_data, y_data, 0.3, 'black')
plt.xlim(0,3.0)
plt.ylim(18, 23)
plt.gca().invert_yaxis()
plt.xlabel("Colour")
plt.ylabel("Magnitude")
plt.title('CMD of NGC 1783')
# Choose an arbitrary point on CMD 
plt.show()

#Calculate the rotation angle 
# theta = np.radians(1.0928526307169) # theta = Af435w/(Af435w - Af814w); A = Absorption Coefficients (Ref. Jansen et al 1994)
theta = 1.1780330682095217
xcos = (x_data - 0.4) * np.cos(theta)  # old_x * cos(theta)
ycos = (y_data - 20) * np.cos(theta)  # old_y * cos(theta)
xsin = (x_data - 0.4) * np.sin(theta)  # old_x * sin(theta)
ysin = (y_data - 20) * np.sin(theta)  # old_y * sin(theta)

xx_data = xcos + ysin # Will store the new X_coordinates 
yy_data = -xsin + ycos # Will store the new Y_coordinates
print(xx_data, yy_data)

print("****************** THIS IS A TRIAL PLOT FOR DEREDDENING PROCESS ***************")
plt.figure()
plt.scatter(xx_data, yy_data, 0.3, 'red')
plt.xlim(-1,4)
plt.ylim(0,0.8)
plt.gca().invert_yaxis()
plt.xlabel("abscissa")
plt.ylabel("ordinate")
plt.title('Rotated CMD')
plt.show()

# Define a dataframe for x data and y data
df= pd.DataFrame({'x_data':xx_data,'y_data':yy_data})
# df1 will contain only those values which are in the range [X:-1 to 4] and [Y: 0 to 0.8]
df1 = df[(df['x_data']<=4.0) & (df['x_data']>= -1.0) & (df['y_data']<=0.8) & (df['y_data']>=0.0)]
#print(df1)
bins = np.linspace(0.0, 0.8, num=10) # These are number of bins
#print(bins)
# md will contain the x and y median points which will be calculated by the following iteration loop. 
md = pd.DataFrame(np.zeros(((len(bins)-1), 2)), columns=['x_med','y_med']) # Save the median points after the loop calculation.
#print(md)

# Iteration over the bins to get the median points for each y bins
for i in range(len(bins)-1):
    tempdf = df1[(df1['y_data'] >= bins[i]) & (df1['y_data'] <= bins[i+1]) ]
    x_median = np.median(tempdf['x_data'])
    y_median = np.median(tempdf['y_data'])
    md.iloc[i]=[x_median, y_median]
#print(md)
print("************* THIS IS FAMOUS FIDUCIAL LINE *****************")
plt.figure()
plt.plot(md['x_med'], md['y_med'], 'black')
plt.scatter(df1['x_data'], df1['y_data'], 0.3, zorder=0) # zorder= is used when you are lazy. 
plt.xlim(-1,4)
plt.ylim(0.0, 0.78)
plt.gca().invert_yaxis() # Again. When you are lazy, use this. Being lazy is good and easy. 
plt.title('Fiducial Line through the Main Sequence')
plt.show()
