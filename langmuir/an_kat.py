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



data=pd.read_csv("data/100V_-15_5.txt", sep="\t")
U=data["% U (Volt)"]
I=data["I (A)"]
print(data,U)

fig = plt.figure(figsize=(5, 5))
gs = GridSpec(5, 5)
fig1 = fig.add_subplot(gs[:5, :])
fig1.set_title("Selbstaufgenommene Kennlinie")
fig1.set_ylabel("I in mA")
fig1.set_xlabel("U in V")
fig1.plot(U,I)
plt.tight_layout()
plt.show()