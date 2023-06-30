from functools import singledispatchmethod


class Symbol:
    pass


class Expression:
    def __init__(self, symbols: list, operators: list = []):
        self._symbols = []
        self._operators = operators
        self._str_expr = ''

        stop_list = []
        for idx_symbol in range(len(symbols) - 1):
            cache = symbols[idx_symbol]
            if isinstance(cache, Symbol):
                if ((cache.var, cache.degree) in stop_list) or cache.factor == 0:
                    continue

                for idx_sub_symbol in range(idx_symbol + 1, len(symbols)):
                    if isinstance(symbols[idx_sub_symbol], Symbol):
                        if cache.var == symbols[idx_sub_symbol].var and \
                                cache.degree == symbols[idx_sub_symbol].degree:
                            cache += symbols[idx_sub_symbol]

                stop_list.append((cache.var, cache.degree))
                if cache.factor == 0:
                    cache = 0

            if cache:
                self._symbols.append(cache)

        if (m := symbols[-1]) != 0 and not isinstance(m, Symbol):
            self._symbols.append(m)

    @property
    def expression(self):
        for idx_symbol in range(len(self._symbols) - 1):
            item = self._symbols[idx_symbol]
            if idx_symbol != 0:
                item = abs(item)

            match (self._symbols[idx_symbol + 1]):
                case Symbol():
                    self._str_expr += str(self._symbols[idx_symbol]) + \
                                      (' + ' if self._symbols[idx_symbol + 1].factor > 0 else ' - ')

                case int() | float():
                    self._str_expr += str(self._symbols[idx_symbol]) + \
                                      (' + ' if self._symbols[idx_symbol + 1] > 0 else ' - ')

        self._str_expr += str(abs(self._symbols[-1]))
        return self._str_expr

    @property
    def symbols(self):
        return self._symbols

    def __mul__(self, other):
        if isinstance(other, Symbol):
            return other * self

    def __str__(self):
        return self.expression


