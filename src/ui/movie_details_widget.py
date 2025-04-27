from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QSpacerItem, 
                            QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests
from io import BytesIO
from database.user_session import UserSession

class MovieDetailsWidget(QWidget):

    def __init__(self, db_manager, parent, watchlist=False):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.watchlist = watchlist
        self.movie_data = {}
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        back_button = None

        if self.watchlist:
            back_button = QPushButton("← Back to Watchlist") 
            back_button.clicked.connect(self.parent.show_watchlist)
        else:
            back_button = QPushButton("← Back to Search")
            back_button.clicked.connect(self.parent.show_search_page)

        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.addStretch()

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.poster_label = QLabel()

        self.plot_desc = QLabel()
        self.plot_desc.setWordWrap(True)

        self.user_rating = QLineEdit()

        watchlist_button = None
        if self.watchlist:
            watchlist_button = QPushButton("Edit Movie Rating") 
            watchlist_button.clicked.connect(self.update_watchlist_rating)
        else:
            watchlist_button = QPushButton("Add Movie Rating")
            watchlist_button.clicked.connect(self.add_to_watchlist)

        self.release_date_label = QLabel()
        self.rating_label = QLabel()
        self.personal_rating_label = QLabel()

        self.layout.addLayout(back_layout)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.poster_label)
        self.layout.addWidget(self.plot_desc)
        self.layout.addWidget(self.release_date_label)
        self.layout.addWidget(self.rating_label)
        self.layout.addWidget(self.user_rating)
        self.layout.addWidget(watchlist_button)
        self.layout.addStretch()

    def populate_movie_details(self, movie_data):
        self.movie_data = movie_data
        self.title_label.setText(movie_data["Title"])

        self.plot_desc.setText(
            movie_data.get("Plot", "No description available.")
        )
        self.release_date_label.setText(
            f"Release Date: {movie_data.get('Year', 'Unknown')}"
        )

        poster_url = movie_data.get("Poster")
        if poster_url and poster_url != "N/A":  # OMDB uses 'N/A' when no poster exists
            try:
                # Download the image
                response = requests.get(poster_url)
                image_data = BytesIO(response.content)

                # Create QPixmap from downloaded data
                pixmap = QPixmap()
                pixmap.loadFromData(image_data.getvalue())

                # Scale the image to fit the label while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    self.poster_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                self.poster_label.setPixmap(scaled_pixmap)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.poster_label.setText("Error loading image")
        else:
            self.poster_label.setText("No poster available")

        self.rating_label.setText(f"IMDB Rating: {movie_data.get('imdbRating', 'N/A')}/10")
        if self.watchlist:
            user = UserSession()
            user_watchlist_rating = self.db_manager.retrieve_watchlist_rating(movie_data.get('imdbID'), user.id)
            self.personal_rating_label.setText(f"Personal Rating: {user_watchlist_rating['rating']}")
            self.layout.insertWidget(self.layout.indexOf(self.rating_label), self.personal_rating_label)

    def add_to_watchlist(self):
        user = UserSession()

        rating = -1
        if self.user_rating.text():
            rating = self.user_rating.text()
        self.db_manager.insert_movie_into_watchlist(user.id, self.movie_data['imdbID'], rating)
        watchlist_data = self.db_manager.get_watchlist(user.id)
        self.parent.create_watchlist_widget(watchlist_data)
        self.parent.show_watchlist() if self.watchlist else self.parent.show_search_page()

    def update_watchlist_rating(self):
        user = UserSession()
        if self.user_rating.text():
            rating = self.user_rating.text()
            self.db_manager.update_movie_in_watchlist(user.id, rating, self.movie_data['imdbID'])
            watchlist_data = self.db_manager.get_watchlist(user.id)
            self.parent.create_watchlist_widget(watchlist_data)
            self.parent.show_watchlist() if self.watchlist else self.parent.show_search_page()
