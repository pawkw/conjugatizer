from dataclasses import dataclass

@dataclass
class Assignment:
    left_side: str
    right_side: str


class ParseTree:
    def __init__(self):
        self.pronoun_dict = {}

    def set_pronouns(self, pronouns: list[Assignment]):
        for pronoun in pronouns:
            self.pronoun_dict[pronoun.left_side] = pronoun.right_side


