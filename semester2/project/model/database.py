from model.publication import Publication
from model.user import User


class Database:
    def __init__(self):
        self.users = dict[str, User] = []
        self.publications: dict[str, Publication] = []

    # def login(self, )

    def publish(self, publication: Publication):
        self.publications.append(publication)

    def find_user_by_name(self, name: str) -> User:
        # return [u.name for u in self.users.values()].index(name)
        for u in self.users.values():
            if u.name == name:
                return u
        return None

    def try_login(self, name: str, password: str) -> bool:
        user = self.find_user_by_name(name)
        if user is None:
            return False
        return user.password == password
