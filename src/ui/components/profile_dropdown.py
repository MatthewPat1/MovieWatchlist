from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel
)

class ProfileDropdown(QWidget):
    def __init__(self):
        super().__init__()
        self.profile = QPushButton("Profile")
        