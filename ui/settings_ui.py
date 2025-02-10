from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt6.QtCore import pyqtSignal
import json

class SettingsUI(QDialog):
    settings_applied = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("الإعدادات")
        self.setGeometry(200, 200, 300, 200)
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.temp_label = QLabel("درجة الحرارة الأولية (°C):")
        self.temp_input = QSpinBox()
        self.temp_input.setRange(10, 50)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.temp_input)

        self.duration_label = QLabel("مدة التشغيل (دقيقة):")
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 60)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)

        self.apply_button = QPushButton("تطبيق")
        self.apply_button.setStyleSheet("""
            QPushButton {
                font-size: 16px; 
                padding: 10px; 
                background-color: #007ACC; 
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #005f9e; }
        """)
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def load_settings(self):
        try:
            with open("config.json", "r") as file:
                settings = json.load(file)
                self.temp_input.setValue(settings.get("start_temperature", 30))
                self.duration_input.setValue(settings.get("duration", 5))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def apply_settings(self):
        settings = {
            "start_temperature": self.temp_input.value(),
            "duration": self.duration_input.value()
        }
        with open("config.json", "w") as file:
            json.dump(settings, file, indent=4)
        self.settings_applied.emit(settings)
        self.close()