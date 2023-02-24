import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
class calculation:
    def __init__(self,U_pp=400*1e-3,calculate=True):
        print("initialize calculation")
        L=64*1e-3
        R=1e3
        U_S=-0.3
        C0=100*1e-12
        omega=2*np.pi*55*1e3
        np.savetxt("calculation_directory/input/schwingkreis.txt",[U_pp,L,R,U_S,C0,omega])
        Q0=0
        I0=0
        np.savetxt("calculation_directory/input/start.txt",[Q0,I0])
        dt=10**(-9)
        dir_name="a"
        np.savetxt("calculation_directory/input/simu.txt", [dt])
        self.calculate=calculate
    def __call__(self):
        os.chdir("calculation_directory/")
        if self.calculate:
            os.system("ifort runge.f90 -O -o runge-fortran.sh")
            os.system("./runge-fortran.sh")
        torig = np.loadtxt("output/result_time.txt")
        self.t = torig#[int(len(torig)/2):]
        self.Q = np.loadtxt("output/result_Q.txt")#[int(len(torig)/2):]
        self.I = np.loadtxt("output/result_I.txt")#[int(len(torig)/2):]
        self.phi=np.loadtxt("output/result_phi.txt")#[int(len(torig)/2):]
        os.chdir("../")

    def get_data(self):
        os.chdir("calculation_directory/")
        torig = np.loadtxt("output/result_time.txt")
        self.t = torig[int(len(torig)/2):]
        self.Q = np.loadtxt("output/result_Q.txt")[int(len(torig)/2):]
        self.I = np.loadtxt("output/result_I.txt")[int(len(torig)/2):]
        self.phi = np.loadtxt("output/result_phi.txt")[int(len(torig)/2):]
        os.chdir("../")

    def poincare(self):
        check = True
        self.I_poin=[]
        self.phi_poin=[]
        self.t_poin=[]
        for i in range(len(self.I)-11):
            if np.mean(self.I[i:i+1])<np.mean(self.I[i+1:i+2]) and np.mean(self.I[i+1:i+2])>np.mean(self.I[i+2:i+3]):
                self.I_poin.append(self.I[i+1])
                self.t_poin.append(self.t[i+1])
                self.phi_poin.append(self.phi[i+1])



def main():
    bifur()


def plot():
    plot_3d = False
    plot_time = True
    plot_phase = True
    for U in [0.61]:
        calc = calculation(U)
        # calc()
        calc.get_data()
        calc.poincare()
        if plot_time:
            fig = plt.figure(figsize=(5, 5))
            gs = GridSpec(5, 5)
            fig1 = fig.add_subplot(gs[:5, :])
            fig1.set_ylabel("I in A")
            fig1.set_xlabel("t in s")
            # fig1.set_xlim(2.5e-5,2.52e-5)
            fig1.plot(calc.t, calc.I)
            fig1.plot(calc.t_poin, calc.I_poin, "o")
            plt.tight_layout()
            plt.savefig(f"plots/{int(U * 10)}_time_poin.pdf")
            plt.show()
        if plot_3d:
            ax = plt.figure().add_subplot(projection='3d')
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.plot(calc.Q, calc.I, calc.phi)
            plt.tight_layout()
            plt.show()
        if plot_phase:
            fig = plt.figure(figsize=(5, 5))
            gs = GridSpec(5, 5)
            fig1 = fig.add_subplot(gs[:5, :])
            fig1.set_ylabel("I in A")
            fig1.set_xlabel("$U_{in}}$ in V")
            fig1.plot(U / 2 * np.sin(calc.phi), calc.I)
            fig1.plot(U / 2 * np.sin(calc.phi_poin), calc.I_poin, "o")
            plt.tight_layout()
            plt.savefig(f"plots/{int(U * 10)}_phase_poin.pdf")
            plt.show()

def bifur():
    cal=False
    U_list=[0.005*i for i in range(1000)]
    I_poin_list=[]
    for i,U in enumerate(U_list):
        print(U)
        if cal:
            calc = calculation(U)
            calc()
            calc.get_data()
            calc.poincare()
            I_poin_list.append(calc.I_poin)
            np.savetxt(f"tmp/poin{U}.txt", I_poin_list[i])
        else:
            I_poin_list.append(np.loadtxt(f"tmp/poin{U}.txt"))
    fig = plt.figure(figsize=(20, 10))
    gs = GridSpec(5, 5)
    fig1 = fig.add_subplot(gs[:5, :])
    fig1.set_ylabel("I in A Poincare Schnitt")
    fig1.set_xlabel("$U_{pp}}$ in V")
    # fig1.set_xlim(0.8,2.5)
    # fig1.set_ylim(-0.0001, 0.00015)
    for i in range(len(U_list)):
        # print(i)
        fig1.plot([U_list[i] for j in I_poin_list[i]],I_poin_list[i],"o",color="blue")
        # fig1.plot([U_list[i] for j in plot_list], plot_list, "o", color="blue")
        #
    plt.tight_layout()
    plt.savefig(f"plots/bifur_zoom_full.pdf")
    plt.show()


if __name__=="__main__":
    main()