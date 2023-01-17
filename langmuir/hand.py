import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib as mpl
import numpy as np
from scipy.stats import linregress
import scipy.constants as const
mpl.use("QT5Agg")
plt.rcParams['font.size']=15

mass_ar=39.948*const.u
A=9.2e-6
class data_class():
    def __init__(self):
        I=np.array([287,287,286,285,284,282,281,276,274,273,271,269,268,266,264,262,259,256,253,249,246,241,235,229,221,211,199,177,136,96,65,42,26,15,8,4,2,1])
        I=np.append(I,np.array([0 for i in range(22)]))
        I_alt=np.array([14.6,8.2,4.3,2.2,1.0,0.5,0.2,0.0,0.0])
        I_alt=np.append(I[:len(I)-len(I_alt)-18],np.append(I_alt,np.array([-0.1 for i in range(18)])))
        self.U=-np.array([0.25*i for i in range(1,len(I)+1)])
        self.I_alt=I_alt
        self.I=I
        self.Ie=[0]
    def plot(self,log):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(5, 5)
        fig1 = fig.add_subplot(gs[:5, :])
        fig1.set_title("Selbstaufgenommene Kennlinie")
        fig1.set_ylabel("I in mA")
        fig1.set_xlabel("U in V")
        #fig1.plot(U,I, marker="o",label="2000$\mu$")
        if log:
            fig1.set_yscale("log")
        fig1.plot(self.U[40-11:40],self.I_alt[40-11:40], marker="o",)
        plt.tight_layout()
        plt.show()
    def get_intersection(self):
        U=self.U
        I=self.I_alt
        for i in range(len(U) - 2):
            if np.sign(I[i]) != np.sign(I[i + 1]):
                self.floating = np.roots([linregress([U[i], U[i + 1]], [I[i], I[i + 1]])[0],
                                 linregress([U[i], U[i + 1]], [I[i], I[i + 1]])[1]])
                self.Dfloating=0.125
                print("Floating Pot",self.floating)
    def get_ioncurr(self):
        self.Ic=self.I_alt[np.where(self.U==-13.75)]
        print("Ion Current",self.Ic)
        self.I_alt=np.array(self.I_alt)-self.Ic
    def get_turiningpoint(self):
        diffs=[]
        for i in range(len(self.U)-1):
            diffs.append(self.I_alt[i]-self.I_alt[i+1])
        self.phip=self.U[np.argmax(diffs)+1]
        print("Plasma Potential by turning point",self.phip)
    def get_etemps(self):
        self.I_log=np.log(self.I_alt)
        regress1=linregress(self.U[40-11:40],self.I_log[40-11:40])
        regress2 = linregress(self.U[:20], self.I_log[:20])
        regress3 = linregress(self.U[27:30],self.I_log[27:30])
        print(regress1,regress2)
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(5, 5)
        fig1 = fig.add_subplot(gs[:5, :])
        fig1.set_title("Selbstaufgenommene Kennlinie")
        fig1.set_ylabel("I in mA")
        fig1.set_xlabel("U in V")
        fig1.plot(self.U,self.I_log, marker="o",label="Messwerte")
        fig1.plot(self.U[25:40], regress1.slope*np.array(self.U[25:40])+regress1.intercept,label="Fit $U<\Phi_P$")
        fig1.plot(self.U[:30], regress2.slope * np.array(self.U[:30]) + regress2.intercept,label="Fit $U>\Phi_P$")
        fig1.plot(self.U[27:30], regress3.slope * np.array(self.U[27:30]) + regress3.intercept, label="Fit $U>\Phi_P$")
        plt.tight_layout()
        plt.legend()
        plt.show()
        #print(regress1)
        # print(regress2)
        #get etemps out of slope of the staright
        self.Te1=const.e/(const.k*regress1.slope)
        self.Te2=const.e/(2*const.k*regress2.slope)
        self.Te3 = const.e / (2 * const.k * regress3.slope)
        self.DTe1 = const.e / (const.k * regress1.slope**2)*regress1.stderr
        self.DTe2 = const.e / (2 * const.k * regress2.slope**2)*regress2.stderr
        self.DTe3 = const.e / (2 * const.k * regress3.slope ** 2) * regress3.stderr
        # get plasma potential out of intersection of the 2 slopes
        self.phip1=np.roots([regress1.slope-regress2.slope,regress1.intercept-regress2.intercept])
        self.Dphip1=regress1.intercept_stderr/(regress1.slope-regress2.slope)\
                    +regress2.intercept_stderr/(regress1.slope-regress2.slope)\
                    +regress1.stderr*(regress1.intercept-regress2.intercept)/(regress1.slope-regress2.slope)**2\
                    +regress2.stderr*(regress1.intercept-regress2.intercept)/(regress1.slope-regress2.slope)**2
        #get etemp out of the difference from plasamapotential and floating potential
        self.Te4=(self.floating-self.phip1)*const.e/const.k/np.log(0.6*np.sqrt(2*np.pi*const.electron_mass/mass_ar))
        self.DTe4=np.abs(self.Dfloating*const.e/const.k/np.log(0.6*np.sqrt(2*np.pi*const.electron_mass/mass_ar)))\
                  +np.abs(self.Dphip1*const.e/const.k/np.log(0.6*np.sqrt(2*np.pi*const.electron_mass/mass_ar)))
        #get density
        self.ne=self.Ie/(A*const.e*np.sqrt(const.k*self.Te3/(2*np.pi*const.electron_mass)))
        self.ni=self.Ic/(0.6*const.e*A*np.sqrt(const.k*self.Te3/mass_ar))
        print("Temperatur im Anlaufbereich",self.Te1, self.DTe1)
        print("Temperatur im E Sättigung",self.Te2, self.DTe2)
        print("Temperatur im E Sättigung alternativ", self.Te3, self.DTe3)
        print("Plasma Potential",self.phip1,self.Dphip1)
        print("Temperatur aus Differenz der Potentiale",self.Te4,self.DTe4)

def main():
    #init data
    data=data_class()
    #get floating point
    data.get_intersection()
    #get ion current and subtract it from the dataset
    data.get_ioncurr()
    #get etemps
    data.get_turiningpoint()
    data.get_etemps()

main()