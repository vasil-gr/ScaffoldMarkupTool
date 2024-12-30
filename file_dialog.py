from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QFileDialog, QLineEdit, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QToolBar, QMenu
from PyQt6.QtGui import QIcon, QColor, QPalette, QCursor, QPixmap, QMouseEvent, QPainter
from PyQt6.QtCore import Qt, QEvent
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
        self.btn_open = QPushButton('Find File', self)
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
                background-color:rgb(255, 87, 51);
                color: white;
                font-weight: 700;
                padding: 5px;
            }
            QPushButton:hover {
                background-color:rgb(211, 73, 42);
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
                    background-color:rgb(255, 87, 51);
                    color: white;
                    padding: 5px;
                    width: 60px;
                }

                QPushButton:hover {
                background-color:rgb(211, 73, 42);
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
        self.pixmap = QPixmap(file_path)

        self.resize(self.pixmap.width(), self.pixmap.height())

        # Сохранение текущих размеров окна
        self.normal_size = self.size()

        # Изменение цвета фона
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(147, 201, 218))
        self.setPalette(palette)

        layout = QVBoxLayout(self)

        main_layout = QHBoxLayout()

        # ToolBar
        toolbar = QToolBar("Toolbar", self)
        toolbar.setMovable(False)
        toolbar.setContentsMargins(0, 0, 0, 0)  

        # Кнопка "File" с выпадающим списком
        file_menu = QMenu("File", self)
        file_menu.addAction("New")
        file_menu.addAction("Duplicate layer")
        file_menu.addAction("Export")
        file_menu.addAction("Exit")

        file_button = QPushButton("File", self)
        file_button.setMenu(file_menu)
        file_button.setObjectName("File")
        file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(file_button)

        # Кнопка "Markup" с выпадающим списком
        markup_menu = QMenu("Markup", self)
        markup_menu.addAction("Normalise coordinates")
        markup_menu.addAction("Set dot")
        markup_menu.addAction("Remove dot")

        markup_button = QPushButton("Markup", self)
        markup_button.setMenu(markup_menu)
        markup_button.setObjectName("Markup") 
        markup_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(markup_button)

        # Кнопка "Zoom" с выпадающим списком
        zoom_menu = QMenu("Zoom", self)
        zoom_menu.addAction("Zoom In")
        zoom_menu.addAction("Zoom Out")
        # zoom_menu.addAction("Reset Zoom")
        # zoom_menu.addAction("Fit to Window")

        zoom_button = QPushButton("Zoom", self)
        zoom_button.setMenu(zoom_menu)
        zoom_button.setObjectName("Zoom")
        zoom_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(zoom_button)

        # Кнопка "Processing"
        processing_button = QPushButton("Processing", self)
        processing_button.setObjectName("Processing")
        processing_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(processing_button)

        main_layout.addWidget(toolbar)
        main_layout.addStretch()

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.minimize_button = QPushButton("_", self)
        self.minimize_button.setObjectName("minimizeButton")
        self.minimize_button.clicked.connect(self.showMinimized)
        button_layout.addWidget(self.minimize_button)

        self.fullscreen_button = QPushButton("⛶", self)
        self.fullscreen_button.setObjectName("fullscreenButton")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        button_layout.addWidget(self.fullscreen_button)

        self.close_button = QPushButton("X", self)
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        main_layout.addLayout(button_layout)
        layout.addLayout(main_layout)

        # Стили кнопок
        self.setStyleSheet("""
            /* Стили для кнопок в ToolBar */
            QPushButton#File, QPushButton#Markup, QPushButton#Zoom, QPushButton#Processing {
                background-color:rgb(255, 87, 51);
                border-radius: 5px;
                font-weight: 600;
                padding: 5px 10px;
                margin-right: 10px;
                color: white;
            }

            QPushButton#File, QPushButton#Zoom{
                width: 60px;
                color: white;
                text-align: center
            }

            QPushButton#Markup QPushButton#Processing{
                width: 120px;
                color: white;
                text-align: center
            }            

            QPushButton#File:hover, QPushButton#Markup:hover, QPushButton#Zoom:hover, QPushButton#Processing:hover {
                background-color:rgb(211, 73, 42);
            }

            /* Стили для выпадающих списков */
            QMenu {
                background-color: rgb(255, 145, 120);
                color: white;
                font-weight: 600;
                border-radius: 5px;
            }

            QMenu::item {
                padding: 5px 10px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background-color:rgb(233, 104, 75)
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

        # Отображение изображения
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(False)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

        # фильтр событий на QLabel
        self.image_label.installEventFilter(self)

        # список для хранения координат точек
        self.points = []
    
   

    # Обработка наведения мыши на изображение
    def eventFilter(self, obj, event):
        if obj == self.image_label:
            if event.type() == QEvent.Type.Enter:
                self.image_label.setCursor(Qt.CursorShape.CrossCursor)  # курсор "цель"
            elif event.type() == QEvent.Type.Leave:
                self.image_label.setCursor(Qt.CursorShape.ArrowCursor)
        return super().eventFilter(obj, event)


    # Обработка кликов мыши по изображению
    def mousePressEvent(self, event: QMouseEvent):
        click_pos = event.position()
        widget_pos = self.image_label.mapFromParent(click_pos.toPoint())

        if 0 <= widget_pos.x() < self.pixmap.width() and 0 <= widget_pos.y() < self.pixmap.height():
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:  # удаление точки: клик+Shift
                self.remove_dot(widget_pos)
            else:  # добавление точки: клик
                self.points.append((widget_pos.x(), widget_pos.y()))
                print(f"Добавлена точка: ({widget_pos.x()}, {widget_pos.y()})")
                self.add_dot()
        else:
            print("Клик вне изображения.")

    
    # Добавление точки и обновление изображения
    def add_dot(self):
        pixmap_with_points = self.pixmap.copy()
        painter = QPainter(pixmap_with_points)
        painter.setPen(Qt.GlobalColor.red)
        painter.setBrush(Qt.GlobalColor.red)

        for point in self.points:
            painter.drawEllipse(point[0] - 3, point[1] - 3, 6, 6)  # потом сделать возможность менять радиус и цвет точек

        painter.end()
        self.image_label.setPixmap(pixmap_with_points)
    

    # Удаление точки и обновление изображения
    def remove_dot(self, click_pos):
        removal_radius = 10  # поиск точки для удаления производится в определённом радиусе вокруг точки нажатия; потом можно добавить возможность менять этот радиус
        nearest_point = None
        min_distance = float('inf')

        # удаляет ближайшую
        for point in self.points:
            distance = ((point[0] - click_pos.x()) ** 2 + (point[1] - click_pos.y()) ** 2) ** 0.5
            if distance < removal_radius and distance < min_distance:
                nearest_point = point
                min_distance = distance

        if nearest_point:
            self.points.remove(nearest_point)
            print(f"Удалена точка: {nearest_point}")
            self.add_dot()
        else:
            print("Нет точки в области клика для удаления.")



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