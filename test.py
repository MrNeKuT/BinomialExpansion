import re

from BinomialExpansion import *


def expand(str_expr: str):
    Symbol.with_print = False
    pattern = re.compile(r'-?\d*\w')

    res = re.findall(pattern, str_expr)
    if len(res) < 3:
        raise ValueError('Incorrect input!')

    if len(res[0]) > 1 and '-' in res[0][-2]:
        res[0] = res[0].replace('-', '-1')
    elif len(res[0]) == 1:
        res[0] = '1' + res[0]

    x = Symbol(res[0][-1])
    x.factor = int(res[0].replace(res[0][-1], ''))
    x.whole = int(res[1])
    degree = int(res[2])

    return str(x**degree).replace(' ', '')


def main():
    test_expr = '(x + 3)^2'
    result = expand(test_expr)
    print(result)


if __name__ == '__main__':
    main()
