import sys
from PyQt5.QtWidgets import *
import dragAudio
import utilitiesGUI
import soundfile as sf
from scipy.fft import rfft, rfftfreq
import numpy as np
from matplotlib import pyplot as plt

class Main(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 300)

        self.path = "none"

        # LOAD AUDIOS #
        self.btnMix = QPushButton('Create', self)
        self.btnMix.setGeometry(10, 10, 200, 50)
        self.btnMix.clicked.connect(lambda: self.startCreating())

        self.boxAudio = dragAudio.ListboxWidget(self)
        self.boxAudio.setPos(250, 15)

    def plotAudio(self):
        self.path = QListWidgetItem(self.boxAudio.item(0))
        if self.path.text():
            self.path = self.path.text()
            audio, samplerate = sf.read(self.path)
            self.chart = utilitiesGUI.Canvas(self)
            self.chart.plotAudio(audio)
            self.chart.setGeometry(10, 80, 460, 200)
            self.chart.show()
        print("AUDIO PLOTTED")
        print("-------------")

    def startCreating(self):
        self.plotAudio()
        audio, samplerate, duration = utilitiesGUI.makeKickPattern(self.path, 120, 4)

        ## FFT
        samples = duration * samplerate
        kickAmp = rfft(audio)
        kickFreq = rfftfreq(samples, 1 / samplerate)

        plt.plot(kickFreq, np.abs(kickAmp))
        plt.show()

'''def applyEnvelope(inAudio, inSampleRate, inAttack, inRelease):

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

def convertMilliToSamples(inValue, inSampleRate):
    inSec = inValue * 0.001
    inSamples = inSec * inSampleRate
    return inSamples

audio, samplerate = sf.read('audios/guitar.wav')
audio = applyEnvelope(audio, samplerate, 1000, 1000)
sf.write('Results/Attack.wav', audio, 44100, 'PCM_24')'''

app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())