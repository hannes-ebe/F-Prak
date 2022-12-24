import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.stats import linregress
mpl.use('Qt5Agg')
plt.rcParams['font.size']=15
class Kalibration:
    def __init__(self):
        pass

    def uberlegen(self):
        thorlabs=np.loadtxt("data/thorlabs_nichtsat.txt")
        wellenlänge= []
        intensity_thor=[]
        for line in thorlabs:
            wellenlänge.append(line[0])
            intensity_thor.append(line[1])

        eigen=np.loadtxt("data/spektrum/spektrum_500_5.dat")
        step=[]
        intensity_ccd = []
        for line in eigen:
            step.append(line[0])
            intensity_ccd.append(line[1])
        step=(np.array(step)-self.b)/self.m
        intensity_ccd=(np.array(intensity_ccd)-260)*1e-3/0.8
        print(step,intensity_ccd)

        fig = plt.figure(figsize=(10, 5))
        gs = GridSpec(5, 5)
        fig1 = fig.add_subplot(gs[:5, :])
        fig1.set_xlim(580,650)
        fig1.set_title("Übereinanderlegeung der beiden Spektren")
        fig1.set_ylabel("Intensität in AU")
        fig1.set_xlabel("$\lambda$ in nm")
        fig1.plot(wellenlänge,intensity_thor,label="thorlabs")
        fig1.plot(step,intensity_ccd,label="Schrittmotor")
        plt.tight_layout()
        plt.legend()
        plt.savefig("plots/kalibration_übereinanderlegung.pdf")
        plt.show()
    def maxima(self):
        maxima_thorlabs=[584.3,587.4,593.6,602.2,606.5,608.8,613.3,615,626]
        maxima_spektrum=[9500,9900,10900,12300,13000,13300,14000,14300,15900]

        print(linregress(maxima_thorlabs,maxima_spektrum))
        self.m,self.b=linregress(maxima_thorlabs,maxima_spektrum)[0],linregress(maxima_thorlabs,maxima_spektrum)[1]

        fig = plt.figure(figsize=(10, 5))
        gs = GridSpec(5, 5)
        fig1 = fig.add_subplot(gs[:5, :])
        fig1.set_xlim(580, 650)
        fig1.set_title("Position der Peaks in beiden Spektren")
        fig1.set_ylabel("Schrittmotor Position der Peaks")
        fig1.set_xlabel("Position der Peaks im Thorlabs Spektrum in nm")
        fig1.plot(maxima_thorlabs,maxima_spektrum,"o",label="Schrittmotor Spektrum")
        fig1.plot(maxima_thorlabs,linregress(maxima_thorlabs,maxima_spektrum)[0]*np.array(maxima_thorlabs)+linregress(maxima_thorlabs,maxima_spektrum)[1],label="linearer Fit")
        plt.legend()
        plt.tight_layout()
        plt.savefig("plots/kalibration_peaks.pdf")
        plt.show()

def alttoneu(lam):
    return (np.array(lam)-522)*153

def main():
    kali=Kalibration()
    kali.maxima()
    kali.uberlegen()


if __name__=="__main__":
    main()

