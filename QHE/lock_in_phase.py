#import necassary modules and choose mode for displaying plots
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from scipy.optimize import curve_fit
mpl.use("QT5Agg")
plt.rcParams['font.size']=15
#load in data
theta=np.array([22.5*i for i in range(17)])
theta_fine=np.array([1*i for i in range(360)])
X=[3.61,3.32,2.54,1.36,-0.023,-1.4,-2.56,-3.32,-3.59,-3.28,-2.5,-1.37,0.046,1.41,2.59,3.32,3.58]
Y=[-0.039,-1.39,-2.59,-3.17,-3.43,-3.13,-2.39,-1.22,-0.0936,1.44,2.57,3.33,3.57,3.3,2.52,1.36,-0.009]
#fit data
fit_f = lambda x,f,phi,A: A*np.sin(f*x+phi)
popt_X,pcov_X = curve_fit(fit_f,theta,X,p0=[1/100,np.pi/2,3.5])
fit_X = lambda x: fit_f(x,popt_X[0],popt_X[1],popt_X[2])

popt_Y,pcov_Y = curve_fit(fit_f,theta,Y,p0=[1/100,np.pi,3.5])
fit_Y = lambda x: fit_f(x,popt_Y[0],popt_Y[1],popt_Y[2])


fig = plt.figure(figsize=(16, 9))
gs = GridSpec(5, 5)
fig1 = fig.add_subplot(gs[:5, :])
fig1.set_title("Ausgangsspannung des Lock-in Verstärkers in Abhängigkeit der Phase")
fig1.set_ylabel("$U_{out}$ in V")
fig1.set_xlabel("Phase in °")
fig1.plot(theta,X,"x",label="X-Ausgang",color="b")
fig1.plot(theta_fine,fit_X(theta_fine),label="X Fit",color="b")
fig1.plot(theta,Y,"x",label="Y_Ausgang",color="r")
fig1.plot(theta_fine,fit_Y(theta_fine),label="Y Fit",color="r")
plt.tight_layout()
plt.legend()
plt.savefig("plots/U(theta).pdf")
plt.show()