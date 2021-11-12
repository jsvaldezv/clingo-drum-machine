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

#kick 1/4
def makeKickPattern(inAudio, inBPM, inNumCompas,inSampleRate):
    #Simple QuarterNote [1/4] Pattern

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

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)  #  #kick
#snare 1/4
def makeSnarePattern(inAudio, inBPM, inNumCompas,inSampleRate):
    #QuarterNote [1/4] Pattern with OFFSET

    #audio, samplerate = sf.read(inPath)
    audio = inAudio
    snareInterval = computeInterval(inBPM, inSampleRate)
    loopSnare = []

    intervalOne = snareInterval
    intervalTwo = snareInterval * 2
    intervalTres = snareInterval * 3

    cont, cont2, cont3, cont4 = 0, 0, 0, 0

    for sample in range(snareInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopSnare.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopSnare.append(audio[cont2])
            else:
                loopSnare.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopSnare.append(0)
            cont3 += 1
        else:
            if cont4 < len(audio):
                loopSnare.append(audio[cont4])
            else:
                loopSnare.append(0)
            cont4 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopSnare:
            compasCompleto.append(sample)

    sf.write('../Results/LoopSnare.wav', compasCompleto, inSampleRate, 'PCM_24')

    print("SNARE LOOP CREADO")
    print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)
#snare 1/8
def makeSnarePattern2(inAudio, inBPM, inNumCompas,inSampleRate):
    # Eight note [1/8] pattern with variations

    #audio, samplerate = sf.read(inPath)
    audio = inAudio
    kickInterval = computeInterval(inBPM, inSampleRate)
    loopKick = []

    intervalOne = kickInterval/2
    intervalTwo = kickInterval
    intervalTres = kickInterval * 1.5
    intervalCuatro = kickInterval * 2
    intervalCinco = kickInterval * 2.5
    intervalSix = kickInterval * 3
    intervalSeven = kickInterval * 3.5

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(kickInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopKick.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopKick.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopKick.append(audio[cont3])
            else:
                loopKick.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopKick.append(audio[cont4])
            else:
                loopKick.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopKick.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopKick.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopKick.append(audio[cont7])
            else:
                loopKick.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopKick.append(audio[cont8])
            else:
                loopKick.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopKick:
            compasCompleto.append(sample)

    sf.write('../Results/LoopSnare2.wav', compasCompleto, inSampleRate, 'PCM_24')

    print("SNARE LOOP CREADO")
    print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)
#kick 1/8 var
def makeKickPattern2(inAudio, inBPM, inNumCompas,inSampleRate):
    # Eight note [1/8] pattern with variations

    #audio, samplerate = sf.read(inPath)
    audio = inAudio
    kickInterval = computeInterval(inBPM, inSampleRate)
    loopKick = []

    intervalOne = kickInterval/2
    intervalTwo = kickInterval
    intervalTres = kickInterval * 1.5
    intervalCuatro = kickInterval * 2
    intervalCinco = kickInterval * 2.5
    intervalSix = kickInterval * 3
    intervalSeven = kickInterval * 3.5

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(kickInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopKick.append(audio[sample])
            else:
                loopKick.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopKick.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopKick.append(audio[cont3])
            else:
                loopKick.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopKick.append(audio[cont4])
            else:
                loopKick.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopKick.append(audio[cont5])
            else:
                loopKick.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopKick.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopKick.append(audio[cont7])
            else:
                loopKick.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopKick.append(audio[cont8])
            else:
                loopKick.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopKick:
            compasCompleto.append(sample)

    sf.write('../Results/LoopKick2.wav', compasCompleto, inSampleRate, 'PCM_24')

    print("KICK LOOP CREADO")
    print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)
