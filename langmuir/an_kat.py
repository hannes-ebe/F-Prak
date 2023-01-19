import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib as mpl
import numpy as np
from scipy.stats import linregress
import scipy.constants as const
import pandas as pd
mpl.use("QT5Agg")
plt.rcParams['font.size']=15



data=pd.read_csv("data/100V_65_85.txt", sep="\t")
U=data["% U (Volt)"]
I=data["I (A)"]*10**6
print(data,U)

fig = plt.figure(figsize=(8, 5))
gs = GridSpec(10, 5)
fig1 = fig.add_subplot(gs[:, :])
fig1.set_title("Messung mit Sonde als Anode")
fig1.set_ylabel("I in $\mu$A")
fig1.set_xlabel("U in V")
fig1.plot(U,I)
plt.tight_layout()
plt.savefig("plots/an_kat.pdf")
# plt.savefig('figures/sonde_als_anode.pdf')
plt.show()