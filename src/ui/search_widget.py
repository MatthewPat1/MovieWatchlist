from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)
from api.omdb_client import OMDBClient
from .components.navbar import NavBar


class SearchWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.omdb_client = OMDBClient()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        navbar = NavBar()

        # Search controls
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        search_button = QPushButton("Search")
        watchlist_button = QPushButton("Watchlist")

        button_layout = QVBoxLayout()
        button_layout.addWidget(search_button)
        button_layout.addWidget(watchlist_button)

        search_layout.addWidget(self.search_input)
        search_layout.addLayout(button_layout)

        # Movie list
        self.movie_list = QListWidget()
        
        layout.addWidget(navbar)
        layout.addLayout(search_layout)
        layout.addWidget(self.movie_list)

        # Connect signals
        search_button.clicked.connect(self.search_movies)
        watchlist_button.clicked.connect(self.watchlist_button_clicked)
        self.movie_list.itemClicked.connect(self.movie_item_clicked)

    def search_movies(self):
        query = self.search_input.text()
        results = self.omdb_client.search_movies(query)
        self.update_movie_list(results)

    def update_movie_list(self, results):
        self.movie_list.clear()
        for movie in results:
            item = QListWidgetItem(movie['Title'])
            item.setData(Qt.ItemDataRole.UserRole, movie)
            self.movie_list.addItem(item)

    def movie_item_clicked(self, item):
        movie_data = item.data(Qt.ItemDataRole.UserRole)
        movie_data = self.omdb_client.retrieve_movie_info(movie_data['imdbID'])
        self.parent.show_movie_details(movie_data)

    def watchlist_button_clicked(self):
        self.parent.show_watchlist()