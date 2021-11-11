import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import soundfile as sf
import random
import math

clingo_args = [ "--warn=none",
                "--sign-def=rnd",
                "--sign-fix",
                "--rand-freq=1",
                "--seed=%s"%random.randint(0,32767),
                "--restart-on-model",
                "--enum-mode=record"]

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

def makeKickPattern(inAudio, inBPM, inNumCompas,inSampleRate):

    #audio, samplerate = sf.read(inPath)
    audio = inAudio
    kickInterval = computeInterval(inBPM, inSampleRate)
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

    sf.write('../Results/LoopKick.wav', compasCompleto, inSampleRate, 'PCM_24')

    print("KICK LOOP CREADO")
    print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

def makeCut (inPath, inLen):
    finalAudio = []
    cont = 0
    audio, samplerate = sf.read(inPath)
    inLen = convertMilliToSamples(inLen,samplerate)
    for sample in audio:
        if cont < inLen:
            finalAudio.append(sample)
        cont += 1
    return finalAudio, samplerate

def convertMilliToSamples(inValue, inSampleRate):
    inSec = inValue * 0.001
    inSamples = inSec * inSampleRate
    return inSamples

def applyEnvelope(inAudio, inSampleRate, inAttack, inRelease):

    lineAttack = 0
    lineRelease = 1

    attackinSamples = convertMilliToSamples(inAttack, inSampleRate)
    releaseinSamples = convertMilliToSamples(inRelease, inSampleRate)

    intervalAttack = 1 / attackinSamples
    intervalRelease = 1 / releaseinSamples

    for sample in range(int(attackinSamples)):
        inAudio[sample] *= lineAttack
        lineAttack += intervalAttack

    startRelease = len(inAudio) - int(releaseinSamples)
    for sample in range(int(releaseinSamples)):
        inAudio[sample+startRelease] *= lineRelease
        lineRelease -= intervalRelease

    return inAudio

def spectralSpread(inFrequency, inAmplitude, inCentroid):
    i = 0
    numerator = 0
    denominator = 0
    for frequency in inFrequency:
        numerator += (frequency - inCentroid) ** 2 * inAmplitude[i]
        denominator += inAmplitude[i]
        i += 1
    return math.sqrt(numerator / denominator)