from dataclasses import dataclass

@dataclass
class Assignment:
    left_side: list[str]
    right_side: list[str]


class ParseTree:
    def __init__(self):
        self.pronoun_dict = {}
        self.conjugation_dict = {}
        self.regular_verbs = {}
        self.irregular_verbs = {}
        self.irregular_verb_glosses = {}

    def set_pronouns(self, pronouns: list[Assignment]):
        for pronoun in pronouns:
            self.pronoun_dict[pronoun.left_side.join(' ')] = pronoun.right_side.join(' ')

    def add_conjugation(self, tense: str, mood: str, suffix: str, assignments: list[Assignment]):
        persons_entry = {}
        for person in assignments:
            persons_entry[person.left_side.join(' ')] = person.right_side.join(' ')
        
        mood_entry = {}
        mood_entry[mood] = persons_entry
        tense_entry = {}
        tense_entry[tense] = mood_entry
        self.conjugation_dict[suffix] |= tense_entry

    def add_regular(self, verbs: list[Assignment]):
        for verb in verbs:
            self.regular_verbs[verb.left_side] = verb.right_side.join(' ')
    
    def add_irregular(self, verb: str, gloss: str, tense: str, mood: str, assignments: list[Assignment]):
        persons_entry = {}
        for person in assignments:
            persons_entry[person.left_side.join(' ')] = person.right_side.join(' ')
        
        mood_entry = {}
        mood_entry[mood] = persons_entry
        tense_entry = {}
        tense_entry[tense] = mood_entry
        self.irregular_verbs[verb] |= tense_entry
        self.irregular_verb_glosses[verb] = gloss