import save_res

from PyQt6.QtGui import QIcon, QColor, QPalette, QCursor, QPixmap, QMouseEvent, QPainter, QAction
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QFileDialog, QLineEdit, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QToolBar, QMenu, QScrollArea
from PyQt6.QtCore import Qt, QEvent
import sys
import os
import json
import zipfile

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
            self.close()
            self.open_image_window(file_path)

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
        self.pixmap_original = QPixmap(file_path)
        self.pixmap = self.pixmap_original.copy() # копия для применения масштабирования
        self.folder_path = os.path.dirname(file_path) # директория файла (понадобится при сохранении)
        self.file_name = os.path.splitext(os.path.basename(file_path))[0] # имя файла (понадобится при сохранении)

        # Предельные размеры окна (не больше 0.8 от экрана)
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        screen_width, screen_height = screen_geometry.width(), screen_geometry.height()
        max_window_width = int(screen_width * 0.8)
        max_window_height = int(screen_height * 0.8)
        frame_width = 25  # рамки по высоте
        frame_height = 60  # рамки по ширине
        # Устанавливаем размер окна: по размеру изображения, если оно вместе с рамками меньше предельных размеров
        window_width = min(self.pixmap.width() + frame_width, max_window_width)
        window_height = min(self.pixmap.height() + frame_height, max_window_height)
        self.resize(window_width, window_height)
        # Сохранение текущих размеров окна
        self.normal_size = self.size()

        # Полосы прокрутки
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(False) # изображение сверху-слева
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.image_label) # если изображение больше окна, появятся полосы прокрутки.

        # Поддержка масштабирования
        self.scale_factor = 1.0
        self.min_scale_factor = 0.2 # мин масштаб
        self.max_scale_factor = 5.0 # макс масштаб 

        # Изменение цвета фона
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(147, 201, 218))
        self.setPalette(palette)

        # ToolBar
        main_layout = QHBoxLayout()
        toolbar = QToolBar("Toolbar", self)
        toolbar.setMovable(False)
        toolbar.setContentsMargins(0, 0, 0, 0)  

        # Кнопка "File" с выпадающим списком
        file_menu = QMenu("File", self)
        file_menu.addAction("Open project").triggered.connect(self.open_project)
        duplicate_action = QAction("Duplicate layer", self)
        duplicate_action.triggered.connect(self.duplicate_layer)
        file_menu.addAction(duplicate_action)
        # подменю сохранения
        save_menu = QMenu("Save", self)

        save_menu.addAction("Markup image (png)").triggered.connect(
            lambda: save_res.save_markup_image(self.folder_path, self.file_name, self.pixmap, self.points)
        )
        save_menu.addAction("Markup only (png)").triggered.connect(
            lambda: save_res.save_markup_only(self.folder_path, self.file_name, self.pixmap, self.points)
        )
        save_menu.addAction("Points (json)").triggered.connect(
            lambda: save_res.save_points(self.folder_path, self.file_name, self.pixmap, self.points)
        )
        save_menu.addAction("Project (zip)").triggered.connect(
            lambda: save_res.save_project(self.folder_path, self.file_name, self.pixmap, self.points)
        )
        file_menu.addMenu(save_menu)
        file_menu.addAction("Exit")

        file_button = QPushButton("File", self)
        file_button.setMenu(file_menu)
        file_button.setObjectName("File")
        file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(file_button)

        # Кнопка "Edit" с выпадающим списком
        edit_menu = QMenu("Edit", self)
        edit_menu.addAction("Remove last dot").triggered.connect(self.remove_last_dot)
        edit_menu.addAction("Restore last dot").triggered.connect(self.restore_last_dot)

        edit_button = QPushButton("Edit", self)
        edit_button.setMenu(edit_menu)
        edit_button.setObjectName("Edit") 
        edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(edit_button)

        # Кнопка "Zoom" с выпадающим списком
        zoom_menu = QMenu("Zoom", self)
        zoom_menu.addAction("Zoom in").triggered.connect(self.zoom_in)  
        zoom_menu.addAction("Zoom out").triggered.connect(self.zoom_out)
        zoom_menu.addAction("Reset zoom").triggered.connect(self.reset_zoom)
        # zoom_menu.addAction("Fit to Window")

        zoom_button = QPushButton("Zoom", self)
        zoom_button.setMenu(zoom_menu)
        zoom_button.setObjectName("Zoom")
        zoom_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(zoom_button)

        
        # Кнопка "Settings" с выпадающим списком
        settings_menu = QMenu("Settings", self)
        # подменю выбора размера точек
        size_menu = QMenu("Size", self)
        size_menu.addAction("Small (2px)").triggered.connect(lambda: self.set_point_size(2))
        size_menu.addAction("Standard (3px)").triggered.connect(lambda: self.set_point_size(3))
        size_menu.addAction("Large (5px)").triggered.connect(lambda: self.set_point_size(5))
        self.point_radius = 3 # стартовый размер точек
        settings_menu.addMenu(size_menu)

        settings_button = QPushButton("Settings", self)
        settings_button.setMenu(settings_menu)
        settings_button.setObjectName("Settings")
        settings_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toolbar.addWidget(settings_button)


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


        # Устанавливаем компоновку
        layout = QVBoxLayout(self)
        layout.addLayout(main_layout) # тулбар (меню), вверху
        layout.addWidget(self.scroll_area) # прокручиваемая область с изображением, снизу
        self.setLayout(layout)


        # Стили кнопок
        self.setStyleSheet("""
            /* Стили для кнопок в ToolBar */
            QPushButton#File, QPushButton#Edit, QPushButton#Zoom, QPushButton#Settings {
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

            QPushButton#Edit QPushButton#Settings{
                width: 120px;
                color: white;
                text-align: center
            }            

            QPushButton#File:hover, QPushButton#Edit:hover, QPushButton#Zoom:hover, QPushButton#Settings:hover {
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


        # фильтр событий на QLabel
        self.image_label.installEventFilter(self)

        # список для хранения координат точек (+ размер, + цвет)
        self.points = []
        # список для хранения координат удалённых точек (+ размер, + цвет)
        self.removed_points = []

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

        # Если клик вне изображения — не обрабатываем
        if not self.image_label.underMouse():
            return
        
        # Координаты клика внутри self.image_label
        widget_pos = self.image_label.mapFromGlobal(event.globalPosition().toPoint())
        # Учёт масштаба:
        original_x = int(widget_pos.x() / self.scale_factor)
        original_y = int(widget_pos.y() / self.scale_factor)

        # Проверяем, попал ли клик внутрь изображения
        if 0 <= original_x < self.pixmap_original.width() and 0 <= original_y < self.pixmap_original.height():
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:  # удаление точки: клик+Shift
                self.remove_dot((original_x, original_y))
            else:  # добавление точки: клик
                self.points.append(((original_x, original_y), self.point_radius))
                print(f"Added dot: ({original_x}, {original_y}), size: {self.point_radius}px")
                self.add_dot()
        else:
            print("Click is outside of image.")

    # Добавление точки и обновление изображения (с учётом текущего масштаба)
    def add_dot(self, clear_removed_points=True):

        if clear_removed_points: # только при добавлении новой точки (флаг)
            self.removed_points.clear() # очистка истории удалённых точек

        pixmap_with_points = self.pixmap.copy()
        painter = QPainter(pixmap_with_points)
        painter.setPen(Qt.GlobalColor.red)
        painter.setBrush(Qt.GlobalColor.red)

        for point, size in self.points:
            # Учёт масштаба
            scaled_x = int(point[0] * self.scale_factor)
            scaled_y = int(point[1] * self.scale_factor)
            radius = int(size * self.scale_factor)  # видимый радиус точек меняется при изменении масштаба (реальный радиус = выставленному в настройках)
            painter.drawEllipse(scaled_x - radius, scaled_y - radius, radius * 2, radius * 2)

        painter.end()
        self.image_label.setPixmap(pixmap_with_points)
    
    # Изменение размера точек
    def set_point_size(self, size):
        self.point_radius = size
        print(f"Point size set to: {size}px")

    # Удаление точки и обновление изображения (с учётом масштаба)
    def remove_dot(self, click_pos):
        removal_radius = 10  # поиск точки для удаления производится в определённом радиусе вокруг точки нажатия; потом можно добавить возможность менять этот радиус
        nearest_point = None
        min_distance = float('inf')

        # удаляет ближайшую
        for point in self.points:
            distance = ((point[0] - click_pos[0]) ** 2 + (point[1] - click_pos[1]) ** 2) ** 0.5
            if distance < removal_radius and distance < min_distance:
                nearest_point = point
                min_distance = distance

        if nearest_point:
            self.points.remove(nearest_point)
            self.removed_points.append(nearest_point) # для возможности восстановления
            print(f"Removed dot: {nearest_point}")
            self.add_dot(False) # False - перерисовка без очистки removed_points
        else:
            print("There isn't dot in the click area to removed.")
    
    def remove_last_dot(self):
        if self.points:
            last_point = self.points.pop()  # Удаляем последнюю точку
            self.removed_points.append(last_point)  # Добавляем её в стек удалённых
            print(f"Removed last dot: {last_point}")
            self.add_dot(False)  # False - перерисовка без очистки removed_points
        else:
            print("No dots to remove.")
    
    def restore_last_dot(self):
        if self.removed_points:
            last_removed = self.removed_points.pop()  # Берём последнюю удалённую точку
            self.points.append(last_removed)  # Возвращаем её в основной список точек
            print(f"Restored last removed dot: {last_removed}")
            self.add_dot(False)  # False - перерисовка без очистки removed_points
        else:
            print("No dots to restore.")
    
    # Горячие клавиши: масштабирование, редактирование
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:  # Ctrl +
                self.zoom_in()
            elif event.key() == Qt.Key.Key_Minus:  # Ctrl -
                self.zoom_out()
            elif event.key() == Qt.Key.Key_0:  # Ctrl 0
                self.reset_zoom()
            elif event.key() == Qt.Key.Key_Z:  # Ctrl + Z
                self.remove_last_dot()
            elif event.key() == Qt.Key.Key_Y:  # Ctrl + Y
                self.restore_last_dot()
    
    # Функции масштабирования
    def zoom_in(self):
        if self.scale_factor < self.max_scale_factor:
            self.scale_factor *= 1.1
            self.update_zoom()
    def zoom_out(self):
        if self.scale_factor > self.min_scale_factor:
            self.scale_factor /= 1.1
            self.update_zoom()
    def reset_zoom(self):
        self.scale_factor = 1.0
        self.update_zoom()

    # Функция для отображения изменений при zoom
    def update_zoom(self):
        self.scale_factor = max(self.min_scale_factor, min(self.scale_factor, self.max_scale_factor)) # ограничиваем масштаб
        self.pixmap = self.pixmap_original.scaled(self.pixmap_original.size() * self.scale_factor, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation) # масштабируем изображение
        self.image_label.setPixmap(self.pixmap)
        self.image_label.resize(self.pixmap.size()) # изменение QLabel
        self.scroll_area.widget().adjustSize()  # изменение QScrollArea
        self.add_dot() # перерисовка точек

    # Полноэкранный режим
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.resize(self.normal_size)
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(screen_geometry)
            self.showFullScreen()
    

    # Открытие проекта
    def open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "ZIP Files (*.zip)")

        if not file_path or not file_path.lower().endswith('.zip'):
            print("Project is not selected or incorrect file format.")
            return

        temp_folder = os.path.join(os.path.dirname(file_path), "temp_project")
        os.makedirs(temp_folder, exist_ok=True)

        try:
            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall(temp_folder)

            image_path = os.path.join(temp_folder, "image.png")
            metadata_path = os.path.join(temp_folder, "metadata.json")

            if not os.path.exists(image_path) or not os.path.exists(metadata_path):
                print("Error: required files are missing in the project.")
                return

            # загрузка данных
            pixmap = QPixmap(image_path)
            with open(metadata_path, 'r', encoding='utf-8') as metafile:
                metadata = json.load(metafile)

            points = [((point["x"], point["y"]), point.get("size", 3)) for point in metadata.get("points", [])]
            file_name = os.path.splitext(os.path.basename(file_path))[0]

            # Создаём новое окно с загруженными данными
            project_window = ImageWindow(image_path)
            project_window.pixmap = pixmap
            project_window.image_label.setPixmap(pixmap)
            project_window.points = points
            project_window.file_name = file_name
            project_window.folder_path = os.path.dirname(file_path)
            project_window.add_dot()
            project_window.exec()

            print(f"Project was loaded from: {file_path}")

        except Exception as e:
            print(f"Error opening project: {e}")

        # Удаляем временные файлы, если они были созданы
        if os.path.exists(temp_folder):
            for f in os.listdir(temp_folder):
                os.remove(os.path.join(temp_folder, f))
            os.rmdir(temp_folder)

    # Создание нового окна для дублированного изображения
    def duplicate_layer(self):
        duplicate_window = DuplicatedImageWindow(self.pixmap)
        duplicate_window.exec()

class DuplicatedImageWindow(ImageWindow):
    def __init__(self, pixmap):
        super().__init__("")
        self.setWindowTitle("Duplicated Layer")
        self.image_label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height()) 



if __name__ == '__main__':
    app = QApplication(sys.argv)

    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())