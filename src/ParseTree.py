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

    def set_pronouns(self, assignments: list[Assignment]):
        for pronoun in assignments:
            self.pronoun_dict[' '.join(pronoun.left_side)] = ' '.join(pronoun.right_side)

    def add_conjugation(self, tense: str, mood: str, suffix: str, assignments: list[Assignment]):
        persons_entry = {}
        for person in assignments:
            persons_entry[' '.join(person.left_side)] = ' '.join(person.right_side)
        
        mood_entry = {}
        mood_entry[mood] = persons_entry
        tense_entry = {}
        tense_entry[tense] = mood_entry
        if suffix in self.conjugation_dict.keys():
            self.conjugation_dict[suffix] |= tense_entry
        else:
            self.conjugation_dict[suffix] = tense_entry

    def add_regular(self, assignments: list[Assignment]):
        for verb in assignments:
            self.regular_verbs[' '.join(verb.left_side)] = ' '.join(verb.right_side)
    
    def add_irregular(self, verb: str, gloss: str, tense: str, mood: str, assignments: list[Assignment]):
        persons_entry = {}
        for person in assignments:
            persons_entry[' '.join(person.left_side)] = ' '.join(person.right_side)
        
        mood_entry = {}
        mood_entry[mood] = persons_entry
        tense_entry = {}
        tense_entry[tense] = mood_entry
        if verb in self.irregular_verbs.keys():
            self.irregular_verbs[verb] |= tense_entry
        else:
            self.irregular_verbs[verb] = tense_entry
        self.irregular_verb_glosses[verb] = gloss

    def find_verb(self, verb: str) -> tuple:
        verb_type = 'unknown'
        gloss = 'unknown'

        if verb in self.irregular_verbs.keys():
            verb_type = 'irregular'
            gloss = self.irregular_verb_glosses[verb]
        elif verb in self.regular_verbs.keys():
            verb_type = 'regular'
            gloss = self.regular_verbs[verb]
        
        return verb_type, gloss
    
    def find_irregular_conjugation(self, verb: str, tense: str, mood: str) -> dict:
        result = None
        target = {}
        if verb in self.irregular_verbs.keys():
            target = self.irregular_verbs[verb]
        else:
            return result
        
        if tense in target.keys():
            target = target[tense]
        else:
            return result
        
        if mood in target.keys():
            result = target[mood]
        return result
    
    def find_conjugation(self, suffix: str, tense: str, mood: str) -> dict:
        result = None
        target = {}
        if suffix in self.conjugation_dict.keys():
            target = self.conjugation_dict[suffix]
        else:
            return result
        
        if tense in target.keys():
            target = target[tense]
        else:
            return result
        
        if mood in target.keys():
            result = target[mood]
        return result