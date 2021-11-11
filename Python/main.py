import sys
from PyQt5.QtWidgets import *
import dragAudio
import utilitiesGUI
import soundfile as sf
import clingo, math
from scipy.fft import rfft, rfftfreq
import numpy as np
from matplotlib import pyplot as plt
import librosa
'''from pyAudioAnalysis import ShortTermFeatures'''

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
        audio, samplerate = utilitiesGUI.makeCut(self.path,400)
        audio = utilitiesGUI.applyEnvelope(audio,samplerate,200,30)
        sf.write('../Results/corte.wav', audio, samplerate, 'PCM_24')
        loop, samplerate, duration = utilitiesGUI.makeKickPattern(audio, 120, 4, samplerate)
        self.getfromClingo()
        self.makeAnalysis(loop, duration, samplerate)

    def makeAnalysis(self, audio, duration, samplerate):
        samples = duration * samplerate
        amplitude = np.abs(rfft(audio))
        frequency = rfftfreq(int(samples), 1 / samplerate)
        centroid = np.sum(amplitude * frequency) / np.sum(amplitude)
        print(centroid)
        spread = utilitiesGUI.spectralSpread(frequency, amplitude, centroid)
        print(spread)
        peakIndex = np.argmax(np.array(amplitude))
        print(peakIndex)
        peak = frequency[peakIndex]
        print(peak)

    def getfromClingo(self):
        # ** CONFIGURAR Y CARGAR CLINGO *** #
        control = clingo.Control(utilitiesGUI.clingo_args)
        control.configuration.solve.models = 5
        control.load("../remixer.lp")
        models = []

        # ** GROUNDING *** #
        print("Grounding...")
        control.ground([("base", [])])
        print("------")

        # ** SOLVE *** #
        print("Solving...")
        with control.solve(yield_=True) as solve_handle:
            for model in solve_handle:
                models.append(model.symbols(shown=True))
        print("------")
        print(models)

app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())