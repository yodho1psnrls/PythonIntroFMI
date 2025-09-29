from model.user import User
from uuid import uuid4


class Rating:
    def __init__(self, stars: int, who: User):
        if stars < 0 or stars >= 10:
            raise ValueError("Review stars should be between 0 and 10")
        self.stars = stars
        self.who_id = who.id
