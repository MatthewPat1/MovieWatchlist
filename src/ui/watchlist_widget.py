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
from PyQt6.QtCore import Qt
import difflib
from api.omdb_client import OMDBClient
from database.user_session import UserSession

class WatchlistWidget(QWidget):
    def __init__(self, parent, watchlist_data, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.watchlist_data = watchlist_data
        self.omdb_client = OMDBClient()
        self.db_manager = db_manager

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        back_button = QPushButton("← Back to Search")

        search_layout = QHBoxLayout()
        self.search = QLineEdit()
        search_button = QPushButton("Search")
        search_layout.addWidget(self.search)
        search_layout.addWidget(search_button)

        self.watch_list = QListWidget()

        self.populate_watchlist()

        layout.addWidget(back_button)
        layout.addLayout(search_layout)
        layout.addWidget(self.watch_list)

        search_button.clicked.connect(self.search_watchlist)
        back_button.clicked.connect(self.parent.show_search_page)
        self.watch_list.itemClicked.connect(self.watchlist_item_clicked)

    def search_watchlist(self):
        pattern = self.search.text().strip().lower()
        self.watch_list.clear()

        if pattern:
            results = [
                movie for movie in self.watchlist_data
                if pattern in movie['Title'].lower() or difflib.SequenceMatcher(None, pattern, movie['Title'].lower()).ratio() > 0.6
            ]
        else:
            results = self.watch_list

        self.watch_list.addItems(results)

    def populate_watchlist(self):
        self.watch_list.clear()
        for watchlist in self.watchlist_data:
            watchlist_dict = dict(watchlist)
            movie_info = self.omdb_client.retrieve_movie_info(watchlist_dict['imdb_id'])
            item = QListWidgetItem(f"{movie_info['Title']}")
            item.setData(Qt.ItemDataRole.UserRole, movie_info)
            self.watch_list.addItem(item)

    def watchlist_item_clicked(self, item):
        user = UserSession()
        movie_data = item.data(Qt.ItemDataRole.UserRole)
        movie_data = self.omdb_client.retrieve_movie_info(movie_data["imdbID"])
        movie_data['userRating'] = self.db_manager.retrieve_watchlist_rating(movie_data['imdbID'], user.id)
        self.parent.show_watchlist_movie_details(movie_data)
