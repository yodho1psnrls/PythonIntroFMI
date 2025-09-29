from model.user import User


class Comment:
    def __init__(self, text: str, who: User):
        if not isinstance(text, str):
            raise ValueError("The given text should be of string type")
        self.text = text
        self.who_id = who.id
