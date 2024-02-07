from enum import Enum


class UserRole(Enum):
    sa = 'Site Admin'
    so = 'Stadium Owner'
    u = 'User'

    @classmethod
    def choices(cls):
        return ((_.name, _.value) for _ in cls)