from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from database.user_session import UserSession


class SignUpWidget(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        email_layout = QHBoxLayout()
        username_layout = QHBoxLayout()
        password_layout = QHBoxLayout()
        password_confirm_layout = QHBoxLayout()

        application_name = QLabel("Movie Ranker")

        email_label = QLabel("Email:")
        username_label = QLabel("User:")
        password_label = QLabel("Pass:")
        password_confirm_label = QLabel("Confirm Pass:")

        self.username_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()
        self.email_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        password_confirm_line_edit = QLineEdit()
        password_confirm_line_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_line_edit)

        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_line_edit)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_line_edit)

        password_confirm_layout.addWidget(password_confirm_label)
        password_confirm_layout.addWidget(password_confirm_line_edit)

        sign_up_button = QPushButton("Confirm Sign Up")
        already_have_an_account_button = QPushButton("Already have an account")

        sign_up_button.clicked.connect(self.create_new_user)
        already_have_an_account_button.clicked.connect(self.show_sign_in)
        layout.addWidget(application_name)
        layout.addLayout(email_layout)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(password_confirm_layout)
        layout.addWidget(sign_up_button)
        layout.addWidget(already_have_an_account_button)

    def create_new_user(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        email = self.email_line_edit.text()
        if self.db_manager.create_new_user(username, password, email):
            session = UserSession()
            user = self.db_manager.sign_in(username, password)
            session.id, session.user, session.email, session.created = (
                user["id"],
                user["username"],
                user["email"],
                user["date_created"],
            )
            watchlist = self.db_manager.get_watchlist(user["id"])
            self.parent.create_watchlist_widget(watchlist)
            self.parent.show_search_page()
        else:
            print("nuh uh!!!!")

    def show_sign_in(self):
        self.parent.show_sign_in()
