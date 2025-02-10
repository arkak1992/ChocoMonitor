import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QVBoxLayout, QPushButton, QMessageBox
from ui.sensor_widget import SensorWidget
from ui.graph_widget import GraphWidget
from ui.control_buttons import ControlButtons
from ui.settings_ui import SettingsUI
from sensors.arduino_receiver import ArduinoReader
from algorithms.data_analysis import analyze_and_save

class ChocoMonitorUI(QWidget):
    def __init__(self, arduino_reader):
        super().__init__()
        self.setWindowTitle("ChocoMonitor - محلل درجة الحرارة")
        self.setGeometry(100, 100, 1024, 600)
        self.arduino_reader = arduino_reader
        self.settings = self.load_settings()
        self.init_ui()

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"start_temperature": 30, "duration": 5}

    def init_ui(self):
        main_layout = QGridLayout()
        left_layout = QVBoxLayout()

        self.sensor_widget = SensorWidget(self.arduino_reader)
        left_layout.addWidget(self.sensor_widget)

        self.buttons_widget = ControlButtons()
        self.buttons_widget.start_clicked.connect(self.start_graph)
        self.buttons_widget.stop_clicked.connect(self.stop_graph)
        self.buttons_widget.settings_clicked.connect(self.open_settings)
        self.buttons_widget.reset_clicked.connect(self.reset_graph)
        left_layout.addWidget(self.buttons_widget)

        self.export_button = QPushButton("تصدير التقرير")
        self.export_button.setStyleSheet("""
            font-size: 16px; 
            padding: 10px; 
            background-color: #007ACC; 
            color: white;
            border-radius: 8px;
        """)
        self.export_button.clicked.connect(self.export_report)
        left_layout.addWidget(self.export_button)

        main_layout.addLayout(left_layout, 0, 0)

        self.graph_widget = GraphWidget(self.arduino_reader)
        main_layout.addWidget(self.graph_widget, 0, 1)

        self.setLayout(main_layout)

    def start_graph(self):
        self.graph_widget.start_graph()

    def stop_graph(self):
        self.graph_widget.stop_graph()

    def reset_graph(self):
        self.graph_widget.stop_graph()
        self.graph_widget.start_graph()
        print("🔄 تم إعادة تعيين الرسم البياني.")

    def open_settings(self):
        self.settings_window = SettingsUI(self)
        self.settings_window.settings_applied.connect(self.update_settings)
        self.settings_window.show()

    def update_settings(self, new_settings):
        self.settings = new_settings
        self.graph_widget.max_duration = new_settings["duration"] * 60

    def export_report(self):
        csv_file = getattr(self.arduino_reader, "data_file", None)
        if csv_file and os.path.exists(csv_file):
            analyze_and_save(csv_file)
            QMessageBox.information(self, "نجاح التصدير", "تم حفظ التقرير بنجاح.")
        else:
            QMessageBox.warning(self, "خطأ في التصدير", "لا توجد بيانات صالحة للتصدير.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arduino_reader = ArduinoReader()
    arduino_reader.start_reading()
    window = ChocoMonitorUI(arduino_reader)
    window.show()
    sys.exit(app.exec())