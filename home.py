from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from valid_1 import Ui_Home
from valid_2 import Ui_Validacao
from back import Validator


class Home(QMainWindow, Ui_Validacao):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.upload.clicked.connect(self.get_path)

    def get_path(self):
        if self.dropdown.currentIndex() == 0 or self.num_cod.text() in ['', '0']:
            return
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        try:
            val = Validator(filename, self.num_cod.text(), self.dropdown.currentIndex())
            val.pat_to_csv()
            val.csv_to_df()
            val.get_json()
            val.relationship_cols()
        except:
            print('ERRO')
            return


def main():
    app = QApplication([])
    window = Home()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()