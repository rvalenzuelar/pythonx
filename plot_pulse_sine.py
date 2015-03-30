import matplotlib.pyplot as plt
import numpy as np 
import math

pi=math.pi
t=np.linspace(0,8*pi,800)
a=np.linspace(0,0,200)
b=np.linspace(1,1,200)

# creates pulses or CW
A=np.concatenate([a,b,a,b])
#A=np.concatenate([b,b,b,b])

# frequency
f=4;

# wave
y=A*np.sin(f*t)


plt.plot(t,y, linewidth=4)

plt.show()