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
from pysndfx import AudioEffectsChain
from pygame import mixer


class Main(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 450)

        self.paths = []
        self.boxes = []
        self.labels = []
        self.resultsClingo = []
        self.finalCutsAudio = []
        self.checkboxes = []
        self.labels = []
        self.results = []
        self.bestLoop = []

        # Title
        self.mainLabel = QLabel(self)
        self.mainLabel.setText("SMART BUILDER")
        self.mainLabel.setFont(QFont("Nixie One", 25))
        self.mainLabel.setGeometry(int(1000 / 2 - 120), 0, 245, 50)

        # Load audios
        self.btnCreate = QPushButton("Create", self)
        self.btnCreate.setGeometry(10, 75, 100, 50)
        self.btnCreate.clicked.connect(lambda: self.startCreating())

        # Delete audios
        self.btnDel = QPushButton("Delete", self)
        self.btnDel.setGeometry(10, 135, 100, 50)
        self.btnDel.clicked.connect(lambda: self.clear())

        # Play audios
        self.play = QPushButton("Play", self)
        self.play.setGeometry(760, 71, 100, 50)
        self.play.clicked.connect(lambda: self.playSound())

        # Loops
        self.numMixes = QLabel(self)
        self.numMixes.setText("Loops:")
        self.numMixes.setFont(QFont("Nixie One", 15))
        self.numMixes.setGeometry(15, 200, 120, 30)

        self.sp = QSpinBox(self)
        self.sp.setGeometry(15, 225, 110, 30)
        self.sp.setValue(2)
        self.sp.setRange(1, 100)
        self.sp.show()

        # Bars
        self.numBeats = QLabel(self)
        self.numBeats.setText("Bars:")
        self.numBeats.setFont(QFont("Nixie One", 15))
        self.numBeats.setGeometry(15, 255, 140, 30)

        self.spBeats = QSpinBox(self)
        self.spBeats.setGeometry(15, 280, 110, 30)
        self.spBeats.setValue(2)
        self.spBeats.setRange(1, 12)
        self.spBeats.show()

        # BPM
        self.bpmLabel = QLabel(self)
        self.bpmLabel.setText("BPM:")
        self.bpmLabel.setFont(QFont("Nixie One", 15))
        self.bpmLabel.setGeometry(15, 310, 140, 30)

        self.bpm = QSpinBox(self)
        self.bpm.setGeometry(15, 335, 110, 30)
        self.bpm.setValue(120)
        self.bpm.setRange(60, 210)
        self.bpm.show()

        # Kick
        self.kickLabel = QLabel(self)
        self.kickLabel.setText("Kick:")
        self.kickLabel.setFont(QFont("Nixie One", 15))
        self.kickLabel.setGeometry(140, 40, 120, 30)
        self.labels.append("kick")

        self.boxAudio = dragAudio.ListboxWidget(self)
        self.boxAudio.setGeometry(140, 75, 100, 50)
        self.boxes.append(self.boxAudio)

        # Snare
        self.snareLabel = QLabel(self)
        self.snareLabel.setText("Snare:")
        self.snareLabel.setFont(QFont("Nixie One", 15))
        self.snareLabel.setGeometry(260, 40, 120, 30)
        self.labels.append("snare")

        self.boxAudioTwo = dragAudio.ListboxWidget(self)
        self.boxAudioTwo.setGeometry(260, 75, 100, 50)
        self.boxes.append(self.boxAudioTwo)

        # Hi hat
        self.hihatLabel = QLabel(self)
        self.hihatLabel.setText("Hi-hat:")
        self.hihatLabel.setFont(QFont("Nixie One", 15))
        self.hihatLabel.setGeometry(380, 40, 120, 30)
        self.labels.append("hihat")

        self.boxAudioThree = dragAudio.ListboxWidget(self)
        self.boxAudioThree.setGeometry(380, 75, 100, 50)
        self.boxes.append(self.boxAudioThree)

        # Text button
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(500, 75, 250, 320)

        # Image
        self.photo = QLabel(self)
        self.photo.setGeometry(140, 150, 340, 180)
        self.photo.setText("")
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")

    def clear(self):
        for box in self.boxes:
            box.clear()

    def plotAudio(self, inAudio):
        chart = utilities.Canvas(self)
        chart.plotAudio(inAudio)
        self.photo.setPixmap(QPixmap("Results/audio.png"))

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
        self.createCheckBoxes()
        self.makeAnalysis()
        self.analizeWithClingo()
        self.makePatterns()

    def getfromClingo(self):
        del self.resultsClingo[:]
        # Configure and load clingo
        control = clingo.Control(utilities.clingo_args)
        if self.sp.value() != 0:
            control.configuration.solve.models = self.sp.value()

            control.load("./Clingo/remixer.lp")
            models = []

            # Add facts to LP
            cont = 0
            for instrumento in self.boxes:
                path = QListWidgetItem(instrumento.item(0))
                if path.text():
                    name = self.labels[cont]
                    fact = "sound(" + name + ")."
                    control.add("base", [], str(fact))

                cont += 1

            # Grounding
            print("Grounding...")
            self.printText("Grounding...")
            control.ground([("base", [])])
            print("-------------")
            self.printText("-------------")

            # Solve
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
                print("Option ", cont + 1)
                self.printText("Option ".upper() + str(cont + 1))
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

                    print(
                        "For",
                        instrument,
                        "apply:",
                        attack,
                        "attack,",
                        release,
                        "release,",
                        pitchShift,
                        "pitch shift and",
                        eq,
                        "EQ in the pattern",
                        pattern,
                    )

                    self.printText(str(instrument.upper() + "..."))
                    self.printText("• Pattern " + str(pattern))
                    self.printText("• " + str(attack) + " attack")
                    self.printText("• " + str(release) + " release")
                    self.printText("• " + str(pitchShift) + " pitch shifting")
                    self.printText("• " + str(eq) + " EQ")
                    self.printText("")

                self.resultsClingo.append(resp)
                cont += 1
                print("")
                self.printText("-------------")
                self.printText("")
            print("-------------")

        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setText("You can't ask for 0 options")
            dialog.setIcon(QMessageBox.Critical)
            dialog.exec_()

    def soundDesign(self):
        cont = 0
        i = 1
        del self.finalCutsAudio[:]
        for design in self.resultsClingo:
            corte = []
            for instrument in design:
                if instrument[0] == "kick":
                    caja = self.boxes[0]
                elif instrument[0] == "snare":
                    caja = self.boxes[1]
                else:
                    caja = self.boxes[2]

                path = QListWidgetItem(caja.item(0))

                if path.text():
                    # Cut
                    audio, samplerate = utilities.makeCut(path.text(), 400)

                    # Envelop
                    audio = utilities.applyEnvelope(
                        audio, samplerate, instrument[1], instrument[2]
                    )

                    # Pitch shifting
                    pitch = AudioEffectsChain().pitch(shift=instrument[4])
                    audio = pitch(np.array(audio))

                    # EQ
                    audio = utilities.applyFilter(audio, instrument[0], instrument[5])

                    corte.append([instrument[0], audio])

                cont += 1

            cont = 0
            i += 1
            self.finalCutsAudio.append(corte)

    def makePatterns(self):
        print("-------------")
        cont = 1
        contCortes = 0
        for corte in self.finalCutsAudio:
            samplerate = 0
            samples = []

            for sample in corte:
                values = 0
                numBeats = self.spBeats.value()
                bpm = self.bpm.value()
                if sample[0] == "kick":
                    if self.resultsClingo[contCortes][0][3] == 1:
                        values, samplerate, long = patterns.makeKickPatternOne(
                            sample[1], bpm, numBeats, 44100
                        )
                    elif self.resultsClingo[contCortes][0][3] == 2:
                        values, samplerate, long = patterns.makeKickPatternTwo(
                            sample[1], bpm, numBeats, 44100
                        )
                    elif self.resultsClingo[contCortes][0][3] == 3:
                        values, samplerate, long = patterns.makeKickPatternDNB(
                            sample[1], bpm, numBeats, 44100
                        )

                elif sample[0] == "snare":
                    if self.resultsClingo[contCortes][0][3] == 1:
                        values, samplerate, long = patterns.makeSnarePatternOne(
                            sample[1], bpm, numBeats, 44100
                        )
                    elif self.resultsClingo[contCortes][0][3] == 2:
                        values, samplerate, long = patterns.makeSnarePatternTwo(
                            sample[1], bpm, numBeats, 44100
                        )
                    elif self.resultsClingo[contCortes][0][3] == 3:
                        values, samplerate, long = patterns.makeSnareDembow(
                            sample[1], bpm, numBeats, 44100
                        )

                elif sample[0] == "hihat":
                    if self.resultsClingo[contCortes][0][3] == 1:
                        values, samplerate, long = patterns.makeHatPatternOne(
                            sample[1], bpm, numBeats, 44100
                        )
                    elif self.resultsClingo[contCortes][0][3] == 2:
                        values, samplerate, long = patterns.makeHatPatternTwo(
                            sample[1], bpm, numBeats, 44100
                        )
                    elif self.resultsClingo[contCortes][0][3] == 3:
                        values, samplerate, long = patterns.makeHatPatternThree(
                            sample[1], bpm, numBeats, 44100
                        )

                samples.append(values)
            contCortes += 1

            final = []

            for cero in range(len(samples[0])):
                final.append(0)

            for ins in range(len(samples)):
                for sample in range(len(samples[0])):
                    final[sample] += samples[ins][sample]

            name = "Loop_" + str(cont)
            print(name, "created")
            sf.write("Results/" + name + ".wav", final, samplerate, "PCM_24")

            cont += 1
        print("-------------")

        kickIndex = self.bestLoop[0][1]
        hihatIndex = self.bestLoop[1][1]
        snareIndex = self.bestLoop[2][1]

        kick = self.finalCutsAudio[int(str(kickIndex)) - 1][0][1]
        hihat = self.finalCutsAudio[int(str(hihatIndex)) - 1][2][1]
        snare = self.finalCutsAudio[int(str(snareIndex)) - 1][1][1]

        kick, samplerate, long = patterns.makeKickPatternOne(
            kick, self.bpm.value(), self.spBeats.value(), 44100
        )
        hihat, samplerate, long = patterns.makeHatPatternOne(
            hihat, self.bpm.value(), self.spBeats.value(), 44100
        )
        snare, samplerate, long = patterns.makeSnarePatternOne(
            snare, self.bpm.value(), self.spBeats.value(), 44100
        )

        samples = []
        samples.append(kick)
        samples.append(hihat)
        samples.append(snare)

        final = []
        for cero in range(len(kick)):
            final.append(0)

        for ins in range(len(samples)):
            for sample in range(len(samples[0])):
                final[sample] += samples[ins][sample]

        sf.write("Results/best.wav", final, 44100, "PCM_24")

    def makeAnalysis(self):
        del self.results[:]
        print("Analisis")
        for loop in range(len(self.finalCutsAudio)):
            for corte in self.finalCutsAudio[loop]:
                amplitude = np.abs(rfft(corte[1]))
                frequency = rfftfreq(len(corte[1]), 1 / 44100)
                centroid = np.sum(amplitude * frequency) / np.sum(amplitude)
                spread = utilities.spectralSpread(frequency, amplitude, centroid)
                peakIndex = np.argmax(np.array(amplitude))
                peak = frequency[peakIndex]
                self.results.append(
                    [corte[0], loop + 1, int(centroid), int(spread), int(peak)]
                )

    def playSound(self):
        cont = 0
        maxLen = len(self.checkboxes)
        for check in self.checkboxes:
            if cont + 1 == maxLen:
                if check.isChecked() == True:
                    path = "Results/best.wav"
                    audio, sr = sf.read(path)
                    self.plotAudio(audio)
                    mixer.init()
                    sound = mixer.Sound(path)
                    sound.play()
            else:
                if check.isChecked() == True:
                    print("Playing...")
                    path = "Results/Loop_" + str(cont + 1) + ".wav"
                    audio, sr = sf.read(path)
                    self.plotAudio(audio)
                    mixer.init()
                    sound = mixer.Sound(path)
                    sound.play()

            cont += 1
        print("-------------")

    def printText(self, inText):
        cursor = self.textEdit.textCursor()
        cursor.atEnd()
        cursor.insertText(inText + "\n")

    def createCheckBoxes(self):
        yInitChecBox = 120
        yInitLabel = 120

        for check in range(len(self.checkboxes)):
            if check < len(self.checkboxes) - 1:
                globals()[f"checkBox_{check}"].hide()
                globals()[f"checkBoxLabel_{check}"].hide()
            else:
                self.checkboxes[-1].hide()
                self.labels[-1].hide()

        del self.checkboxes[:]
        del self.labels[:]

        for check in range(len(self.resultsClingo)):
            globals()[f"checkBox_{check}"] = QRadioButton(self)
            globals()[f"checkBox_{check}"].setGeometry(765, yInitChecBox, 100, 50)
            globals()[f"checkBox_{check}"].show()
            self.checkboxes.append(globals()[f"checkBox_{check}"])

            globals()[f"checkBoxLabel_{check}"] = QLabel(self)
            globals()[f"checkBoxLabel_{check}"].setGeometry(785, yInitLabel, 100, 50)
            globals()[f"checkBoxLabel_{check}"].setText("Loop " + str(check + 1))
            globals()[f"checkBoxLabel_{check}"].show()
            self.labels.append(globals()[f"checkBoxLabel_{check}"])

            yInitChecBox += 30
            yInitLabel += 30

        bestCheck = QRadioButton(self)
        bestCheck.setGeometry(765, yInitChecBox, 100, 50)
        bestCheck.show()
        self.checkboxes.append(bestCheck)

        bestCheckLabel = QLabel(self)
        bestCheckLabel.setGeometry(785, yInitLabel, 100, 50)
        bestCheckLabel.setText("Best Loop")
        bestCheckLabel.show()
        self.labels.append(bestCheckLabel)

    def analizeWithClingo(self):
        del self.bestLoop[:]

        controlAnalize = clingo.Control(utilities.clingo_args)
        controlAnalize.configuration.solve.models = 0
        controlAnalize.load("Clingo/evaluate.lp")
        models = []

        # Add facts to LP
        for instrumento in self.results:
            name = instrumento[0]
            loop = str(instrumento[1])
            centroid = str(instrumento[2])
            spread = str(instrumento[3])
            peak = str(instrumento[4])

            fact = (
                "sound("
                + name
                + ","
                + loop
                + ","
                + centroid
                + ","
                + spread
                + ","
                + peak
                + ")."
            )
            controlAnalize.add("base", [], str(fact))

        # Grounding
        print("-------------")
        print("Grounding Analize...")
        controlAnalize.ground([("base", [])])
        print("-------------")

        # Solve
        print("Solving Analize...")
        with controlAnalize.solve(yield_=True) as solve_handle:
            for model in solve_handle:
                models.append(model.symbols(shown=True))
        print("-------------")

        print(
            "The best ", models[-1][0].arguments[0], " is ", models[-1][0].arguments[1]
        )
        print(
            "The best ", models[-1][1].arguments[0], " is ", models[-1][1].arguments[1]
        )
        print(
            "The best ", models[-1][2].arguments[0], " is ", models[-1][2].arguments[1]
        )

        self.printText(
            "The best "
            + str(models[-1][0].arguments[0])
            + " is "
            + str(models[-1][0].arguments[1])
        )
        self.printText(
            "The best "
            + str(models[-1][1].arguments[0])
            + " is "
            + str(models[-1][1].arguments[1])
        )
        self.printText(
            "The best "
            + str(models[-1][2].arguments[0])
            + " is "
            + str(models[-1][2].arguments[1])
        )
        self.printText("")
        self.printText("-------------")

        self.bestLoop.append([models[-1][0].arguments[0], models[-1][0].arguments[1]])
        self.bestLoop.append([models[-1][1].arguments[0], models[-1][1].arguments[1]])
        self.bestLoop.append([models[-1][2].arguments[0], models[-1][2].arguments[1]])


app = QApplication(sys.argv)
demo = Main()
demo.show()
sys.exit(app.exec_())
