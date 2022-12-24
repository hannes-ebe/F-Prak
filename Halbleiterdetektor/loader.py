import numpy as np

class Loader():
    '''Einlesen von .txt-Datein oder ähnlichen Dateiformaten. Spalten werden als numpy-arrayds in dictionaries organisiert.
    Die eingelesenen Spalten werden im Array unter den Namen im Parameter header (Liste oder ähnliches) gespeichert.'''

    def __init__(self, filepath, header, usecols=None, comments='#', delimiter=None, skip_header=0, skip_footer=0) -> dict:
        self.data = {}
        ayuda = np.genfromtxt(fname=filepath, comments=comments, delimiter=delimiter, usecols=usecols, skip_header=skip_header, skip_footer=skip_footer).T
        for i in range(len(header)):
            self.data[header[i]] = ayuda[i]

def arr_to_tab(*args):
    out=[]
    for i in range(len(args[0])):
        string=""
        for j in range(len(args)):
            string+=str(args[j][i])+"&"
        string+="\\\"+"\\\"+"\\vline"
        out.append(string)
    np.savetxt("tab",out,fmt='%s')

