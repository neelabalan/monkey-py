# A parser is a software component that takes input data (frequently text) and builds
# a data structure – often some kind of parse tree, abstract syntax tree or other
# hierarchical structure – giving a structural representation of the input, checking for
# correct syntax in the process. […] The parser is often preceded by a separate lexical
# analyser, which creates tokens from the sequence of input characters

import typing

import _abstract_syntax_tree as _ast
import _lexer
import _token


class Parser:
    def __init__(self, lexer: _lexer.Lexer):
        self.lexer = lexer
        self._current_token = None
        self._peek_token = None

        self.next_token()
        self.next_token()

    def next_token(self):
        self._current_token = self._peek_token
        self._peek_token = self.lexer.next_token()

    def parse_program(self) -> typing.Optional[_ast.Program]:
        program = _ast.Program()
        while self._current_token.token_type not in (_token.TokenType.EOF, _token.TokenType.ILLEGAL):
            statement = self._parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()
        return program

    def _parse_statement(self) -> typing.Optional[_ast.Statement]:
        if self._current_token.token_type == _token.TokenType.LET:
            return self._parse_let_statement()
        elif self._current_token.token_type == _token.TokenType.RETURN:
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_expression_statement(self) -> _ast.Expression:
        # statement = _ast.ExpressionStatement(token=self._current_token)
        pass

    def _parse_return_statement(self):
        pass

    def _expect_peek(self, token_type: _token.TokenType) -> bool:
        if self._peek_token.token_type == token_type:
            self.next_token()
            return True
        else:
            raise SyntaxError(f'Unexpected {token_type}')

    def _parse_let_statement(self) -> typing.Optional[_ast.LetStatement]:
        token = self._current_token

        if not self._expect_peek(_token.TokenType.IDENT):
            return None

        identifier = _ast.Identifier(token=self._current_token, value=self._current_token.literal)

        # skip the expression for now
        while self._current_token.token_type != _token.TokenType.SEMICOLON:
            self.next_token()
        statement = _ast.LetStatement(token=token, name=identifier, value=None)
        return statement
