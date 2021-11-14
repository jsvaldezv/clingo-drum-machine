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
        self.resize(700, 300)

        self.paths = []
        self.cajitas = []
        self.resultadosClingo = []
        self.cortesAudiosFinales = []

        # LOAD AUDIOS #
        self.btnMix = QPushButton('Create', self)
        self.btnMix.setGeometry(10, 10, 100, 50)
        self.btnMix.clicked.connect(lambda: self.startCreating())

        # DELETE AUDIOS #
        self.btnMix = QPushButton('Delete', self)
        self.btnMix.setGeometry(10, 65, 100, 50)
        self.btnMix.clicked.connect(lambda: self.clear())

        # LOOPS #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Número de loops:")
        self.numMixes.setGeometry(10, 120, 120, 30)

        self.sp = QSpinBox(self)
        self.sp.setGeometry(10, 145, 100, 30)
        self.sp.setValue(1)
        self.sp.show()

        # KICK #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Kick:")
        self.numMixes.setGeometry(140, 15, 120, 30)

        self.boxAudio = dragAudio.ListboxWidget(self)
        #self.boxAudio.setPos(120, 15)
        self.boxAudio.setGeometry(140, 50, 100, 50)
        self.cajitas.append(self.boxAudio)

        # SNARE #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Snare:")
        self.numMixes.setGeometry(260, 15, 120, 30)

        self.boxAudioTwo = dragAudio.ListboxWidget(self)
        #self.boxAudioTwo.setPos(350, 15)
        self.boxAudioTwo.setGeometry(260, 50, 100, 50)
        self.cajitas.append(self.boxAudioTwo)

        # HI-HAT #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Hi-hat:")
        self.numMixes.setGeometry(380, 15, 120, 30)

        self.boxAudioThree = dragAudio.ListboxWidget(self)
        #self.boxAudioThree.setPos(350, 15)
        self.boxAudioThree.setGeometry(380, 50, 100, 50)
        self.cajitas.append(self.boxAudioThree)

    def clear(self):
        for box in self.cajitas:
            box.clear()

    def plotAudio(self):
        cont = 0
        for item in self.cajitas:
            caja = QListWidgetItem(item.item(0))
            if caja.text():
                self.paths.append(caja.text())
                track, samplerate = sf.read(self.paths[cont])
                globals()['string%s' % + cont] = utilities.Canvas(self)
                globals()['string%s' % + cont].plotAudio(track)
                globals()['string%s' % + cont].setGeometry(cont+200, 80, 200, 150)
                globals()['string%s' % + cont].show()
                print(globals()['string%s' % + cont])

            cont += 1

        print(self.paths)

        print("-------------")
        print("Audio plotted")
        print("-------------")

    def startCreating(self):
        #self.plotAudio()
        self.getfromClingo()
        self.soundDesign()
        self.makePatterns()
        #self.makeAnalysis(loop, duration, samplerate)

    def getfromClingo(self):
        del self.resultadosClingo[:]
        # ** CONFIGURAR Y CARGAR CLINGO *** #
        control = clingo.Control(utilities.clingo_args)
        if self.sp.value() != 0:
            control.configuration.solve.models = self.sp.value()

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
                    print("Para", instrument, "aplicar:", attack, "de attack,", release, "de release,", pitchShift,
                          "de pitch shift y", eq, "de EQ en el patrón", pattern)
                self.resultadosClingo.append(resp)
                cont += 1
                print("")
            print("-------------")

        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setText("No puedes pedir 0 propuestas")
            dialog.setIcon(QMessageBox.Critical)
            dialog.exec_()

    def soundDesign(self):
        cont = 0
        i = 1
        for design in self.resultadosClingo:
            corte = []
            for instrument in design:
                caja = self.cajitas[cont]
                path = QListWidgetItem(caja.item(0))

                #if path.text():
                # CUT
                audio, samplerate = utilities.makeCut(path.text(), 400)
                # ENVELOPE
                audio = utilities.applyEnvelope(audio, samplerate, instrument[1], instrument[2])
                # PITCH SHIFTING
                pitch = AudioEffectsChain().pitch(shift=instrument[4])
                audio = pitch(np.array(audio))
                # EQ
                audio = utilities.applyFilter(audio, instrument[0], instrument[5])
                # WRITE
                name = instrument[0] + '_' + str(i)
                sf.write('../Results/' + name + '.wav', audio, samplerate, 'PCM_24')

                corte.append([instrument[0], audio])

                cont += 1
            cont = 0
            i += 1
            self.cortesAudiosFinales.append(corte)

    def makePatterns(self):
        cont = 1
        #print(self.cortesAudiosFinales)
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
            print(name, "creado")
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