from TokenBuffer import Token, TokenBuffer
import sys


def print_help():
    indent = "    "
    print("Usage:")
    print(f"{sys.argv[0]} [options] [files]")


def main(file_list: list):
    patterns = {
        'H3': r'###\s+',
        'H2': r'##\s+',
        'H1': r'#\s+',
        'definition': r'\w+\:',
        'suffix': r'\s-\w+',
        'assignment': r'=',
        'word': r'\w+',
    }

    buffer = TokenBuffer()
    buffer.init_patterns(patterns)
    buffer.load_files(file_list)
    buffer.config(skip_white_space=True, skip_EOF = False, skip_EOL = False)
    buffer.tokenize()

    while not buffer.out_of_tokens():
        peek: Token = buffer.peek()
        file, line, _ = buffer.get_position()
        print(f"file: {file} line {line} column {peek.column} type: {peek.type} value: '{peek.value}'")
        buffer.consume()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        exit(0)

    main(sys.argv[1:])
