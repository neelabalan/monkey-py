import typing

import _token
from datastructure import Char

# import types #MappingProxyType


class Lexer:
    def __iter__(self):
        raise NotImplementedError('iterator not implmeneted')

    def __init__(self, source_code: str):
        self.source_code = source_code
        self._read_position = 0
        self._position = 0
        self._char = Char('')

        self._read_char()

    def _read_char(self):
        if self._read_position >= len(self.source_code):
            self._char = Char('')
        else:
            self._char = Char(self.source_code[self._read_position])
        self._position = self._read_position
        self._read_position += 1

    def handle_not_operator(self):
        token = None
        ch = self._char
        if self._peek_char() == '=':
            self._read_char()
            token = _token.Token(literal=ch + self._char, token_type=_token.TokenType.NOT_EQ)
        else:
            token = _token.Token(literal=ch, token_type=_token.TokenType.BANG)
        return token

    def handle_assign_operator(self):
        token = None
        ch = self._char
        if self._peek_char() == '=':
            self._read_char()
            token = _token.Token(literal=ch + self._char, token_type=_token.TokenType.EQ)
        else:
            token = _token.Token(literal=ch, token_type=_token.TokenType.ASSIGN)
        return token

    def token_lookup(self, key: Char) -> _token.Token:
        simple_token_type_map: dict[Char, _token.TokenType] = {
            Char('+'): _token.TokenType.PLUS,
            Char('('): _token.TokenType.LPAREN,
            Char(')'): _token.TokenType.RPAREN,
            Char('{'): _token.TokenType.LBRACE,
            Char('}'): _token.TokenType.RBRACE,
            Char(','): _token.TokenType.COMMA,
            Char(';'): _token.TokenType.SEMICOLON,
            Char(''): _token.TokenType.EOF,
        }
        function_token_map: dict[Char, typing.Callable] = {
            Char('!'): self.handle_not_operator,
            Char('='): self.handle_assign_operator,
        }
        token = None
        if token_type := simple_token_type_map.get(key):
            token = _token.Token(literal=str(key), token_type=token_type)
        else:
            token_handler_func = function_token_map.get(key)
            if token_handler_func:
                token = token_handler_func()
        return token

    def skip_whitespace(self):
        while self._char in (Char(' '), Char('\t'), Char('\n'), Char('\r')):
            self._read_char()

    def _peek_char(self):
        if self._read_position >= len(self.source_code):
            return 0
        else:
            return self.source_code[self._read_position]

    def next_token(self) -> _token.Token:
        self.skip_whitespace()
        token = self.token_lookup(self._char)
        if not token:
            if self._char.isalpha():
                identifier = self._read_identifier()
                keyword = _token.keyword_map.get(identifier)
                return (
                    _token.Token(literal=identifier, token_type=keyword)
                    if keyword
                    else _token.Token(literal=identifier, token_type=_token.TokenType.IDENT)
                )
            elif self._char.isdigit():
                return _token.Token(literal=self._read_number(), token_type=_token.TokenType.INT)
            elif self._char.strip() == Char(''):
                return _token.TokenType(literal='', token_type=_token.TokenType.EOF)
            else:
                return _token.Token(literal=self._char, token_type=_token.TokenType.ILLEGAL)
        self._read_char()
        return token

    def _read_number(self):
        position = self._position
        while self._char.isdigit():
            self._read_char()
        return self.source_code[position : self._position]

    def _read_identifier(self):
        position = self._position
        while self._char.isalpha():
            self._read_char()
        return self.source_code[position : self._position]

    def _handle_not_operator(self): ...
