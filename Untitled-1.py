from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PySide6.QtCore import Slot

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.input_field = QLineEdit()
        self.output_label = QLabel("No input yet")

        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.output_label)
        self.setLayout(layout)

        self.input_field.textChanged.connect(self.on_text_changed)

    @Slot()
    def on_text_changed(self, new_text):
         self.output_label.setText(f"Input changed to: {new_text}")

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()