import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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