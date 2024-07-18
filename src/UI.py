from ParseTree import ParseTree
from dataclasses import dataclass
from TokenBuffer import tokenize
import logging

logger = logging.getLogger(__name__)
g_backend: bool = False

def emit(message: str) -> None:
    global g_backend
    if g_backend:
        pass
    else:
        print(message)


def command_error(command, error):
    emit(f"While executing '{command}' the following error occurred:")
    emit(error)

def command_get_verb(ast: ParseTree, verb: str) -> tuple:
    return ast.find_verb(verb)
 

def command_get_conjugation(ast: ParseTree, suffix: str, tense: str, mood: str) -> dict:
    return ast.find_conjugation(suffix, tense, mood)


def command_get_suffix(verb: str):
    return '-' + verb[-2:]


def helper_get_root(verb: str):
    return verb[:-2]


def command_apply_conjugation(verb: str, conjugation: dict) -> dict:
    result = {}
    root = helper_get_root(verb)
    for person, ending in conjugation.items():
        result[person] = root + ending[1:]
    return result


def command_conjugate(ast: ParseTree, verb: str, tense: str = 'present', mood: str = 'indicative') -> dict:
    suffix = command_get_suffix(verb)
    verb_type, _ = command_get_verb(ast, verb)
    if verb_type == 'unknown':
        command_error('Conjugate', f"Did not find '{verb}'.")
        return None
    
    conjugation = command_get_conjugation(ast, suffix, tense, mood)
    result = command_apply_conjugation(verb, conjugation)
    if verb_type == 'irregular':
        conjugation_differences = ast.find_irregular_conjugation(verb, tense, mood)
        for person, differrence in conjugation_differences.items():
            result[person] = differrence
    return result


def parse_conjugate(ast: ParseTree, user_input: list[str]) -> str:
    length = len(user_input)
    tense = 'present'
    mood = 'indicative'
    result_string = ''
    pronouns = False

    if length == 0:
        command_error('conjugate', 'No verb supplied')
        return ''
    verb = user_input[0]
    verb_type, gloss = command_get_verb(ast, verb)

    if length > 1 and user_input[1] in ['pronouns', 'pronoun']:
        user_input.pop(1)
        pronouns = True
        logger.debug('parse_conjugate: received "pronouns"')
        length -= 1

    if length > 1:
        tense = user_input[1]

    if length > 2:
        mood = user_input[2]

    if length > 3:
        extra_input = ' '.join(user_input[3:])
        command_error('conjugate', f"Ignoring extra input: {extra_input}")

    result_string += f"{verb} - {gloss}  type: {verb_type} tense: {tense} mood: {mood}\n"
    logger.debug(f"Calling command_conjugate with {result_string}")
    command_result = command_conjugate(ast, verb, tense, mood)
    logger.debug(f"Received: {command_result}")
    if not command_result:
        return ''

    pronoun_dict = ast.pronoun_dict
    for person, realization in command_result.items():
        result_string += f"{person} = {pronoun_dict[person] + ' ' if pronouns else ''}{realization}\n"

    return result_string

commands = {
    'conjugate': (parse_conjugate, 'conjugate <verb> pronouns(False) <tense(present)> <mood(indicative)>'),
    'save': (None, 'save <filename> chunks(False)\nSaves a new file with the language information. If you specify "chunks", it\nwill save sections as individual files.')
}

def conjugatize(ast: ParseTree, backend: bool):
    global g_backend
    g_backend = backend

    emit('Enter "exit" to exit. Enter "list" to get a list of commands. Enter "<command> help" to get help.')
    while True:
        command = input('>> ').lower()
        command_list = command.split()
        logger.debug(f"Received {command}.")
        if not command_list:
            command_error('User input', 'No command entered.')
            continue

        if command_list[0] == 'exit':
            break

        if command_list[0] == 'list':
            for command_string, command_tuple in commands.items():
                emit(f"{command_string}: {command_tuple[1]}")
            continue

        if command_list[0] in commands.keys():
            if command_list[1] == 'help':
                emit(commands[command_list[0]][1])
            else:
                logger.debug(f"Executing {command_list[0]} with {command_list[1:]}")
                command_result = commands[command_list[0]][0](ast, command_list[1:])
                emit(command_result)
        else:
            emit(f"Command '{command_list[0]}' not found.")