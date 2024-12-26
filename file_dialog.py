from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QFileDialog, QLineEdit, QMessageBox
import sys
import os

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(450, 100)

        # поле ввода пути
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter file path")
        self.input_field.setGeometry(10, 50, 250, 30)

        # кнопка открытия диалогового окна
        self.btn_open = QPushButton('Open File', self)
        self.btn_open.setGeometry(270, 50, 100, 30)
        self.btn_open.clicked.connect(self.evt_btn_open_clicked)

        # кнопка ок
        self.btn_ok = QPushButton('Ok', self)
        self.btn_ok.setGeometry(380, 50, 50, 30)
        self.btn_ok.clicked.connect(self.evt_btn_ok_clicked)

    def evt_btn_open_clicked(self):
        # открытие диалогового окна для выбора файла
        res, _ = QFileDialog.getOpenFileName(self, 'Open File', '/Users/yourusername', 'Image Files (*.jpg *.jpeg *.png *.bmp)')
        if res:  # если файл выбран, записываем путь в поле ввода
            self.input_field.setText(res)

    def evt_btn_ok_clicked(self):
        # логика нажатия на кнопку ок
        file_path = self.input_field.text()
        # проверка существования файла и явлеяется ли он изображением (если да - указываем этот путь и закрываем оуно, нет - сообщение об ошибке)
        if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            print(f"File path: {file_path}")
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Path to the file does not exist or does not lead to the image.', QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())
