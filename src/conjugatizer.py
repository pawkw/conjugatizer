from TokenBuffer import TokenBuffer
from parse import parse
from UI import conjugatize
import logging
import sys


logger = logging.getLogger("Conjugatizer")


def print_help():
    indent = "    "
    print("Usage:")
    print(f"{sys.argv[0]} [options] [files]")
    print('\nOptions:')
    print("-log_level [level]:")
    print(f"{indent}Sets the minimum logging level. The levels are:")
    print(f"{indent}{indent}debug - All log events are reported.")
    print(f"{indent}{indent}info")
    print(f"{indent}{indent}warning")
    print(f"{indent}{indent}error")
    print(f"{indent}{indent}critical - Only program crashes are reported.")
    print("-v or -verbose:")
    print(f"{indent}The equivalent of '-log_level debug")
    print("-log_file [filename]:")
    print(f"{indent}Log reports are sent to a file instead of standard out.")
    print("-backend or -background:")
    print(f"{indent}Starts the program in non-interactive mode.")
    print(f"{indent}This is meant for wrapper programs that run the program")
    print(f"{indent}as a backend.")
    print()


def main(file_list: list, backend: bool):
    patterns = {
        'H3': r'###\s+',
        'H2': r'##\s+',
        'H1': r'#\s+',
        'definition': r'\w+\:',
        'suffix': r'-\w+',
        'assignment': r'=',
        'word': r'\w+',
    }

    buffer = TokenBuffer()
    logger.debug('Initializing token buffer.')
    buffer.init_patterns(patterns)
    buffer.load_files(file_list)
    buffer.config(skip_white_space=True, skip_EOF = False, skip_EOL = False)
    buffer.tokenize()
    logger.debug('Token buffer initialized.')

    logger.info('Starting parse.')
    ast = parse(buffer)
    logger.info('Finished parse.')

    conjugatize(ast, backend)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        exit(0)

    log_level_dict = {
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    file_list = []
    log_level = logging.CRITICAL
    log_file = None
    backend = False
    skip_next_argument = False
    for argument_number in range(len(sys.argv)):
        if argument_number == 0:
            continue

        if skip_next_argument:
            skip_next_argument = False
            continue

        argument = sys.argv[argument_number]
        if argument.startswith('-'):
            match argument[1:]:
                case 'log_level':
                    log_level = log_level_dict[sys.argv[argument_number+1]]
                    skip_next_argument = True
                case 'v' | 'verbose':
                    log_level = log_level_dict['debug']
                case 'log_file':
                    log_file = sys.argv[argument_number+1]
                    skip_next_argument = True
                case 'backend' | 'background':
                    backend = True
                case _:
                    print_help()
                    exit(1)
        else:
            file_list.append(argument)
    
    logging.basicConfig(level=log_level)
    if log_file:
        logging.basicConfig(filename=log_file)
    main(file_list, backend)
