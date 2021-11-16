import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import dragAudio
import utilities
import patterns
import soundfile as sf
import clingo
from scipy.fft import rfft, rfftfreq
import numpy as np
import playsound
from pysndfx import AudioEffectsChain

class Main(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.resize(1000, 450)

        self.paths = []
        self.cajitas = []
        self.labels = []
        self.resultadosClingo = []
        self.cortesAudiosFinales = []
        self.objetosCheckboxes = []

        # TITLE #
        self.mainLabel = QLabel(self)
        self.mainLabel.setText("SMART BUILDER")
        self.mainLabel.setFont(QFont('Arial', 30))
        self.mainLabel.setGeometry(int(1000/2 - 120), 0, 245, 50)

        # LOAD AUDIOS #
        self.btnMix = QPushButton('Create', self)
        self.btnMix.setGeometry(10, 40, 100, 50)
        self.btnMix.clicked.connect(lambda: self.startCreating())

        # DELETE AUDIOS #
        self.btnMix = QPushButton('Delete', self)
        self.btnMix.setGeometry(10, 95, 100, 50)
        self.btnMix.clicked.connect(lambda: self.clear())

        # PLAY AUDIOS #
        self.play = QPushButton('Play', self)
        self.play.setGeometry(10, 150, 100, 50)
        self.play.clicked.connect(lambda: self.playSound())

        # LOOPS #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Loops:")
        self.numMixes.setGeometry(15, 200, 120, 30)

        self.sp = QSpinBox(self)
        self.sp.setGeometry(15, 225, 110, 30)
        self.sp.setValue(1)
        self.sp.setRange(1, 100)
        self.sp.show()

        # COMPASES #
        self.numCompases = QLabel(self)
        self.numCompases.setText("Compases:")
        self.numCompases.setGeometry(15, 255, 140, 30)

        self.spCompases = QSpinBox(self)
        self.spCompases.setGeometry(15, 280, 110, 30)
        self.spCompases.setValue(4)
        self.spCompases.setRange(1, 12)
        self.spCompases.show()

        # BPM #
        self.bpmLabel = QLabel(self)
        self.bpmLabel.setText("BPM:")
        self.bpmLabel.setGeometry(15, 310, 140, 30)

        self.bpm = QSpinBox(self)
        self.bpm.setGeometry(15, 335, 110, 30)
        self.bpm.setValue(120)
        self.bpm.setRange(60, 210)
        self.bpm.show()

        # KICK #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Kick:")
        self.numMixes.setGeometry(140, 40, 120, 30)
        self.labels.append("kick")

        self.boxAudio = dragAudio.ListboxWidget(self)
        self.boxAudio.setGeometry(140, 75, 100, 50)
        self.cajitas.append(self.boxAudio)

        # SNARE #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Snare:")
        self.numMixes.setGeometry(260, 40, 120, 30)
        self.labels.append("snare")

        self.boxAudioTwo = dragAudio.ListboxWidget(self)
        self.boxAudioTwo.setGeometry(260, 75, 100, 50)
        self.cajitas.append(self.boxAudioTwo)

        # HI-HAT #
        self.numMixes = QLabel(self)
        self.numMixes.setText("Hi-hat:")
        self.numMixes.setGeometry(380, 40, 120, 30)
        self.labels.append("hihat")

        self.boxAudioThree = dragAudio.ListboxWidget(self)
        self.boxAudioThree.setGeometry(380, 75, 100, 50)
        self.cajitas.append(self.boxAudioThree)

        # TEXT BUTTON #
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(500, 50, 250, 320)

    def clear(self):
        for box in self.cajitas:
            box.clear()

    def plotAudio(self, inAudio):
        chart = utilities.Canvas(self)
        chart.plotAudio(inAudio)
        chart.setGeometry(140, 150, 340, 180)
        chart.show()

    def startCreating(self):
        print("---------------------------------------------------------")
        print("Starting...")
        print("-------------")
        self.textEdit.clear()
        self.printText("-------------")
        self.printText("Starting...")
        self.printText("-------------")

        self.getfromClingo()
        self.soundDesign()
        self.makePatterns()
        self.createCheckBoxes()
        #self.makeAnalysis(loop, duration, samplerate)

    def getfromClingo(self):
        del self.resultadosClingo[:]
        # ** CONFIGURAR Y CARGAR CLINGO *** #
        control = clingo.Control(utilities.clingo_args)
        if self.sp.value() != 0:
            control.configuration.solve.models = self.sp.value()

            control.load("../Clingo/remixer.lp")
            models = []

            # **** AÑADIR HECHOS A LP ***** #
            cont = 0
            for instrumento in self.cajitas:
                path = QListWidgetItem(instrumento.item(0))
                if path.text():
                    name = self.labels[cont]
                    fact = "sound(" + name + ")."
                    control.add("base", [], str(fact))

                cont += 1

            # ** GROUNDING *** #
            print("Grounding...")
            self.printText("Grounding...")
            control.ground([("base", [])])
            print("-------------")
            self.printText("-------------")

            # ** SOLVE *** #
            print("Solving...")
            self.printText("Solving...")
            with control.solve(yield_=True) as solve_handle:
                for model in solve_handle:
                    models.append(model.symbols(shown=True))
            print("-------------")
            self.printText("-------------")

            cont = 0
            for model in models:
                resp = []
                print("Propuesta ", cont + 1)
                self.printText("Propuesta ".upper() + str(cont + 1))
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

                    self.printText(str(instrument.upper() + "..."))
                    self.printText("• Patrón " + str(pattern))
                    self.printText("• " + str(attack) + " de attack")
                    self.printText("• " + str(release) + " de release")
                    self.printText("• " + str(pitchShift) + " de pitch shifting")
                    self.printText("• " + str(eq) + " de EQ")

                    self.printText("")
                self.resultadosClingo.append(resp)
                cont += 1
                print("")
                self.printText("-------------")
                self.printText("")
            print("-------------")
            #self.printText("-------------")

        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setText("No puedes pedir 0 propuestas")
            dialog.setIcon(QMessageBox.Critical)
            dialog.exec_()

    def soundDesign(self):
        cont = 0
        i = 1
        del self.cortesAudiosFinales[:]
        for design in self.resultadosClingo:
            corte = []
            for instrument in design:

                if instrument[0] == 'kick':
                    caja = self.cajitas[0]
                elif instrument[0] == 'snare':
                    caja = self.cajitas[1]
                else:
                    caja = self.cajitas[2]

                #caja = self.cajitas[cont]
                path = QListWidgetItem(caja.item(0))

                if path.text():
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
                    #name = instrument[0] + '_' + str(i)
                    #sf.write('../Results/' + name + '.wav', audio, samplerate, 'PCM_24')

                    corte.append([instrument[0], audio])

                cont += 1

            cont = 0
            i += 1
            self.cortesAudiosFinales.append(corte)

    def makePatterns(self):
        cont = 1
        contCortes = 0
        for corte in self.cortesAudiosFinales:
            samplerate = 0
            samples = []

            for sample in corte:
                values = 0
                numCompases = self.spCompases.value()
                bpm = self.bpm.value()
                if sample[0] == 'kick':
                    if self.resultadosClingo[contCortes][0][3] == 1:
                        values, samplerate, long = patterns.makeKickPatternOne(sample[1], bpm, numCompases, 44100)
                    elif self.resultadosClingo[contCortes][0][3] == 2:
                        values, samplerate, long = patterns.makeKickPatternTwo(sample[1], bpm, numCompases, 44100)
                    elif self.resultadosClingo[contCortes][0][3] == 3:
                        values, samplerate, long = patterns.makeKickPatternDNB(sample[1], bpm, numCompases, 44100)

                elif sample[0] == 'snare':
                    if self.resultadosClingo[contCortes][0][3] == 1:
                        values, samplerate, long = patterns.makeSnarePatternOne(sample[1], bpm, numCompases, 44100)
                    elif self.resultadosClingo[contCortes][0][3] == 2:
                        values, samplerate, long = patterns.makeSnarePatternTwo(sample[1], bpm, numCompases, 44100)
                    elif self.resultadosClingo[contCortes][0][3] == 3:
                        values, samplerate, long = patterns.makeSnareDembow(sample[1], bpm, numCompases, 44100)

                elif sample[0] == 'hihat':
                    if self.resultadosClingo[contCortes][0][3] == 1:
                        values, samplerate, long = patterns.makeHatPatternOne(sample[1], bpm, numCompases, 44100)
                    elif self.resultadosClingo[contCortes][0][3] == 2:
                        values, samplerate, long = patterns.makeHatPatternTwo(sample[1], bpm, numCompases, 44100)
                    elif self.resultadosClingo[contCortes][0][3] == 3:
                        values, samplerate, long = patterns.makeHatPatternThree(sample[1], bpm, numCompases, 44100)

                samples.append(values)
            contCortes += 1

            final = []

            for cero in range(len(samples[0])):
                final.append(0)

            for ins in range(len(samples)):
                for sample in range(len(samples[0])):
                    final[sample] += samples[ins][sample]

            name = 'Loop_' + str(cont)
            print(name, "creado")
            sf.write('../Results/' + name + '.wav', final, samplerate, 'PCM_24')

            #if cont == 1:
            #    self.plotAudio(final)

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

    def playSound(self):
        cont = 0
        for check in self.objetosCheckboxes:
            if check.isChecked() == True:
                print("Playing...")
                path = "../Results/Loop_" + str(cont+1) + ".wav"
                audio, sr = sf.read(path)
                self.plotAudio(audio)
                playsound.playsound(path)

                '''import threading
                thread = threading.Thread(target=self.plotAudio(audio))
                thread.start()
                thread.join()
                playsound.playsound(path)'''

            cont += 1
        print("-------------")

    def printText(self, inText):
        cursor = self.textEdit.textCursor()
        cursor.atEnd()
        cursor.insertText(inText + "\n")

    def createCheckBoxes(self):
        yInitChecBox = 0
        yInitLabel = 0

        for check in range(len(self.objetosCheckboxes)):
            globals()[f"checkBox_{check}"].hide()
            globals()[f"checkBoxLabel_{check}"].hide()

        del self.objetosCheckboxes[:]

        for check in range(len(self.resultadosClingo)):
            globals()[f"checkBox_{check}"] = QCheckBox(self)
            globals()[f"checkBox_{check}"].setGeometry(780, yInitChecBox, 100, 50)
            globals()[f"checkBox_{check}"].show()
            self.objetosCheckboxes.append(globals()[f"checkBox_{check}"])

            globals()[f"checkBoxLabel_{check}"] = QLabel(self)
            globals()[f"checkBoxLabel_{check}"].setGeometry(800, yInitLabel, 100, 50)
            globals()[f"checkBoxLabel_{check}"].setText("Loop "+str(check+1))
            globals()[f"checkBoxLabel_{check}"].show()

            yInitChecBox += 30
            yInitLabel += 30


app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())