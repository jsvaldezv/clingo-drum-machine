import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import soundfile as sf

class Canvas(FigureCanvas):

    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(6, 1), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

    def plotAudio(self, inSamples):
        self.ax.plot(inSamples)
        self.ax.axis("off")

def computeInterval(inBpm, inSampleRate):
    interval = int((60 / inBpm) * inSampleRate)
    return interval

def makeKickPattern(inPath, inBPM, inNumCompas):

    audio, samplerate = sf.read(inPath)
    kickInterval = computeInterval(inBPM, samplerate)
    loopKick = []

    intervalOne = kickInterval
    intervalTwo = kickInterval * 2
    intervalTres = kickInterval * 3

    cont, cont2, cont3, cont4 = 0, 0, 0, 0

    for sample in range(kickInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopKick.append(audio[sample])
            else:
                loopKick.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopKick.append(audio[cont2])
            else:
                loopKick.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopKick.append(audio[cont3])
            else:
                loopKick.append(0)
            cont3 += 1
        else:
            if cont4 < len(audio):
                loopKick.append(audio[cont4])
            else:
                loopKick.append(0)
            cont4 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopKick:
            compasCompleto.append(sample)

    sf.write('../Results/LoopKick.wav', compasCompleto, samplerate, 'PCM_24')

    print("KICK LOOP CREADO")
    print("-----------")
