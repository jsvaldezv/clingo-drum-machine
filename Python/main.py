import sys
from PyQt5.QtWidgets import *
import dragAudio
import utilitiesGUI
import soundfile as sf
import clingo, math
from scipy.fft import rfft, rfftfreq
import numpy as np
import sox
from pysndfx import AudioEffectsChain

class Main(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 300)

        self.path = "none"
        self.resultados = []

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
        self.getfromClingo()
        #audio, samplerate = utilitiesGUI.makeCut(self.path,400)
        self.soundDesign()
        '''loop, samplerate, duration = utilitiesGUI.makeKickPattern(audio, 120, 4, samplerate)
        self.makeAnalysis(loop, duration, samplerate)'''

    def makeAnalysis(self, audio, duration, samplerate):
        samples = duration * samplerate
        amplitude = np.abs(rfft(audio))
        frequency = rfftfreq(int(samples), 1 / samplerate)
        centroid = np.sum(amplitude * frequency) / np.sum(amplitude)
        spread = utilitiesGUI.spectralSpread(frequency, amplitude, centroid)
        peakIndex = np.argmax(np.array(amplitude))
        peak = frequency[peakIndex]
        print("Centroid:", centroid, ", Spread:", spread, ", Peak:", peak)

    def soundDesign(self):
        for design in self.resultados:
            for instrument in design:
                print(instrument)
                audio, samplerate = utilitiesGUI.makeCut(self.path, 400)
                audio = utilitiesGUI.applyEnvelope(audio, samplerate, instrument[1], instrument[2])
                pitch = AudioEffectsChain().pitch(shift=instrument[4])
                audio = pitch(audio)

                sf.write('../Results/corte.wav', audio, samplerate, 'PCM_24')

    def getfromClingo(self):
        # ** CONFIGURAR Y CARGAR CLINGO *** #
        control = clingo.Control(utilitiesGUI.clingo_args)
        control.configuration.solve.models = 3
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

        cont = 0
        for model in models:
            resp = []
            print("Propuesta ", cont + 1)
            for atom in model:
                instrument = str(atom.arguments[0])
                attack = int(str(atom.arguments[1]))
                release = int(str(atom.arguments[2]))
                pattern = int(str(atom.arguments[3]))
                pitchShift = int(str(atom.arguments[4]))
                eq = int(str(atom.arguments[5]))
                result = []
                result.append(instrument)
                result.append(attack)
                result.append(release)
                result.append(pattern)
                result.append(pitchShift)
                result.append(eq)
                resp.append(result)
                print("Para", instrument, "aplicar:", attack, "de attack,", release, "de release,", pitchShift, "de pitch shift y", eq, "de EQ en el patrón", pattern)
            self.resultados.append(resp)
            cont += 1

app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())