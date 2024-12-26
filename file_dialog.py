from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt6.QtGui import QIcon, QColor, QPalette, QCursor
from PyQt6.QtCore import Qt
import sys
import os

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScaffoldMarkupTool")  # Установка заголовка окна
        self.setWindowIcon(QIcon("./icon2.png"))  # Установка иконки окна
        self.resize(450, 100)

        # Изменение цвета фона
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(147, 201, 218))  # Цвет фона
        self.setPalette(palette)

        # Поле ввода пути
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter file path")
        self.input_field.setGeometry(10, 50, 250, 30)

        # Кнопка открытия диалогового окна
        self.btn_open = QPushButton('Open File', self)
        self.btn_open.setGeometry(270, 50, 100, 30)
        self.btn_open.clicked.connect(self.evt_btn_open_clicked)
        self.btn_open.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Указатель при наведении

        # Кнопка ОК
        self.btn_ok = QPushButton('OK', self)
        self.btn_ok.setGeometry(380, 50, 50, 30)
        self.btn_ok.clicked.connect(self.evt_btn_ok_clicked)
        self.btn_ok.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Указатель при наведении

        # Стили кнопок
        self.setStyleSheet("""
            QDialog {
                border-radius: 50px;
            }
            QLineEdit {
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QPushButton {
                border-radius: 5px;
                background-color: #FF5733;
                color: white;
                font-weight: 700;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #C70039;
            }
        """)

    def evt_btn_open_clicked(self):
        # Открытие диалогового окна для выбора файла
        res, _ = QFileDialog.getOpenFileName(self, 'Open File', '/Users/yourusername', 'Image Files (*.jpg *.jpeg *.png *.bmp)')
        if res:  # Если файл выбран, записываем путь в поле ввода
            self.input_field.setText(res)

    def evt_btn_ok_clicked(self):
        file_path = self.input_field.text()
        if os.path.isfile(file_path) and file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            print(f"File path: {file_path}")
            self.close()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Error')
            msg_box.setText('Path to the file does not exist or does not lead to the image!')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

            # Стили
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: rgba(147, 201, 218, 255);
                }
                QLabel {
                    color: Black;
                    font-weight: 700;
                    text-align: center;
                }
                QPushButton {
                    border-radius: 5px;
                    background-color: #FF5733;
                    color: white;
                    padding: 5px;
                    width: 60px;
                }
                QPushButton:hover {
                background-color: #C70039;
                }
            """)
            ok_button = msg_box.button(QMessageBox.StandardButton.Ok)
            ok_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            msg_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())