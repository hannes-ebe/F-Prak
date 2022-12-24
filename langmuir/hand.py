import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import norm
from scipy.optimize import curve_fit
import matplotlib as mpl
mpl.use("QT5Agg")
plt.rcParams['font.size']=15


I=np.array([287,287,286,285,284,282,281,276,274,273,271,269,268,266,264,262,259,256,253,249,246,241,235,229,221,211,199,177,136,96,65,42,26,15,8,4,2,1])
I=np.append(I,np.array([0 for i in range(22)]))
I_alt=np.array([14.6,8.2,4.3,2.2,1.0,0.5,0.2,0.0,0.0])
I_alt=np.append(I[:len(I)-len(I_alt)-18],np.append(I_alt,np.array([-0.1 for i in range(18)])))
U=-np.array([0.25*i for i in range(1,len(I)+1)])
print(U,I_alt)
print(len(I_alt),len(I))

fig = plt.figure(figsize=(5, 5))
gs = GridSpec(5, 5)
fig1 = fig.add_subplot(gs[:5, :])
fig1.set_title("Selbstaufgenommene Kennlinie")
fig1.set_ylabel("I in mA")
fig1.set_xlabel("U in V")
fig1.plot(U,I, marker="o",label="2000$\mu$")
fig1.plot(U,I_alt, marker="o",label="200$\mu$")
plt.tight_layout()
#plt.savefig("plots/pseudo_a6_m17.pdf")
plt.show()