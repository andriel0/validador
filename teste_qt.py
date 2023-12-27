import sys
from PyQt5 import QtWidgets

class QDataViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Layout Init.
        self.setGeometry(650, 300, 600, 600)
        self.setWindowTitle('Data Viewer')
        self.quitButton = QtWidgets.QPushButton('QUIT', self)
        self.uploadButton = QtWidgets.QPushButton('UPLOAD', self)
        self.downloadButton = QtWidgets.QPushButton('DOWNLOAD', self)

        hBoxLayout = QtWidgets.QHBoxLayout()
        hBoxLayout.addWidget(self.quitButton)
        hBoxLayout.addWidget(self.uploadButton)
        self.setLayout(hBoxLayout)
        # Signal Init.
        self.quitButton.clicked.connect(QtWidgets.QApplication.quit)
        self.uploadButton.clicked.connect(self.open)
        self.downloadButton.clicked.connect(self.save)

    def open(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        print('Path file:', filename, _)

    def save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.')
        print('Save file as:', filename)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = QDataViewer()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()