#hat 1/8
def makeHatPattern(inAudio, inBPM, inNumCompas,inSampleRate):
    # Simple eight note [1/8] pattern

    #audio, samplerate = sf.read(inPath)
    audio = inAudio
    hatInterval = computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/2
    intervalTwo = hatInterval
    intervalTres = hatInterval * 1.5
    intervalCuatro = hatInterval * 2
    intervalCinco = hatInterval * 2.5
    intervalSix = hatInterval * 3
    intervalSeven = hatInterval * 3.5
    intervalEight = hatInterval * 4

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopHat.append(audio[sample])
            else:
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopHat.append(audio[cont2])
            else:
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopHat.append(audio[cont3])
            else:
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopHat.append(audio[cont4])
            else:
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopHat.append(audio[cont5])
            else:
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopHat.append(audio[cont6])
            else:
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopHat.append(audio[cont7])
            else:
                loopHat.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopHat.append(audio[cont8])
            else:
                loopHat.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    sf.write('../Results/LoopHat.wav', compasCompleto, inSampleRate, 'PCM_24')

    print("HIHAT LOOP CREADO")
    print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)
#hat 1/16
def makeHatPattern2(inAudio, inBPM, inNumCompas,inSampleRate):
    # Simple sixteenth note [1/16] pattern

    #audio, samplerate = sf.read(inPath)
    audio = inAudio
    hatInterval = computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/4
    intervalTwo = hatInterval/2
    intervalTres = hatInterval * 0.75
    intervalCuatro = hatInterval
    intervalCinco = hatInterval * 1.25
    intervalSix = hatInterval * 1.5
    intervalSeven = hatInterval * 1.75
    intervalEight = hatInterval * 2
    intervalNine = hatInterval * 2.25
    intervalTen = hatInterval * 2.5
    intervalEleven = hatInterval * 2.75
    intervalDoce = hatInterval * 3
    intervalTrece = hatInterval * 3.25
    intervalCatorce = hatInterval * 3.5
    intervalQuince = hatInterval * 3.75

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0
    cont9, cont10, cont11, cont12, cont13, cont14, cont15, cont16 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopHat.append(audio[sample])
            else:
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopHat.append(audio[cont2])
            else:
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopHat.append(audio[cont3])
            else:
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopHat.append(audio[cont4])
            else:
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopHat.append(audio[cont5])
            else:
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopHat.append(audio[cont6])
            else:
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopHat.append(audio[cont7])
            else:
                loopHat.append(0)
            cont7 += 1
        elif sample >= intervalSeven and sample < intervalEight:
            if cont8 < len(audio):
                loopHat.append(audio[cont8])
            else:
                loopHat.append(0)
            cont8 += 1
        elif sample >= intervalEight and sample < intervalNine:
            if cont9 < len(audio):
                loopHat.append(audio[cont9])
            else:
                loopHat.append(0)
            cont9 += 1
        elif sample >= intervalNine and sample < intervalTen:
            if cont10 < len(audio):
                loopHat.append(audio[cont10])
            else:
                loopHat.append(0)
            cont10 += 1
        elif sample >= intervalTen and sample < intervalEleven:
            if cont11 < len(audio):
                loopHat.append(audio[cont11])
            else:
                loopHat.append(0)
            cont11 += 1
        elif sample >= intervalEleven and sample < intervalDoce:
            if cont12 < len(audio):
                loopHat.append(audio[cont12])
            else:
                loopHat.append(0)
            cont12 += 1
        elif sample >= intervalDoce and sample < intervalTrece:
            if cont13 < len(audio):
                loopHat.append(audio[cont13])
            else:
                loopHat.append(0)
            cont13 += 1
        elif sample >= intervalTrece and sample < intervalCatorce:
            if cont14 < len(audio):
                loopHat.append(audio[cont14])
            else:
                loopHat.append(0)
            cont14 += 1
        elif sample >= intervalCatorce and sample < intervalQuince:
            if cont15 < len(audio):
                loopHat.append(audio[cont15])
            else:
                loopHat.append(0)
            cont15 += 1
        else:
            if cont16 < len(audio):
                loopHat.append(audio[cont16])
            else:
                loopHat.append(0)
            cont16 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    sf.write('../Results/LoopHat2.wav', compasCompleto, inSampleRate, 'PCM_24')

    print("HIHAT LOOP CREADO")
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