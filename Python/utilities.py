import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import soundfile as sf
import random
import math
from pysndfx import AudioEffectsChain

clingo_args = [
    "--warn=none",
    "--sign-def=rnd",
    "--sign-fix",
    "--rand-freq=1",
    "--seed=%s" % random.randint(0, 32767),
    "--restart-on-model",
    "--enum-mode=record",
]


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(6, 1), dpi=100)
        super().__init__(fig)
        self.setParent(parent)

    def plotAudio(self, inSamples):
        self.ax.plot(inSamples)
        self.ax.axis("off")
        plt.savefig("Results/audio.png")


def computeInterval(inBpm, inSampleRate):
    interval = int((60 / inBpm) * inSampleRate)
    return interval


def makeCut(inPath, inLen):
    finalAudio = []
    cont = 0
    audio, samplerate = sf.read(inPath)
    inLen = convertMilliToSamples(inLen, samplerate)
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
        inAudio[sample + startRelease] *= lineRelease
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


def applyFilter(inAudio, inInstrument, inFrequency):
    if inInstrument == "kick":
        low = AudioEffectsChain().lowpass(inFrequency, 1)
        audio = low(inAudio)
        return audio

    elif inInstrument == "snare":
        high = AudioEffectsChain().highpass(inFrequency, 1)
        audio = high(inAudio)
        return audio

    elif inInstrument == "hihat":
        high = AudioEffectsChain().highpass(inFrequency, 1)
        audio = high(inAudio)
        return audio
