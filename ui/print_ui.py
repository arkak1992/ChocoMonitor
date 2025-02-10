import os
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QListWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class PrintUI(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("عرض النتائج")
        self.setGeometry(100, 100, 1024, 600)
        self.setStyleSheet("background-color: #0F2027; color: white; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # العنوان
        self.title_label = QLabel("عرض النتائج")
        self.title_label.setStyleSheet("""
            font-size: 50px; 
            font-weight: bold; 
            color: #00FFFF; 
            text-align: center;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # تخطيط المحتوى
        content_layout = QHBoxLayout()
        layout.addLayout(content_layout)

        # قائمة المجلدات
        self.folder_list = QListWidget()
        self.folder_list.setStyleSheet("""
            font-size: 20px; 
            padding: 10px; 
            background-color: #1E1E1E; 
            color: #00FFFF; 
            border: 2px solid #00FFFF;
        """)
        self.folder_list.itemClicked.connect(self.load_images)
        content_layout.addWidget(self.folder_list)

        # شبكة الصور
        self.image_grid = QGridLayout()
        self.image_container = QWidget()
        self.image_container.setLayout(self.image_grid)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_container)
        content_layout.addWidget(self.scroll_area)

        # تحميل المجلدات
        self.results_directory = os.path.join(os.getcwd(), "results")
        self.load_folders()

        # زر العودة
        self.back_button = QPushButton("العودة")
        self.back_button.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            padding: 20px; 
            border-radius: 15px; 
            background-color: #FF4500; 
            color: white; 
            border: 2px solid #FF6347; 
            min-width: 200px;
        """)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def load_folders(self):
        if not os.path.exists(self.results_directory):
            return
        self.folder_list.clear()
        for folder in sorted(os.listdir(self.results_directory)):
            folder_path = os.path.join(self.results_directory, folder)
            if os.path.isdir(folder_path):
                self.folder_list.addItem(folder)

    def load_images(self, item):
        folder_name = item.text()
        directory = os.path.join(self.results_directory, folder_name)
        for i in reversed(range(self.image_grid.count())):
            self.image_grid.itemAt(i).widget().setParent(None)
        row, col = 0, 0
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".png"):
                image_path = os.path.join(directory, filename)
                pixmap = QPixmap(image_path).scaled(
                    200, 200,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                image_label = QLabel()
                image_label.setPixmap(pixmap)
                image_label.mousePressEvent = lambda event, path=image_path: self.display_full_image(path)
                self.image_grid.addWidget(image_label, row, col)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

    def display_full_image(self, image_path):
        self.full_image_window = QWidget()
        self.full_image_window.setWindowTitle("عرض الصورة")
        self.full_image_window.setGeometry(300, 150, 600, 400)
        full_image_label = QLabel()
        pixmap = QPixmap(image_path).scaled(
            500, 500,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        full_image_label.setPixmap(pixmap)
        layout = QVBoxLayout()
        layout.addWidget(full_image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.full_image_window.setLayout(layout)
        self.full_image_window.show()

    def go_back(self):
        self.close()
        self.main_window.show()