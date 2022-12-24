import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
mpl.use('Qt5Agg')

I=[0.8,1.5,2.23,2.95,3.86,5.18]
H=[5,10,15,20,22.5,25]

fig = plt.figure(figsize=(10, 5))
gs = GridSpec(5, 5)
fig1 = fig.add_subplot(gs[:5, :])
fig1.set_title("Magnetfeld in Abhängigkeit vom Strom")
fig1.set_ylabel("H in kilo Oerstedt")
fig1.set_xlabel("I in A")
fig1.plot(I,H, marker="o")
plt.tight_layout()
plt.savefig("plots/H(I).pdf")
plt.show()
