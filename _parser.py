# A parser is a software component that takes input data (frequently text) and builds
# a data structure – often some kind of parse tree, abstract syntax tree or other
# hierarchical structure – giving a structural representation of the input, checking for
# correct syntax in the process. […] The parser is often preceded by a separate lexical
# analyser, which creates tokens from the sequence of input characters

from _lexer import Lexer
from _token import TokenType
import typing
from _ab_syn_tree import Program
from _ab_syn_tree import Statement
from _ab_syn_tree import LetStatement


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self._current_token = None
        self._peek_token = None

    def next_token(self):
        self._current_token = self._peek_token
        self._peek_token = self.lexer.next_token()

    def parse_program(self) -> typing.Optional[Program]:
        program = Program()
        while self._current_token != TokenType.EOF:
            statement = self.parse_statement()
            if not statement:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self) -> typing.Optional[Statement]:
        if self._current_token.token_type == TokenType.LET:
            return self.parse_let_statement()

    def parse_let_statement(self) -> LetStatement:
        ...

