from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QFileDialog, QLineEdit, QMessageBox, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QToolBar
from PyQt6.QtGui import QIcon, QColor, QPalette, QCursor, QPixmap
from PyQt6.QtCore import Qt
import sys
import os

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScaffoldMarkupTool")
        self.setWindowIcon(QIcon("./icon2.png"))  
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
            self.open_image_window(file_path)
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

    def open_image_window(self, file_path):
        image_window = ImageWindow(file_path)
        image_window.exec()

        
class ImageWindow(QDialog):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("ScaffoldMarkupTool")
        self.setWindowIcon(QIcon("./icon2.png"))  
        pixmap = QPixmap(file_path)

        self.resize(pixmap.width(), pixmap.height())

        # Сохранение текущих размеров окна
        self.normal_size = self.size()

        # Изменение цвета фона
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(147, 201, 218))
        self.setPalette(palette)

        layout = QVBoxLayout(self)

        # Создание кастомного заголовка
        title_bar = QWidget(self)
        title_bar_layout = QHBoxLayout(title_bar)

        # Создание ToolBar
        toolbar = QToolBar("Toolbar", self)
        toolbar.setMovable(False)
        toolbar.setContentsMargins(0, 0, 0, 0)  
        for name in ["Файл", "Разметка", "Zoom", "Обработка"]:
            button = QPushButton(name, self)
            button.setObjectName(name)
            toolbar.addWidget(button)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        title_bar_layout.addWidget(toolbar)
        title_bar_layout.addStretch()

        # Кнопки управления
        self.minimize_button = QPushButton("_", self)
        self.minimize_button.setObjectName("minimizeButton")
        self.minimize_button.clicked.connect(self.showMinimized)
        title_bar_layout.addWidget(self.minimize_button)

        self.fullscreen_button = QPushButton("⛶", self)
        self.fullscreen_button.setObjectName("fullscreenButton")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        title_bar_layout.addWidget(self.fullscreen_button)

        self.close_button = QPushButton("X", self)
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)
        title_bar_layout.addWidget(self.close_button)

        self.minimize_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.fullscreen_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


        # Стили кнопок
        self.setStyleSheet("""
            /* Стили для кнопок в ToolBar */
            QPushButton#Файл, QPushButton#Разметка, QPushButton#Zoom, QPushButton#Обработка {
                background-color: #FF5733;
                border-radius: 5px;
                color: white;
                font-weight: 600;
                padding: 5px 10px;
                margin-right: 10px;
            }

            QPushButton#Файл:hover, QPushButton#Разметка:hover, QPushButton#Zoom:hover, QPushButton#Обработка:hover {
                background-color: #C70039;
            }

            /* Стили для кнопок управления */
            QPushButton#minimizeButton, QPushButton#fullscreenButton {
                background-color: #007BFF;
                color: white;
                font-weight: 700;
                border-radius: 5px;
                padding: 5px;
                width: 30px;
            }

            QPushButton#closeButton{
                background-color:rgb(255, 0, 4);
                color: white;
                font-weight: 700;
                border-radius: 5px;
                padding: 5px;
                width: 30px;
            }

            QPushButton#minimizeButton:hover, QPushButton#fullscreenButton:hover{
                background-color: #0056b3;
            }

            QPushButton#closeButton:hover {
                background-color: rgb(196, 6, 10);
            }

        """)

        layout.addWidget(title_bar)

        # Отображение изображения
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(file_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(False)  # Масштабировать содержимое окна
        layout.addWidget(image_label)

        self.setLayout(layout)

    # Полноэкранный режим
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.resize(self.normal_size)
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(screen_geometry)
            self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())