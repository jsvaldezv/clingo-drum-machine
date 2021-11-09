import sys
from PyQt5.QtWidgets import *
import dragAudio
import utilitiesGUI
import soundfile as sf

class Main(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 300)

        # LOAD AUDIOS #
        self.btnMix = QPushButton('Create', self)
        self.btnMix.setGeometry(10, 10, 200, 50)
        self.btnMix.clicked.connect(lambda: self.plotAudio())

        self.boxAudio = dragAudio.ListboxWidget(self)
        self.boxAudio.setPos(250, 15)

        self.makeKickPattern()

    def plotAudio(self):
        path = QListWidgetItem(self.boxAudio.item(0))
        if path.text():
            path = path.text()
            audio, samplerate = sf.read(path)
            self.chart = utilitiesGUI.Canvas(self)
            self.chart.plotAudio(audio)
            self.chart.setGeometry(10, 80, 460, 200)
            self.chart.show()

    def makeKickPattern(self):
        audio, samplerate = sf.read('../audios/kick.wav')
        kickInterval = utilitiesGUI.computeInterval(120, samplerate)
        arraY = []
        cont = 0

        print(kickInterval)
        sample1 = kickInterval
        sample2 = kickInterval * 2
        sample3 = kickInterval * 3
        sample4 = kickInterval * 4

        cont = 0
        cont2 = 0
        cont3 = 0
        cont4 = 0
        for sample in range(kickInterval * 4):
            if sample < sample1:
                if cont < len(audio):
                    arraY.append(audio[sample])
                else:
                    arraY.append(0)
                cont += 1
            elif sample >= sample1 and sample < sample2:
                if cont2 < len(audio):
                    arraY.append(audio[cont2])
                else:
                    arraY.append(0)
                cont2 += 1
            elif sample >= sample2 and sample < sample3:
                if cont3 < len(audio):
                    arraY.append(audio[cont3])
                else:
                    arraY.append(0)
                cont3 += 1
            else:
                if cont4 < len(audio):
                    arraY.append(audio[cont4])
                else:
                    arraY.append(0)
                cont4 += 1

        sf.write('../Results/Attack.wav', arraY, samplerate, 'PCM_24')

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