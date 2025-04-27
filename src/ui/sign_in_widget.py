from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from database.user_session import UserSession

class SignInWidget(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        username_layout = QHBoxLayout()
        password_layout = QHBoxLayout()

        application_name = QLabel("Movie Ranker")

        username_label = QLabel("User:")
        password_label = QLabel("Pass:")

        self.username_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)

        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_line_edit)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_line_edit)

        self.login_fail = QLabel("Login credentials incorrect or doesn't exist.")

        login_button = QPushButton("Login")
        sign_up_button = QPushButton("Sign Up")

        self.layout.addWidget(application_name)
        self.layout.addLayout(username_layout)
        self.layout.addLayout(password_layout)
        self.layout.addWidget(login_button)
        self.layout.addWidget(sign_up_button)

        login_button.clicked.connect(self.sign_in)
        sign_up_button.clicked.connect(self.show_sign_up)

    def sign_in(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        user = self.db_manager.sign_in(username, password)

        if user:
            session = UserSession()
            session.id, session.user, session.email, session.created = user['id'], user['username'], user['email'], user['date_created']
            watchlist = self.db_manager.get_watchlist(user["id"])
            self.parent.create_watchlist_widget(watchlist)
            self.parent.show_search_page()
        else:
            self.layout.addWidget(self.login_fail)

    def show_sign_up(self):
        self.parent.show_sign_up()
