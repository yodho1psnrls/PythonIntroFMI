from model.user import User
from model.review import Rating
from model.comment import Comment
from gen.sdf.equations import Equation


class Publication:
    def __init__(
        self,
        name: str,
        equation: Equation,
        publisher: User,
    ):
        self.name = name
        self.equation = equation
        self.who_id = publisher.id
        self.ratings: list[Rating] = []
        self.comments: list[Comment] = []

    def rate(self, review: Rating):
        self.reviews.append(review)

    def comment(self, comment: Comment):
        self.comments.append(comment)

    def rating(self) -> float:
        rts = self.ratings
        return sum([r.stars for r in rts]) / len(rts)
