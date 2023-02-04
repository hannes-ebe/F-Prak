import numpy as np
import matplotlib.pyplot as plt
import os

print("initialize calculation")
Q0=0
I0=0
omega=1
U_pp=2
L=1
R=100
np.savetxt("start.txt",[Q0,I0])
print("Start calculation")
os.system("ifort runge.f90 -O -o runge-fortran.sh")
os.system("./runge-fortran.sh")
print("finished")

t=np.loadtxt("result_time.txt")
Q=np.loadtxt("result_Q.txt")
I=np.loadtxt("result_I.txt")
Q_ref=[t for t in t]
plt.plot(t,Q,label="numerik")
plt.plot(t,I,label="numerik")
#plt.plot(t,Q_ref,label="Theorie")
plt.legend()
plt.show()