class Symbol:
    with_print = True

    def __init__(self, char: str):
        self._symbol = char
        self._str_expr = char
        self._expr = {"var": char,
                      "factor": 1,
                      "degree": 1,
                      "whole": 0}

    @property
    def expression(self):
        var, factor, degree, whole = self._expr.values()
        match ((factor, degree)):
            case (0, _):
                var, degree = '0', 1
            case (_, 0):
                var, factor = '1', 1

        self._str_expr = ('-' if factor < 0 else '') + \
                         (abs(factor) != 1 and factor != 0) * (str(abs(factor))) + \
                         (factor != 0 or whole == 0) * var + \
                         (degree != 1) * ('^' + str(degree)) + \
                         (factor != 0 and whole != 0) * (' + ' if whole >= 0 else ' - ') + \
                         (whole != 0) * (str(abs(whole)))

        return self._str_expr

    @property
    def var(self):
        return self._expr['var']

    @property
    def factor(self):
        return self._expr['factor']

    @property
    def degree(self):
        return self._expr['degree']

    @property
    def whole(self):
        return self._expr['whole']

    @var.setter
    def var(self, value: str):
        if not isinstance(value, str):
            raise NotImplementedError(f"Cannot format value of type {type(value)}",
                                      "must be type: str")

        self._expr['var'] = value

    @property
    def term(self):
        f = Symbol(self.var)
        f.factor = self.factor
        f.degree = self.degree
        return f

    @factor.setter
    def factor(self, value):
        if not any((isinstance(value, int), isinstance(value, float))):
            raise NotImplementedError(f"Cannot format value of type {type(value)}",
                                      "must be type: float or int")

        self._expr['factor'] = value

    @degree.setter
    def degree(self, value):
        if not any((isinstance(value, int), isinstance(value, float))):
            raise NotImplementedError(f"Cannot format value of type {type(value)}",
                                      "must be type: float or int")

        self._expr['degree'] = value

    @whole.setter
    def whole(self, value):
        if not any((isinstance(value, int), isinstance(value, float))):
            raise NotImplementedError(f"Cannot format value of type {type(value)}",
                                      "must be type: float or int")

        self._expr['whole'] = value

    @singledispatchmethod
    def __imul__(self, other):
        if isinstance(other, Symbol):
            if self._expr['var'] == other.self._expr['var']:
                self._expr['degree'] += 1
            else:
                self._expr['var'] += other.self._expr['var']
                self._expr['factor'] *= other.self._expr['factor']

            f = Expression([self, other * self._expr['whole']],
                           [x for x in self.expression if x in '+-'])

            if self._expr['whole'] == 1:
                self._expr['whole'] = 0

            return f
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__imul__.register(int)
    @__imul__.register(float)
    def _(self, other):
        self._expr['factor'] *= other
        self._expr['whole'] *= other
        return self

    @singledispatchmethod
    def __itruediv__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__itruediv__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__itruediv__.register(int)
    @__itruediv__.register(float)
    def _(self, other):
        self._expr['factor'] /= other
        self._expr['whole'] /= other
        return self

    @singledispatchmethod
    def __ipow__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__ipow__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__ipow__.register(int)
    @__ipow__.register(float)
    def _(self, other):
        if self._expr['factor'] == 0:
            self._expr['degree'] = 1
        else:
            self._expr['degree'] *= other

        self._expr['factor'] **= other
        self._expr['whole'] **= other
        return self

    @singledispatchmethod
    def __iadd__(self, other):
        if isinstance(other, Symbol):
            if self.var == other.var and self.degree == other.degree:
                self.factor += other.factor
                return self
            else:
                return Symbol.__iadd__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__iadd__.register(int)
    @__iadd__.register(float)
    def _(self, other):
        if self._expr['whole'] == 0:
            self._expr['whole'] = other
        else:
            self._expr['whole'] += other
        return self

    @singledispatchmethod
    def __isub__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__isub__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__isub__.register(int)
    @__isub__.register(float)
    def _(self, other):
        if self._expr['whole'] == 0:
            self._expr['whole'] = other
        else:
            self._expr['whole'] -= other
        return self

    @singledispatchmethod
    def __mul__(self, other):
        if isinstance(other, (Symbol, Expression)):
            polynomial_terms = []
            other_items = (other.term, other.whole) if isinstance(other, Symbol) \
                else other.symbols

            i = 1

            for arg_1 in (self.term, self.whole):
                for arg_2 in other_items:
                    match (arg_1, arg_2):
                        case (Symbol(), Symbol()):
                            if arg_1.var == arg_2.var:
                                _f = Symbol(self.var)
                                _f.degree = arg_1.degree + arg_2.degree
                            else:
                                # Still working
                                pass

                            _f.factor = arg_1.factor * arg_2.factor

                        case (Symbol(), int() | float()):
                            _f = Symbol(arg_1.var)
                            _f.degree = arg_1.degree
                            _f.factor = arg_1.factor * arg_2

                        case (int() | float(), Symbol()):
                            _f = Symbol(arg_2.var)
                            _f.degree = arg_2.degree
                            _f.factor = arg_1 * arg_2.factor

                        case _:
                            _f = arg_1 * arg_2

                    if Symbol.with_print:
                        print(f"{i}) {arg_1} * {arg_2} = {str(_f)}")
                    polynomial_terms.append(_f)
                    i += 1

            if Symbol.with_print:
                print(list(map(str, polynomial_terms)))
            return Expression(polynomial_terms)

        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or '{Expression.__name__}' or digit: 'int', 'float'.")

    @__mul__.register(int)
    @__mul__.register(float)
    def _(self, other):
        f = Symbol(self._symbol)
        f.factor = self.factor * other
        f.degree = self.degree
        f.whole = self.whole * other
        return f

    @singledispatchmethod
    def __truediv__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__truediv__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__truediv__.register(int)
    @__truediv__.register(float)
    def _(self, other):
        f = Symbol(self._symbol)
        f.factor = self.factor / other
        f.degree = self.degree
        f.whole = self.whole / other
        return f

    @singledispatchmethod
    def __pow__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__pow__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int'.")

    @__pow__.register(int)
    def _(self, other):
        if other == 0:
            return 1

        f = self
        for i in range(other - 1):
            f = f * self

        return f

    @singledispatchmethod
    def __add__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__add__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__add__.register(int)
    @__add__.register(float)
    def _(self, other):
        f = Symbol(self._symbol)
        f.factor = self.factor
        f.degree = self.degree
        f.whole = self.whole + other
        return f

    @singledispatchmethod
    def __sub__(self, other):
        if isinstance(other, Symbol):
            return Symbol.__sub__.__name__ + ' Still working'
        else:
            raise ValueError(f"Cannot format value of type '{type(other).__name__}' " + \
                             f"must be '{Symbol.__name__}' or digit: 'int', 'float'.")

    @__sub__.register(int)
    @__sub__.register(float)
    def _(self, other):
        f = Symbol(self._symbol)
        f.factor = self.factor
        f.degree = self.degree
        f.whole = self.whole - other
        return f

    def __abs__(self):
        self.factor = abs(self.factor)
        return self

    def __str__(self):
        return self.expression
