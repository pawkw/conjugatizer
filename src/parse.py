from TokenBuffer import TokenBuffer, Token
from enum import auto, Enum
from ParseTree import *

class State(Enum):
    unknown = auto()
    ignore = auto()
    pronouns = auto()
    conjugations = auto()
    regular_verb = auto()
    irregular_verb = auto()


def parse_error(error: str, tokens: TokenBuffer, function: str):
    file, line, _ = tokens.get_position()
    print(f"Error: The function {function} found the following error in '{file}' line '{line}':")
    print(error)
    exit(1)


def parse_unknown(tokens: TokenBuffer):
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
        case 'conjugations':
            return State.conjugations
        case 'regular':
            return State.regular_verb
        case 'irregular':
            return State.irregular_verb
        case _:
            return State.unknown
        

def parse_ignore(tokens: TokenBuffer):
    peek: Token = tokens.peek()
    while not tokens.out_of_tokens() and peek.type != 'H1':
        tokens.consume_line()
    return State.unknown


def parse_assigment(tokens: TokenBuffer):
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
    tokens.consume_line()
    left_side = left_side.join(' ')
    right_side = right_side.join(' ')
    return Assignment(left_side=left_side, right_side=right_side)
    

def parse_pronouns(tokens: TokenBuffer):
    if not tokens.expect_value('pronouns', True):
        parse_error("Expected to find 'Pronouns'.")
    tokens.consume_line()


state_functions = {
    State.unknown: parse_unknown,
    State.ignore: parse_ignore,

}


def parse(tokens: TokenBuffer):
    next_state = None
    state = State.ignore

    while not tokens.out_of_tokens():
        if next_state:
            state = next_state
            next_state = None
        next_state = state_functions[state](tokens)
        


