import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from scipy.optimize import curve_fit
import numpy as np
mpl.use('Qt5Agg')

angle=[15*i for i in range(13)]
angle_cont=np.linspace(0,180,180)
intensity=[223,272,426,568,528,331,233,302,358,409,322,269,214]
intensity2=[834,641,381,316,515,790,848,690,432,328,510,842,892]
intensity3=[254,347,497,524,427,286,258,333,497,532,426,298,263]

sin = lambda x,f,phi,A,c: A*np.sin(f*x+phi)+c

popt,pcov = curve_fit(sin,angle,intensity2)
fit1 = lambda x: sin(x,popt[0],popt[1],popt[2],popt[3])
# print(popt)
popt1,pcov1 = curve_fit(sin,angle,intensity3,bounds=([0,-np.inf,-200,-np.inf],[0.3,np.inf,200,np.inf]),p0=[0.075,-np.pi/2,150,400],maxfev=100000)
# popt1=[0.075,-np.pi/2,150,400]
print(popt1)
fit2 = lambda x: sin(x,popt1[0],popt1[1],popt1[2],popt1[3])
fig = plt.figure(figsize=(10, 5))
gs = GridSpec(5, 5)
fig1 = fig.add_subplot(gs[:5, :])
fig1.set_title("Intensität in Abhängigkeit vom Winkel des $\lambda$/2 Plättchen")
fig1.set_ylabel("Intensity in AU")
fig1.set_xlabel("angle in °")
fig1.plot(angle,intensity2, marker="o",label="$\pi$ Komponente",color="red")
fig1.plot(angle,intensity3, marker="o",label="$\sigma$ Komponente",color="green")
fig1.plot(angle_cont,fit1(angle_cont),label="$\pi$ Fit",color="red",linestyle="--")
fig1.plot(angle_cont,fit2(angle_cont),label="$\sigma$ Fit",color="green",linestyle="--")
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("plots/I(alpha).pdf")
plt.show()