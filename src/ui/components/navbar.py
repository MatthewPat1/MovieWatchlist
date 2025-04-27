from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMenu
    )
from PyQt6.QtGui import QAction
class NavBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        home = QPushButton("Home")
        profile = QPushButton("Profile")   
        setting = QPushButton("Settings")

        profile_menu = QMenu()
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        profile_menu.addAction(logout_action)

        profile.setMenu(profile_menu)
        layout.addWidget(home)
        layout.addWidget(profile)
        layout.addWidget(setting)

        self.setLayout(layout)

    def logout(self):
        pass