from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import QTimer

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from dialog import Ui_MainWindow
from buttons import Buttons

class MainWindow(QMainWindow, Ui_MainWindow, Buttons):
    def __init__(self, data):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.data = data
        self.orig_data = data.copy()

        fig = Figure()
        axes = fig.add_subplot(111)

        canvas = FigureCanvasQTAgg(fig)
        comp_for_mpl = QVBoxLayout(self.MplWidget)
        comp_for_mpl.addWidget(canvas)

        self.axes = axes
        self.canvas = canvas

        self.draw_segments()

        self.initButtons()

        timer = QTimer(self)

    def redraw(self):
        self.canvas.draw()
        self.canvas.flush_events()

    def draw_segments(self):
        self.data.draw_segments(self.axes)
        self.redraw()
