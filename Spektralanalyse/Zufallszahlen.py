import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import norm
from scipy.optimize import curve_fit
import matplotlib as mpl
mpl.use("QT5Agg")
plt.rcParams['font.size']=20


def gauss(x,a,m,c):
    an=a/norm.pdf(m,loc=m,scale=c)
    return an*norm.pdf(x,loc=m,scale=c)

class spektral:

    def __init__(self, path, time_or_spec, f_A=None, dB=False) -> None:
        '''Übergabe eines Pfades/Dateinamen der dann geladen wird.
        Angabe notwendig, ob es sich um Time Series oder Spektrum handelt.
        Falls es eine Zeitreihe ist, kann eine Abtastfrequenz übergeben
        werden. In diesem Fall wird das Spektrum zusätzlich selbst
        berechnet. Falls time_or_spec==both ist path ein Tupel mit
        (time, spec).'''
        self.time_or_spec = time_or_spec
        self.dB = dB
        # Transponiere, um x-Achse an Index 0 zu haben
        if time_or_spec == 'time':
            self.time = np.loadtxt(path, usecols=(0, 1)).T
        if time_or_spec == 'spec':
            self.spec = np.loadtxt(path, usecols=(0, 1)).T
        if time_or_spec == 'both':
            self.time = np.loadtxt(path[0], usecols=(0, 1)).T
            self.spec = np.loadtxt(path[1], usecols=(0, 1)).T
        if time_or_spec == 'time' and f_A is not None:
            self.time_or_spec = 'both'
            self.spec = self.spectrum(self.time[1], f_A)

    def plot(self, ax, label=None):
        '''Die Funktion plotted Daten in subplot ax.
        time_or_spec gibt an, ob timeseries oder Spekrum geplotted werden soll.'''

        if self.time_or_spec == 'time':
            ax.plot(self.time[0], self.time[1], label=label)
            ax.set_xlabel('Zeit in Sekunden')
            ax.set_ylabel('Auslenkung in V')

        if self.time_or_spec == 'spec':
            ax.plot(self.spec[0], self.spec[1], label=label)
            ax.set_xlabel('Frequenz in Hz')
            if self.dB == False:
                ax.set_ylabel(r'Leistung in V$^2$')
            if self.dB == True:
                ax.set_ylabel(r'Leistung in dB')

    def plot_both(self, title=None, x1lim=None, x2lim=None):
        '''Bei der Zeitreihe und Frequenz kann der Bereich der x-Achse angegeben werden.'''
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,10))
        ax1.plot(self.time[0], self.time[1])
        ax1.set_xlabel('Zeit in Sekunden')
        ax1.set_ylabel('Auslenkung in V')
        if x1lim is not None:
            ax1.set_xlim(x1lim)
        if self.dB == False:
            ax2.plot(self.spec[0], self.spec[1])
            ax2.set_ylabel(r'Leistung in V$^2$')
        if self.dB == True:
            ### Hier Maske anpassen, eventuell Mist beim Datenspeichern gemacht???
            ax2.plot(self.spec[0], self.spec[1])
            ax2.set_ylabel(r'Leistung in dB')
        ax2.set_xlabel('Frequenz in Hz')
        if x2lim is not None:
            ax2.set_xlim(x2lim)
        if title is not None:
            ax1.set_title(title)
        plt.tight_layout()
        plt.savefig("figure.pdf")
        plt.show()

    def dft(self, x, f_A):
        N = len(x)
        n = np.arange(N)

        freq = n * f_A / N

        k = n.reshape((N, 1))
        e = np.exp(-2j * np.pi * k * n / N)
        S = abs(np.dot(e, x))  # Nehme den Betrag der komplexen Zahlen

        return freq, S

    def spectrum(self, x, f_A):
        '''Berechnung des Single-Sided-Power-Spektrums (Betragsquadrat des Amplitudenspektrums).'''
        freq, S = self.dft(x, f_A)

        N = len(freq)
        N_half = int(N / 2)
        P = np.zeros(N)
        P[0] = S[0] ** 2 / N / N
        for i in range(1, N_half):
            P[i] = 2 * (S[i] ** 2) / N / N
        return [freq, P]

    def dB_to_normal(self):
        self.spec[1]=10**np.array(self.spec[1]) /20

    def peak_intensity(self):
        mean=np.mean(np.where(self.spec[1]<1e-11,self.spec[1],0))
        peak=np.max(self.spec[1])
        print(peak,mean)
        return peak/mean
    def calc_power(self):
        power1=np.sum((self.spec[1]))*len(self.spec[1])*2
        power2=np.sum(self.time[1]**2)
        print(power1,power2,power2/power1)

    def get_spec(self):
        return self.spec

