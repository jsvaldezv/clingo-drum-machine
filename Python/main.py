import sys
from PyQt5.QtWidgets import *
import dragAudio
import utilities
import patterns
import soundfile as sf
import clingo
from scipy.fft import rfft, rfftfreq
import numpy as np
from pysndfx import AudioEffectsChain

class Main(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 300)

        self.path = "none"
        self.resultadosClingo = []
        self.cortesAudiosFinales = []

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
            self.chart = utilities.Canvas(self)
            self.chart.plotAudio(audio)
            self.chart.setGeometry(10, 80, 460, 200)
            self.chart.show()
        print("-------------")
        print("Audio plotted")
        print("-------------")

    def startCreating(self):
        self.plotAudio()
        self.getfromClingo()
        self.soundDesign()
        self.makePatterns()
        #self.makeAnalysis(loop, duration, samplerate)

    def getfromClingo(self):
        # ** CONFIGURAR Y CARGAR CLINGO *** #
        control = clingo.Control(utilities.clingo_args)
        control.configuration.solve.models = 1
        control.load("../Clingo/remixer.lp")
        models = []

        # ** GROUNDING *** #
        print("Grounding...")
        control.ground([("base", [])])
        print("-------------")

        # ** SOLVE *** #
        print("Solving...")
        with control.solve(yield_=True) as solve_handle:
            for model in solve_handle:
                models.append(model.symbols(shown=True))
        print("-------------")

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
            self.resultadosClingo.append(resp)
            cont += 1
        print("-------------")

    def soundDesign(self):

        cont = 1
        for design in self.resultadosClingo:
            corte = []
            for instrument in design:
                # CUT
                audio, samplerate = utilities.makeCut(self.path, 400)
                # ENVELOPE
                audio = utilities.applyEnvelope(audio, samplerate, instrument[1], instrument[2])
                # PITCH SHIFTING
                pitch = AudioEffectsChain().pitch(shift=instrument[4])
                audio = pitch(np.array(audio))
                # EQ
                audio = utilities.applyFilter(audio, instrument[0], instrument[5])
                # WRITE
                name = instrument[0] + '_' + str(cont)
                sf.write('../Results/' + name + '.wav', audio, samplerate, 'PCM_24')

                corte.append([instrument[0], audio])

            self.cortesAudiosFinales.append(corte)
            cont += 1

    def makePatterns(self):
        cont = 1
        for corte in self.cortesAudiosFinales:
            samplerate = 0
            pattern = []
            kick, snare, hihat = [], [], []

            for sample in corte:

                if sample[0] == 'kick':
                    if self.resultadosClingo[0][0][3] == 1:
                        kick, samplerate, long = patterns.makeKickPatternOne(sample[1], 120, 4, 44100)
                    elif self.resultadosClingo[0][0][3] == 2:
                        kick, samplerate, long = patterns.makeKickPatternTwo(sample[1], 120, 4, 44100)

                elif sample[0] == 'snare':
                    if self.resultadosClingo[0][0][3] == 1:
                        snare, samplerate, long = patterns.makeSnarePatternOne(sample[1], 120, 4, 44100)
                    elif self.resultadosClingo[0][0][3] == 2:
                        snare, samplerate, long = patterns.makeSnarePatternTwo(sample[1], 120, 4, 44100)

                elif sample[0] == 'hihat':
                    if self.resultadosClingo[0][0][3] == 1:
                        hihat, samplerate, long = patterns.makeHatPatternOne(sample[1], 120, 4, 44100)
                    elif self.resultadosClingo[0][0][3] == 2:
                        hihat, samplerate, long = patterns.makeHatPatternTwo(sample[1], 120, 4, 44100)

            for sample in range(len(kick)):
                sampleSum = kick[sample] + snare[sample] + hihat[sample]
                pattern.append(sampleSum)

            name = 'Loop_' + str(cont)
            sf.write('../Results/' + name + '.wav', pattern, samplerate, 'PCM_24')
            cont += 1

    def makeAnalysis(self, audio, duration, samplerate):
        samples = duration * samplerate
        amplitude = np.abs(rfft(audio))
        frequency = rfftfreq(int(samples), 1 / samplerate)
        centroid = np.sum(amplitude * frequency) / np.sum(amplitude)
        spread = utilities.spectralSpread(frequency, amplitude, centroid)
        peakIndex = np.argmax(np.array(amplitude))
        peak = frequency[peakIndex]
        print("Centroid:", centroid, ", Spread:", spread, ", Peak:", peak)


app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())
