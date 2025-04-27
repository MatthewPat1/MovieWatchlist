from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from .search_widget import SearchWidget
from .movie_details_widget import MovieDetailsWidget
from .watchlist_widget import WatchlistWidget
from .sign_in_widget import SignInWidget
from .sign_up_widget import SignUpWidget
from .components.navbar import NavBar

# from .movie_details_widget import MovieDetailsWidget
from database.db_manager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Tracker")
        self.setMinimumSize(800, 600)

        # Initialize database connection
        self.db_manager = DatabaseManager()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.search_widget = SearchWidget(self)
        self.sign_in_widget = SignInWidget(self, self.db_manager)
        self.sign_up_widget = SignUpWidget(self, self.db_manager)
        self.movie_details_widget = MovieDetailsWidget(self.db_manager, self)
        self.watchlist_movie_details_widget = MovieDetailsWidget(self.db_manager, self, watchlist=True)

        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.search_widget)
        self.stacked_widget.addWidget(self.movie_details_widget)
        self.stacked_widget.addWidget(self.watchlist_movie_details_widget)
        self.stacked_widget.addWidget(self.sign_in_widget)
        self.stacked_widget.addWidget(self.sign_up_widget)
        self.stacked_widget.setCurrentWidget(self.sign_in_widget)

    def create_watchlist_widget(self, watchlist):
        try:
            if self.stacked_widget.indexOf(self.watchlist_widget) != -1:
                self.stacked_widget.removeWidget(self.watchlist_widget)
            self.watchlist_widget = WatchlistWidget(self, watchlist, self.db_manager)
            self.stacked_widget.addWidget(self.watchlist_widget)
        except AttributeError:
            self.watchlist_widget = WatchlistWidget(self, watchlist, self.db_manager)
            self.stacked_widget.addWidget(self.watchlist_widget)

    def show_search_page(self):
        self.stacked_widget.setCurrentWidget(self.search_widget)

    def show_movie_details(self, movie_data):
        self.movie_details_widget.populate_movie_details(movie_data)
        self.stacked_widget.setCurrentWidget(self.movie_details_widget)

    def show_watchlist_movie_details(self, movie_data):
        self.watchlist_movie_details_widget.populate_movie_details(movie_data)
        self.stacked_widget.setCurrentWidget(self.watchlist_movie_details_widget)

    def show_watchlist(self):
        self.stacked_widget.setCurrentWidget(self.watchlist_widget)

    def show_sign_in(self):
        self.stacked_widget.setCurrentWidget(self.sign_in_widget)

    def show_sign_up(self):
        self.stacked_widget.setCurrentWidget(self.sign_up_widget)