class histogram:
    def __init__(self,name):
        self.name=name
        self.data=np.loadtxt(self.name+".dat")
        self.pdf=np.loadtxt(self.name+".pdf")
        self.gauss=False
    def plot(self,which):
        fig = plt.figure(figsize=(10, 10))
        gs = GridSpec(5, 5)
        fig1 = fig.add_subplot(gs[:5, :])
        fig1.set_xlabel("U in V")
        if which=="data":
            fig1.plot(self.data[:, 0], self.data[:, 1], marker="o")
        elif which=="pdf":
            fig1.bar(self.pdf[:, 0], self.pdf[:, 1],self.pdf[1,0]-self.pdf[0,0])
            if self.gauss:
                a,m,c = self.popt
                fig1.plot(self.pdf[:, 0],gauss(self.pdf[:, 0],a,m,c),color="r")
        else:
            raise exception
        plt.tight_layout()
        plt.savefig("plots/quantisierung/"+self.name+".pdf")
        plt.show()
    def fit_gauss(self):
        self.gauss=True
        self.gauss_data=self.pdf[:,2]
        self.popt,self.pcov = curve_fit(gauss,self.pdf[:,0],self.pdf[:,2])
    def calc_moments(self):
        xdata = self.data[:, 0]
        ydata = self.data[:, 1]
        mean=np.sum(ydata)*1/len(ydata)#
        moments=[]
        for i in range(1,5):
            moment=np.sum((ydata-mean)**i) * 1 / len(ydata)
            moments.append((moment))
        moments[1]=np.sqrt(moments[1])
        moments[2]=moments[2]/moments[1]**3
        moments[3] = moments[3] / moments[1] ** 4
        return mean,moments





def pseudo():
    #schlechtes Beispiel
    seed_1 = np.loadtxt("4/4a/se_1_a_2_m_7.ran")
    seed_2 = np.loadtxt("4/4a/se_3_a_2_m_7.ran")
    fig = plt.figure(figsize=(5,5))
    gs = GridSpec(5,5)
    fig1 = fig.add_subplot(gs[:5, :])
    fig1.set_title("Pseudozufallszahlen: $a=2\qquad m=7$")
    fig1.set_ylabel("N(i+1)")
    fig1.set_xlabel("N(i)")
    fig1.plot(seed_1[:, 0], seed_1[:, 1], marker="o",label="seed=1")
    fig1.plot(seed_2[:, 0], seed_2[:, 1], marker="o",label="seed=3")
    plt.tight_layout()
    plt.legend()
    plt.savefig("plots/pseudo/pseudo_a2_m7.pdf")
    plt.show()
    #besseres Beispiel
    m_17 = np.loadtxt("4/4a/se_3_a_6_m_17.ran")
    fig = plt.figure(figsize=(5, 5))
    gs = GridSpec(5, 5)
    fig1 = fig.add_subplot(gs[:5, :])
    fig1.set_title("Pseudozufallszahlen: $a=6\quad m=17\quad s=3$")
    fig1.set_ylabel("N(i+1)")
    fig1.set_xlabel("N(i)")
    fig1.plot(m_17[:, 0], m_17[:, 1], marker="o")
    plt.tight_layout()
    plt.savefig("plots/pseudo_a6_m17.pdf")
    plt.show()

def quantisierung():
    bit8_21=histogram("4/4b/8_bit_sigma_002")
    bit8_21.fit_gauss()
    bit8_21.plot("pdf")
    bit16_21 = histogram("4/4b/16_bit_sigma_002")
    bit16_21.fit_gauss()
    bit16_21.plot("pdf")

