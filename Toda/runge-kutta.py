import numpy as np
import matplotlib.pyplot as plt
import os
class calculation:
    def __init__(self,omega_f=1,U_pp=400*1e-3,calculate=True):
        print("initialize calculation")
        L=64*1e-3
        R=1e3
        U_S=-0.3
        C0=100*1e-12
        omega=omega_f*2*np.pi*55*1e3
        np.savetxt("calculation_directory/input/schwingkreis.txt",[U_pp,L,R,U_S,C0,omega])
        Q0=0
        I0=0
        np.savetxt("calculation_directory/input/start.txt",[Q0,I0])
        dt=10**(-10)
        dir_name="a"
        np.savetxt("calculation_directory/input/simu.txt", [dt])
        self.calculate=calculate
    def __call__(self):
        os.chdir("calculation_directory/")
        if self.calculate:
            os.system("ifort runge.f90 -O -o runge-fortran.sh")
            os.system("./runge-fortran.sh")
        torig = np.loadtxt("output/result_time.txt")
        self.t = torig[int(len(torig)/2):]
        self.Q = np.loadtxt("output/result_Q.txt")[int(len(torig)/2):]
        self.I = np.loadtxt("output/result_I.txt")[int(len(torig)/2):]
        self.phi=np.loadtxt("output/result_phi.txt")[int(len(torig)/2):]
        os.chdir("../")
def main():
    plot_3d=False
    for U in [i*10*1e-3 for i in [4,6,8,10,12,14,16]]:
        calc=calculation(U)
        calc()
        if plot_3d:
            ax = plt.figure().add_subplot(projection='3d')
            ax.plot(calc.Q,calc.I,calc.t, label='parametric curve')

        else:
            plt.plot(calc.Q, calc.I, label=U)
        plt.savefig(str(U) + ".pdf")
        # plt.plot(calc.t,calc.Q,label="Ladung")
        # plt.plot(calc.t,calc.I*1000,label="Strom")
    plt.legend()
    plt.savefig("gesamt.pdf")
    plt.show()

if __name__=="__main__":
    main()