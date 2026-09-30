import argparse
import re
from pathlib import Path


PATTERN = re.compile(r'"(?:\\.|[^"\\])*"|/\*.*?\*/|(?://[^\n]*(?:\n|$))+', flags=re.S)


def strip_nonlegal(content):
    def replace(match):
        token = match.group()
        if token.startswith('"'):
            return token
        if re.search(r'Copyright|License Agreement|license agreement|Subscription Agreement', token):
            return token
        return '\n' * token.count('\n') + ' '
    return PATTERN.sub(replace, content)


def semantic_tokens(content):
    content = PATTERN.sub(lambda m:m.group() if m.group().startswith('"') else ' ', content)
    return re.findall(r'"(?:\\.|[^"\\])*"|\S+', content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args()
    for path in args.paths:
        original = path.read_text(encoding='utf-8')
        cleaned = strip_nonlegal(original)
        if semantic_tokens(original) != semantic_tokens(cleaned):
            raise ValueError(f'Tokens funcionais alterados: {path}')
        path.write_text(cleaned, encoding='utf-8')
        print(path)


if __name__ == '__main__':
    main()
