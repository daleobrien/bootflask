
from flask.ext.login import (UserMixin, AnonymousUser)
from bcrypt import hashpw
import weakref


class User(UserMixin):

    instances = []

    def __init__(self, name, id, hashed_password, active=True):
        User.instances.append(weakref.proxy(self))
        self.name = name
        self.id = id
        self.active = active
        self.hashed_password = hashed_password

    def is_active(self):
        return self.active

    @classmethod
    def check_password(cls, user_name, password):

        for user in User.instances:
            if user.name == user_name:
                return hashpw(password, user.hashed_password) == \
                                                          user.hashed_password
        return False


class Anonymous(AnonymousUser):
    name = u"Anonymous"
