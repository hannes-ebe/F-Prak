import numpy as np
import matplotlib.pyplot as plt
import os

print("initialize calculation")
Q0=1
I0=1
np.savetxt("start.txt",[Q0,I0])
U_pp=40*10e-3
L=65*1e-3
R=1e3
U_S=-0.3
C0=100*1e-12
omega=2*np.pi*55*10e3
np.savetxt("schwingkreis.txt",[U_pp,L,R,U_S,C0,omega])
print("Start calculation")
os.system("ifort runge.f90 -O -o runge-fortran.sh")
os.system("./runge-fortran.sh")
print("finished")

t=np.loadtxt("result_time.txt")
Q=np.loadtxt("result_Q.txt")
I=np.loadtxt("result_I.txt")
Q_ref=[t for t in t]
#plt.plot(t,Q,label="numerik")
plt.plot(t,I,label="numerik")
#plt.plot(t,Q_ref,label="Theorie")
plt.legend()
plt.show()