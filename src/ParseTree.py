from dataclasses import dataclass

@dataclass
class Assignment:
    left_side: list[str]
    right_side: list[str]


@dataclass
class Conjugation:
    tense: str
    mood: str
    suffix: str
    assignments: list[Assignment]


class ParseTree:
    def __init__(self):
        self.pronoun_dict = {}

    def set_pronouns(self, pronouns: list[Assignment]):
        for pronoun in pronouns:
            self.pronoun_dict[pronoun.left_side.join(' ')] = pronoun.right_side.join(' ')


