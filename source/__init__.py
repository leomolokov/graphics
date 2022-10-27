from PyQt5.QtWidgets import QApplication

from mainwin import MainWindow
from mydata import MyData

import sys

def main():
    data = MyData()
    data.read('tetrahedron.txt')
    app = QApplication(sys.argv)
    main = MainWindow(data)
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()