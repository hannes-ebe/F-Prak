#import necassary modules and choose mode for displaying plots
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from scipy.optimize import curve_fit
import pandas as pd
mpl.use("QT5Agg")
plt.rcParams['font.size']=15

class data_class:
    def __init__(self,const):
        data=pd.read_csv(f"data/zeit_alt/time_{const}.csv")
        self.data=data[["CH1_x","CH1_y","CH2_x","CH2_y"]]
        #print(self.data.head)
        self.Fit=False
        for i in range(len(self.data["CH2_y"]) - 3):
            if np.max(np.abs(self.data["CH2_y"])[i:i + 3]) < 0.1:
                self.trigger = i
                break
    def fit(self):
        fit_f = lambda x,A,lam,dt,c: A*np.exp(lam*(x+dt))+c
        popt,pcov = curve_fit(fit_f,self.data["CH1_x"][self.trigger:],self.data["CH1_y"][self.trigger:],\
                              p0=[np.max(self.data["CH1_y"][self.trigger:])-np.min(self.data["CH1_y"][self.trigger:]),-10,-self.data["CH1_x"][self.trigger],np.min(self.data["CH1_y"][self.trigger:])],\
                              maxfev=10**9,bounds=((0.1,-np.inf,-1,0),(np.inf,0,0,10)))
        self.fit_exp = lambda x: fit_f(x, popt[0], popt[1], popt[2], popt[3])
        self.lam=popt[1]
        self.Dlam=np.sqrt(np.diag(pcov))[1]
        self.Fit=True
    def get_time(self):
        return np.log(0.01)/self.lam,self.Dlam*np.abs(np.log(0.01)/self.lam**2)

    def get_fall(self):
        return self.data["CH1_x"][self.trigger:],self.data["CH1_y"][self.trigger:]
    def plot(self):
        fig = plt.figure(figsize=(11, 6))
        gs = GridSpec(5, 5)
        fig1 = fig.add_subplot(gs[:5, :])
        fig1.set_title("Spannung bei einen Wechsel der Amplitude des Eingangssignals")
        fig1.set_ylabel("$U$ in V")
        fig1.set_xlabel("Zeit in s")
        fig1.scatter(self.data["CH1_x"][:],self.data["CH1_y"][:],marker="o",s=5,label="R-Ausgang", color="b")
        fig1.plot(self.data["CH2_x"], self.data["CH2_y"],linewidth=1,label="Eingang", color="g")
        if self.fit:
            fig1.plot(self.data["CH1_x"][self.trigger:], self.fit_exp(self.data["CH1_x"][self.trigger:]), label="Fit",color="r")
        plt.tight_layout()
        plt.legend()
        plt.savefig("plots/U_zeit_bsp.pdf")
        # plt.savefig("plots/U(theta).pdf")
        plt.show()



def main():
    lambda_list=[]
    X_list=[]
    Y_list=[]
    for i in range(4):
        ex = data_class(str(i))
        ex.fit()
        ex.plot()
        X=np.array(ex.get_fall()[0])
        Y=np.array(ex.get_fall()[1])
        print(i, ex.get_time())
        X_list.append(np.array(X-X[0]))
        Y_list.append(Y)
    fig = plt.figure(figsize=(11, 6))
    gs = GridSpec(8, 5)
    fig1 = fig.add_subplot(gs[:, :])
    fig1.set_title("Ausgangsspannung nach einen Wechsel der Amplitude des Eingangssignals")
    fig1.set_ylabel("$U_{out}$ in V")
    fig1.set_xlabel("$t-t_0$ in s")
    for i in range(4):
        fig1.plot(X_list[i],Y_list[i],label=f"Zeitkonstante {i}")
    plt.tight_layout()
    plt.legend()
    plt.savefig("plots/U_zeit_vgl.pdf")
    plt.show()


if __name__=="__main__":
    main()

