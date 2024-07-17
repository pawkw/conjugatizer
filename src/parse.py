from TokenBuffer import TokenBuffer, Token
from enum import auto, Enum
from ParseTree import *

class State(Enum):
    unknown = auto()
    ignore = auto()
    pronouns = auto()
    conjugation = auto()
    regular_verb = auto()
    irregular_verb = auto()


def parse_error(error: str, tokens: TokenBuffer, function: str):
    file, line, _ = tokens.get_position()
    print(f"Error: The function {function} found the following error in '{file}' line '{line}':")
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
        case 'conjugation':
            return State.conjugation
        case 'regular':
            return State.regular_verb
        case 'irregular':
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
    

def parse_pronouns(tokens: TokenBuffer, parse_tree: ParseTree) -> State:
    if not tokens.expect_value('pronouns', True):
        parse_error("Expected to find 'Pronouns'.")
    tokens.consume_line()

    assignments : list[Assignment] = []
    while tokens.peek().type not in ['H1', 'H2']:
        if tokens.expect_type('H3'):
            tokens.consume_line()
            continue
        if tokens.expect_type('EOF'):
            return State.ignore
        assignments.append(parse_assignment(tokens))
    parse_tree.set_pronouns(assignments)
    return State.unknown


def parse_conjugation(tokens: TokenBuffer) -> Conjugation:
    pass
    # Consume title
    # Get tense
    # Get mood
    # Get 'of'
    # Get suffix
    # Parse assignments

def parse_conjugations(tokens: TokenBuffer, parse_tree: ParseTree) -> State:
    if not tokens.expect_value('conjugations', True):
        parse_error("Expected to find 'Conjugations'.")
    tokens.consume_line()

    conjugations : list[Conjugation] = []
    while tokens.peek().type not in ['H1']:
        if tokens.expect_type('H3'):
            tokens.consume_line()
            continue
        if tokens.expect_type('EOF'):
            return State.ignore
        if tokens.expect_type('H2'):
            conjugations.append(parse_conjugation(tokens))
            continue
        parse_error("Did not find a conjunction.", tokens, "parse_conjunctions")
    parse_tree.set_pronouns(conjugations)
    return State.unknown


def parse_regular(tokens: TokenBuffer, parse_tree: ParseTree) -> State:
    if not tokens.expect_value('pronouns', True):
        parse_error("Expected to find 'Pronouns'.")
    tokens.consume_line()

    # assignments : list[Assignment] = []
    # while tokens.peek().type not in ['H1', 'H2']:
    #     if tokens.expect_type('H3'):
    #         tokens.consume_line()
    #         continue
    #     if tokens.expect_type('EOF'):
    #         return State.ignore
    #     assignments.append(parse_assignment(tokens))
    # parse_tree.set_pronouns(assignments)
    # return State.unknown


def parse_irregular(tokens: TokenBuffer, parse_tree: ParseTree) -> State:
    if not tokens.expect_value('pronouns', True):
        parse_error("Expected to find 'Pronouns'.")
    tokens.consume_line()

    # assignments : list[Assignment] = []
    # while tokens.peek().type not in ['H1', 'H2']:
    #     if tokens.expect_type('H3'):
    #         tokens.consume_line()
    #         continue
    #     if tokens.expect_type('EOF'):
    #         return State.ignore
    #     assignments.append(parse_assignment(tokens))
    # parse_tree.set_pronouns(assignments)
    # return State.unknown


state_functions = {
    State.unknown: parse_unknown,
    State.ignore: parse_ignore,
    State.pronouns: parse_pronouns,
    State.conjugations: parse_conjugations,
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


