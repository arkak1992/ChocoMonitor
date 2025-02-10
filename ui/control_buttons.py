from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal

class ControlButtons(QWidget):
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        buttons = [
            ("بدء التشغيل", "green", self.start_clicked),
            ("إيقاف", "red", self.stop_clicked),
            ("الإعدادات", "#007ACC", self.settings_clicked),
            ("إعادة التعيين", "orange", self.reset_clicked, "black")
        ]

        for text, color, signal, *args in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            text_color = args[0] if args else "white"
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 18px; 
                    background-color: {color}; 
                    color: {text_color};
                    border-radius: 8px;
                }}
                QPushButton:hover {{ background-color: {color}; opacity: 0.9; }}
            """)
            btn.clicked.connect(signal.emit)
            layout.addWidget(btn)

        self.setLayout(layout)