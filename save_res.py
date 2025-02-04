import os
import json
import zipfile
from datetime import datetime
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt

# Обработчик сохранения размеченного изображения
def save_markup_image(folder_path, file_name, pixmap, points):
    
    default_file_name = os.path.join(folder_path, f"{file_name}_img+mark") # путь с именем по умолчанию
    file_path, _ = QFileDialog.getSaveFileName(None, "Save Markup Image", default_file_name, "PNG Files (*.png)")

    if file_path:
        
        if not file_path.lower().endswith('.png'): # Если расширение не ".png" или его нет, то делаем его таким
            file_path = os.path.splitext(file_path)[0] + '.png'
        
        if pixmap:
            # копию изображения для отрисовки (в приницпе, отрисованное изображение уже создано, но так надёжнее)
            pixmap_with_points = pixmap.copy()
            painter = QPainter(pixmap_with_points)
            painter.setPen(Qt.GlobalColor.red)
            painter.setBrush(Qt.GlobalColor.red)
            # отрисовка
            for (x, y), size in points:
                painter.drawEllipse(x - size, y - size, size * 2, size * 2)
            painter.end()

            pixmap_with_points.save(file_path, "PNG")  # Сохраняем изображение в PNG
            print(f"Изображение сохранено в {file_path}")
        else:
            print("Нет изображения для сохранения.")


# Обработчик сохранения только разметки (только точки на прозрачном фоне)
def save_markup_only(folder_path, file_name, pixmap, points):

    default_file_name = os.path.join(folder_path, f"{file_name}_mark") # путь с именем по умолчанию
    file_path, _ = QFileDialog.getSaveFileName(None, "Save Markup Only", default_file_name, "PNG Files (*.png)")

    if file_path:

        if not file_path.lower().endswith('.png'):
            file_path = os.path.splitext(file_path)[0] + '.png'

        transparent_pixmap = QPixmap(pixmap.size()) # пустое изображение с прозрачным фоном
        transparent_pixmap.fill(Qt.GlobalColor.transparent)

        # hисуем точки как в списке points
        painter = QPainter(transparent_pixmap)
        painter.setPen(Qt.GlobalColor.red)
        painter.setBrush(Qt.GlobalColor.red)
        
        for (x, y), size in points:  # Исправленный формат точек
            painter.drawEllipse(x - size, y - size, size * 2, size * 2) 

        painter.end()

        if transparent_pixmap.save(file_path, "PNG"):
            print(f"Разметка сохранена в {file_path}")
        else:
            print("Ошибка сохранения файла.")


# Обработчик сохранения инфы о точках (текстовый файл)
def save_points(folder_path, file_name, pixmap, points):
    
    default_file_name = os.path.join(folder_path, f"{file_name}_points") # путь с именем по умолчанию
    file_path, _ = QFileDialog.getSaveFileName(None, "Save Points to JSON", default_file_name, "JSON Files (*.json)")

    if file_path:
        if not file_path.lower().endswith('.json'):
            file_path = os.path.splitext(file_path)[0] + '.json'

        # данные для сохранения
        data = {
            "image_name": f"{file_name}",
            "image_size": {
                "width": pixmap.width(),
                "height": pixmap.height()
            },
            "points": [{"x": int(x), "y": int(y), "size": size} for (x, y), size in points],
            "point_count": len(points),
            "scale": {
                "unit": "nanometers",
                "value_per_pixel": None
            },
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "author": "user",
            "notes": None
        }

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Данные успешно сохранены в {file_path}")

# сохранение проекта в архиве (json файл и исходное изображение) (можно переписать красивее)
def save_project(folder_path, file_name, pixmap, points):
    
    default_file_name = os.path.join(folder_path, f"{file_name}_project") # путь с именем по умолчанию
    file_path, _ = QFileDialog.getSaveFileName(None, "Save Project", default_file_name, "ZIP Files (*.zip)")

    if file_path:
        if not file_path.lower().endswith('.zip'):
            file_path = os.path.splitext(file_path)[0] + '.zip'

        data = {
            "image_name": f"{file_name}.png",
            "image_size": {
                "width": pixmap.width(),
                "height": pixmap.height()
            },
            "points": [{"x": int(x), "y": int(y), "size": size} for (x, y), size in points],
            "point_count": len(points),
            "scale": {
                "unit": "nanometers",
                "value_per_pixel": None
            },
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "author": "user",
            "notes": None
        }

        try:
            # ZIP-архив
            with zipfile.ZipFile(file_path, 'w') as zipf:
                # исходное изображение
                image_path = os.path.join(folder_path, f"{file_name}.png")
                pixmap.save(image_path, "PNG")
                zipf.write(image_path, "image.png")
                os.remove(image_path)

                # JSON-файл
                metadata_path = os.path.join(folder_path, "metadata.json")
                with open(metadata_path, 'w', encoding='utf-8') as metafile:
                    json.dump(data, metafile, indent=4)
                zipf.write(metadata_path, "metadata.json")
                os.remove(metadata_path)

            print(f"Проект успешно сохранён в {file_path}")
        except Exception as e:
            print(f"Ошибка сохранения проекта: {e}")