# coding=utf-8
import ply.lex as lex
import re


class Lexer:
    states = (
        ('string', 'exclusive'),
    )

    """ Базовый синтаксис языка """

    tokens = ["PLUS", "MINUS", "LESS_OR_EQUAL", "MORE_OR_EQUAL", "COMMA", "DEGREE", "OPEN", "MOD", "DIV", "LESS",
              "MORE", "CLOSE",
              "OPEN_BRACKET", "CLOSE_BRACKET", "NOT_EQUAL", "T_COMMA", "COLON", "ID", "ASSIGN", "EQUAL",
              "QUOM", "STRING"]

    """ Зарезервированные переменные  """

    reserved = {
        "si": "IF",
        "encore": "ELSE",

        "alors_que": "WHILE",

        "pour": "FOR",
        "continuer": "CONTINUE",
        "interrompre": "BREAK",

        "fonction": "FUNCTION",
        "dos": "RETURN",

        "et": "AND",
        "ou": "OR",
        "pas": "NOT",

        "saisir": "READ",
        "print": "WRITE",

        "var": "VAR",
        "glob": "GVAR",
        "int": "NUMBERS",
        "float": "FLOAT_NUMBER"
    }

    tokens = tokens + list(reserved.values())

    ident = r'[a-z]\w*'

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MOD = r'\%'
    t_DIV = r'\//'
    t_LESS_OR_EQUAL = r"<="
    t_MORE_OR_EQUAL = r">="
    t_LESS = "<"
    t_MORE = ">"
    t_COMMA = r","
    t_DEGREE = r'\^|\*'
    t_NUMBERS = r"\d+"
    t_STRING = r'"(\\.|[^"])*"'
    t_OPEN = r"\{"
    t_CLOSE = r"\}"
    t_OPEN_BRACKET = r'\('
    t_CLOSE_BRACKET = r'\)'
    t_ASSIGN = r'='
    t_EQUAL = r'=='
    t_NOT_EQUAL = r"(!=)|(<>)"
    t_T_COMMA = r";"
    t_ignore = ' \r\t\f'
    t_string_ignore = ''

    def __init__(self):
        self.lexer = None

    def t_FLOAT_NUMBER(self, t):
        r'\d+\.\d+'
        '[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
        t.value = float(t.value)
        return t

    def t_ANY_STRING(self, t):
        r'"'
        if t.lexer.current_state() == 'string':
            t.lexer.begin('INITIAL')  # переходим в начальное состояние
        else:
            t.lexer.begin('string')  # парсим строку
        return t

    def t_comment(self, t):
        r'@(\\.|[^@])+@'
        pass

    def t_ID(self, t):
        r'[a-z]\w*'
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        return t

    def t_string_error(self, t):
        print("Неверный символ '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Неверный символ '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs, reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)

    def main(self, path_file):

        f = open(path_file, 'r')
        program = f.read()

        self.lexer.input(program)

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print("tok: ", tok)
