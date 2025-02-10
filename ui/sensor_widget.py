from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt

class SensorWidget(QWidget):
    def __init__(self, arduino_reader):
        super().__init__()
        self.arduino_reader = arduino_reader
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(1000)  # تحديث كل ثانية

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("درجة الحرارة: -- °C")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #00FF00;
            background-color: #1A1A1A;
            padding: 15px;
            border-radius: 10px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_temperature(self):
        temp = self.arduino_reader.get_latest_temperature()
        if temp is not None:
            self.label.setText(f"درجة الحرارة: {temp:.2f} °C")
        else:
            self.label.setText("درجة الحرارة: -- °C")
            self.label.setStyleSheet("color: #FF0000;")  # تغيير اللون عند فقدان الاتصال