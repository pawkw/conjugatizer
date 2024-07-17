from TokenBuffer import TokenBuffer, Token
from enum import auto, Enum
from ParseTree import *
from typing import Callable
from functools import partial

## File format
#  Section:
#    HEADER
#    (ASSIGNMENT+)?  -- UNKNOWN sections discard all content
#
#  HEADER:
#    H1 [UNKNOWN | "pronouns" | "regular"] (ignore)*
#    | H1 DEFINITION("conjunction:") SPECIFICATION
#    | H1 DEFINITION("irregular:") ASSIGNMENT(SPECIFICATION "=" GLOSS)
#  
#  DEFINITION:
#    WORD ":"
#
#  SPECIFICATION:
#    TENSE MOOD "of" [VERB | SUFFIX] -- conjugation section has SUFFIX
#
#  ASSIGNMENT:
#    (WORD+)? "=" WORD+
#
#  TENSE, MOOD, VERB, UNKNOWN:
#    WORD
#
#  SUFFIX:
#    "-" WORD

class State(Enum):
    unknown = auto()
    ignore = auto()
    pronouns = auto()
    conjugation = auto()
    regular_verb = auto()
    irregular_verb = auto()


def parse_error(error: str, tokens: TokenBuffer, function: str):
    file, line, _ = tokens.get_position()
    print(f"Error: The function {function} found the following error in '{file}' line {line}:")
    print(error)
    exit(1)


def parse_unknown(tokens: TokenBuffer, _) -> State:
    if tokens.out_of_tokens():
        return None
    
    peek: Token = tokens.peek()
    while not tokens.out_of_tokens() and peek.type != 'H1':
        tokens.consume_line()
        peek = tokens.peek()
        if peek.type == 'EOF':
            return State.ignore
        
    tokens.consume()
    peek = tokens.peek()
    match peek.value.lower():
        case 'pronouns':
            return State.pronouns
        case 'conjugation:':
            return State.conjugation
        case 'regular':
            return State.regular_verb
        case 'irregular:':
            return State.irregular_verb
        case _:
            return State.unknown
        

def parse_ignore(tokens: TokenBuffer, _) -> State:
    peek: Token = tokens.peek()
    while not tokens.out_of_tokens() and peek.type != 'H1':
        tokens.consume_line()
    return State.unknown


def parse_assignment(tokens: TokenBuffer):
    left_side = []
    right_side = []
    assignment_found = False
    peek: Token = tokens.peek()
    while peek.type != 'EOL':
        if peek.type == 'assignment':
            assignment_found = True
            tokens.consume()
            continue
        if assignment_found:
            right_side.append(peek.value)
        else:
            left_side.append(peek.value)
        tokens.consume()

    if not assignment_found:
        parse_error("Expected an assignment.", tokens, 'parse_assignment')

    tokens.consume_line()
    return Assignment(left_side=left_side, right_side=right_side)
    

def parse_assignments(tokens: TokenBuffer, assignment_function: Callable) -> State:
    result = State.unknown
    assignments : list[Assignment] = []
    while tokens.peek().type not in ['H1']:
        if tokens.expect_type('H3'):
            tokens.consume_line()
            continue
        if tokens.expect_type('EOF'):
            result = State.ignore
            tokens.consume()
            break
        assignments.append(parse_assignment(tokens))
    assignment_function(assignments)
    return result


def parse_pronouns(tokens: TokenBuffer, parse_tree: ParseTree) -> State:
    tokens.consume_line()
    return parse_assignments(tokens, parse_tree.set_pronouns)


def parse_specification(tokens: TokenBuffer) -> tuple:
    word1 = tokens.peek().value
    tokens.consume()
    word2 = tokens.peek().value
    tokens.consume()
    if tokens.peek().value != 'of':
        parse_error("Expected (word) (word) of (word).")
    tokens.consume()
    word3 = tokens.peek().value
    tokens.consume()
    return word1, word2, word3


def parse_conjugation(tokens: TokenBuffer, parse_tree: ParseTree) -> State:
    tokens.consume()
    tense, mood, suffix = parse_specification(tokens)
    function = partial(parse_tree.add_conjugation, tense=tense, mood=mood, suffix=suffix)
    return parse_assignments(tokens, function)


def parse_regular(tokens: TokenBuffer, parse_tree: ParseTree):
    tokens.consume_line()
    return parse_assignments(tokens, parse_tree.add_regular)


def parse_irregular(tokens: TokenBuffer, parse_tree: ParseTree):
    tokens.consume()
    tense, mood, verb = parse_specification(tokens)
    gloss = parse_assignment(tokens).right_side.join(' ')
    function = partial(parse_tree.add_irregular, verb=verb, gloss=gloss, tense=tense, mood=mood)
    return parse_assignments(tokens, function)


state_functions = {
    State.unknown: parse_unknown,
    State.ignore: parse_ignore,
    State.pronouns: parse_pronouns,
    State.conjugation: parse_conjugation,
    State.regular_verb: parse_regular,
    State.irregular_verb: parse_irregular,
}


def parse(tokens: TokenBuffer) -> ParseTree:
    next_state = None
    state = State.ignore
    parse_tree = ParseTree()

    while not tokens.out_of_tokens():
        if next_state:
            state = next_state
            next_state = None
        next_state = state_functions[state](tokens, parse_tree)

    return parse_tree        


