from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QTextEdit

class InfoPanel(QGroupBox):
    def __init__(self):
        super().__init__("Flight Information")
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setMaximumHeight(150)
        self.text_area.setText("No flight data loaded.")
        layout.addWidget(self.text_area)
        self.setLayout(layout)

    def update_info(self, text):
        self.text_area.setText(text)