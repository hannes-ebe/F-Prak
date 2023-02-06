import numpy as np
import matplotlib.pyplot as plt
import os

print("initialize calculation")
U_pp=40*10e-3
L=65*1e-3
R=1e3
U_S=-0.3
C0=100*1e-6
omega=1.2*2*np.pi*55*10e3
np.savetxt("calculation_directory/input/schwingkreis.txt",[U_pp,L,R,U_S,C0,omega])
Q0=0
I0=0.5*U_pp/R
np.savetxt("calculation_directory/input/start.txt",[Q0,I0])

print("Start calculation")
os.chdir("calculation_directory/")
os.system("ifort runge_LC.f90 -O -o runge-fortran.sh")
os.system("./runge-fortran.sh")
print("finished")

torig=np.loadtxt("output/result_time.txt")
t=torig[int(3*len(torig)/4):]
Q=np.loadtxt("output/result_Q.txt")[int(3*len(torig)/4):]
I=np.loadtxt("output/result_I.txt")[int(3*len(torig)/4):]
phi=np.loadtxt("output/result_phi.txt")[int(3*len(torig)/4):]

# plt.plot(t,Q,label="Ladung")
# plt.plot(t,I*1000,label="Strom")
plt.plot(Q,I)
# plt
# .plot(t,I/1000,label="Spannung")
# plt.plot(t,max(I/1000)*np.sin(phi),label="Antreiber")
# plt.plot(t,phi,label="Strom")
#plt.plot(t,Q_ref,label="Theorie")
plt.legend()
plt.show()