def laenge():
    lens=[128*2**i for i in range(5)]
    lens.append(16384)
    means=[]
    sigma=[]
    skewness=[]
    kurtosis=[]
    for i in lens:
        data=histogram("4/4c/series_"+str(i))
        me,si,sk,ku = data.calc_moments()[1]
        me = data.calc_moments()[0]
        means.append(me)
        sigma.append(si)
        skewness.append(sk)
        kurtosis.append(ku)
    lens_log=np.log2(lens)
    plt.plot(lens_log,np.array(kurtosis)-3,marker="o",label="Exzess")
    plt.plot(lens_log, skewness, marker="o", label="Schiefe")
    plt.plot(lens_log, sigma, marker="o", label="$\sigma$")
    plt.plot(lens_log, means, marker="o", label="Mittelwert")
    plt.xlabel("Länge der Zeitreihe in $2^x$")
    plt.ylabel("Wert des Moments")
    plt.legend()
    plt.savefig("plots/moments_rausch.pdf")
    plt.show()

def spektrum():
    lens=[128,512,32786]
    lens_log=[np.log2(i) for i in lens]
    peak_intensity=[]
    specs=[]
    specs_db=[]
    for le in lens:
        len_=spektral(["4/4e/length_"+str(le)+".dat","4/4e/length_"+str(le)+".aps","spec"],time_or_spec="both",dB=True)
        len_.dB_to_normal()
        peak_intensity.append(len_.peak_intensity())
        spec_db=len_.get_spec().copy()
        specs_db.append(spec_db)
        # len_.plot_both()
        len_.dB_to_normal()
        # len_.plot_both()
        spec=len_.get_spec()[:]
        specs.append(spec)
    plt.yscale("log")
    plt.plot(lens_log,peak_intensity,marker="o")
    plt.xlabel("Länge des Datensatz in $2^x$")
    plt.ylabel("$I_{peak}$")
    plt.tight_layout()
    plt.savefig("plots/rauschen_len.pdf")
    plt.show()
    fig=plt.figure(figsize=(10,15))
    gs = GridSpec(2,1)
    fig1 = fig.add_subplot(gs[:1, :])
    fig2 = fig.add_subplot(gs[1:, :])
    fig1.set_title("Gausches Rauschen bei verschiedenen Messzeiten")
    fig1.set_ylabel("Leistung in V$^2$")
    fig1.set_xlabel("Frequenz in Hz")
    fig2.set_ylabel("Leistung in dB")
    fig2.set_xlabel("Frequenz in Hz")
    fig1.plot(specs[0][0], specs[0][1],label="N=128")
    fig1.plot(specs[2][0], specs[2][1],label="N=32786")
    fig2.plot(specs_db[0][0], specs_db[0][1],label="N=128")
    fig2.plot(specs_db[2][0], specs_db[2][1],label="N=32786")
    plt.tight_layout()
    plt.legend()
    plt.savefig("plots/Rauschen_len2.pdf")
    plt.legend()
    plt.show()
    pass

def mittel():
    fig = plt.figure(figsize=(10, 10))
    fig1 = fig.add_subplot()
    fig1.set_title("Gausches Rauschen mit und ohne Mittelung")
    fig1.set_ylabel("Leistung in dB")
    fig1.set_xlabel("Frequenz in Hz")
    mittel_on=spektral("4/4f/mittelung_32_on.aps","spec",dB=True)
    mittel_on.plot(fig1,label="Mittlung an")
    mittel_off=spektral("4/4f/mittelung_32_off.aps","spec",dB=True)
    mittel_off.plot(fig1,label="Mittlung aus")
    plt.tight_layout()
    plt.legend()
    plt.savefig("plots/Rauschen_Mittelung.pdf")
    plt.show()
    mittel_on.dB_to_normal()
    mittel_off.dB_to_normal()
    print(mittel_on.peak_intensity(),mittel_off.peak_intensity())
    pass

def rausch():
    rauschen=spektral(["4/4d/rausch_01.dat","4/4d/rausch_01.aps"],"both",dB=True)
    # rauschen = spektral(["2/2b/Len_64.dat", "2/2b/len32.aps"], "both")

    rauschen.calc_power()
    rauschen.plot_both()

def power():
    sin = spektral(["2/2b/Len_256.dat", "2/2b/len256.aps"], "both")
    sin.calc_power()
    sin2 = spektral(["2/2b/Len_128.dat", "2/2b/len128.aps"], "both")
    sin2.calc_power()
    rauschen = spektral(["4/4d/rausch_01.dat", "4/4d/rausch_01.aps"], "both")
    rauschen.calc_power()



def main():
    # pseudo()
    # quantisierung()
    # laenge()
    spektrum()
    # mittel()
    # rausch()
    # power()
    pass

if __name__=="__main__":
    main()