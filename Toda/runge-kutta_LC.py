import numpy as np
import matplotlib.pyplot as plt
import os
class calculation:
    def __init__(self,omega_f=1):
        print("initialize calculation")
        U_pp=750*1e-3
        L=64*1e-3
        R=1e3
        U_S=-0.3
        C0=100*1e-12
        omega=omega_f*2*np.pi*55*1e3#np.sqrt(L*C0)#1.2
        #print(1/np.sqrt(L*C0),omega)
        np.savetxt("calculation_directory/input/schwingkreis.txt",[U_pp,L,R,U_S,C0,omega])
        Q0=0
        I0=0
        np.savetxt("calculation_directory/input/start.txt",[Q0,I0])
        dt=10**(-7)
        dir_name=str(omega_f)
    def __call__(self):
        os.chdir("calculation_directory/")
        os.system("ifort runge_LC.f90 -O -o runge-fortran.sh")
        # os.system("./runge-fortran.sh")
        torig = np.loadtxt("output/result_time.txt")
        self.t = torig#[int(len(torig) / 2):]
        self.Q = np.loadtxt("output/result_Q.txt")#[int(len(torig) / 2):]
        self.I = np.loadtxt("output/result_I.txt")#[int(len(torig) / 2):]
        self.phi=np.loadtxt("output/result_phi.txt")#[int(len(torig)/2):]
        os.chdir("../")
def main():
    for omega_f in [1]:
        calc=calculation(omega_f=1)
        calc()
        # plt.plot(calc.Q, calc.I,label=omega_f)
        #
        # ax = plt.figure().add_subplot(projection='3d')
        # ax.plot(calc.Q,calc.I,calc.t, label='parametric curve')
        plt.plot(calc.t,calc.Q,label="Ladung")
        plt.plot(calc.t,calc.I*1000,label="Strom")
    plt.legend()
    plt.show()

if __name__=="__main__":
    main()