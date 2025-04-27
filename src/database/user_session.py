from datetime import datetime
from typing import Optional

class UserSession:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            # Initialize default values
            cls._instance._user = None
            cls._instance._email = None
            cls._instance._created = None
            cls._instance._id = None
        return cls._instance
    
    @property
    def user(self) -> Optional[str]:
        return self._user
    
    @user.setter
    def user(self, value: str):
        self._user = value
    
    @property
    def email(self) -> Optional[str]:
        return self._email
    
    @email.setter
    def email(self, value: str):
        self._email = value
    
    @property
    def created(self) -> Optional[datetime]:
        return self._created
    
    @created.setter
    def created(self, value: datetime):
        self._created = value
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    def clear(self):
        """Reset all user data"""
        self._user = None
        self._email = None
        self._created = None
        self._id = None
