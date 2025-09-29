

class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.id = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

    def __str__(self):
        return self.name

