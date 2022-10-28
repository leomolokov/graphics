from dialog import Ui_MainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer

class Buttons():
    def initButtons(self):
        self.DrawSourceButton.clicked.connect(self.draw_source_call)
        self.ParallelTransfButton.clicked.connect(self.transfer)
        self.ScaleButton.clicked.connect(self.scale)
        self.RotateButton.clicked.connect(self.rotate)
        self.ShiftButton.clicked.connect(self.scew)
        self.OppButton.clicked.connect(self.opp)
        self.FullFitButton.clicked.connect(self.fit)
        self.BackButton.clicked.connect(self.roll_back)

        # self.ConstSpinButton.pressed.connect(self.espin_press)
        # self.ConstSpinButton.released.connect(self.espin_release)

        self.ConstSpinButton.stateChanged.connect(self.check_espin)

        self.DrawFacetsButton.clicked.connect(self.draw_facets)
        self.VisibilityButton.clicked.connect(self.show_visibles)

    def draw_source_call(self):
        self.draw_segments()

    def transfer(self):
        self.data.paral_transf(self.aEdit.value(),
                        self.bEdit.value(),
                        self.cEdit.value())
        self.draw_source_call()

    def scale(self):
        self.data.scale_x(self.kxEdit.value())
        self.data.scale_y(self.kyEdit.value())
        self.data.scale_z(self.kzEdit.value())
        self.draw_source_call()

    def rotate(self):
        self.data.rot_around_x(self.axEdit.value())
        self.data.rot_around_y(self.ayEdit.value())
        self.data.rot_around_z(self.azEdit.value())
        self.draw_source_call()

    def scew(self):
        self.data.scew_x_along_y(self.xyEdit.value())
        self.data.scew_x_along_z(self.xzEdit.value())
        self.data.scew_y_along_x(self.yxEdit.value())
        self.data.scew_y_along_z(self.yzEdit.value())
        self.data.scew_z_along_x(self.zxEdit.value())
        self.data.scew_z_along_y(self.zyEdit.value())
        self.draw_source_call()

    def opp(self):
        self.data.opp_focal_x(self.fxEdit.value())
        self.data.opp_focal_y(self.fyEdit.value())
        self.data.opp_focal_z(self.fzEdit.value())
        self.draw_source_call()

    def fit(self):
        self.data.fullfit()
        self.draw_source_call()

    def roll_back(self):
        self.data = self.orig_data.copy()
        self.draw_source_call()

    def spin_around_e(self):
        from math import sqrt, acos, degrees
        import time

        def len_v(vect):
            len_v = sqrt(vect[0] ** 2 + vect[1] ** 2 + vect[2] ** 2)
            return len_v

        def mult_M(M, N):
            result = 0
            for i in range(3):
                result += M[i] * N[i]
            return result

        e = [self.exEdit.value(), self.eyEdit.value(), self.ezEdit.value()]
        e_zy = [0, self.eyEdit.value(), self.ezEdit.value()]
        oz = [0, 0, 1]
        ox = [1, 0, 0]
        try:
            beta = degrees(acos(mult_M(e_zy, oz) / (len_v(e_zy) * len_v(oz))))
        except ZeroDivisionError:
            beta = 0
        self.data.rot_around_x(beta)
        try:
            gamma = 90 - degrees(acos(mult_M(e, ox) / (len_v(e) * len_v(ox))))
        except ZeroDivisionError:
            gamma = 0
        self.data.rot_around_y(-gamma)
        self.data.rot_around_z(1)
        self.data.rot_around_y(gamma)
        self.data.rot_around_x(-beta)

    def perm_spin(self):
        self.spin_around_e()
        self.draw_source_call()

    # def espin_press(self):
    #     timer = QTimer()
    #     self.timer = timer
    #     timer.timeout.connect(self.perm_spin)
    #     timer.start(100)
    #
    # def espin_release(self):
    #     if self.timer is None:
    #         return
    #     self.timer.stop()
    #     self.timer = None

    def check_espin(self, state):
        if state == 2:
            timer = QTimer()
            self.timer = timer
            timer.timeout.connect(self.perm_spin)
            timer.start(self.SpeedSlider.value())
        else:
            if self.timer is None:
                return
            self.timer.stop()
            self.timer = None

    def show_visibles(self):
      self.data.define_visibility(self.axes)
      self.data.draw_facets()