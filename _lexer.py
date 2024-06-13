from _token import TokenType
from _token import Token
from _token import keyword_map
from datastructure import Char
import typing
# import types #MappingProxyType


class Lexer:
    def __iter__(self):
        raise NotImplementedError("iterator not implmeneted")

    def __init__(self, source_code: str):
        self.source_code = source_code
        self._read_position = 0
        self._position = 0
        self._char = Char("")

        self._read_char()

    def _read_char(self):
        if self._read_position >= len(self.source_code):
            self._char = Char("")
        else:
            self._char = Char(self.source_code[self._read_position])
        self._position = self._read_position
        self._read_position += 1

    def handle_not_operator(self):
        token = None
        ch = self._char
        if self._peek_char() == '=':
            self._read_char()
            token = Token(literal=ch+self._char, token_type=TokenType.NOT_EQ)
        else:
            token = Token(literal=ch, token_type=TokenType.BANG) 
        return token

    def handle_assign_operator(self):
        token = None
        ch = self._char
        if self._peek_char() == '=':
            self._read_char()
            token = Token(literal=ch+self._char, token_type=TokenType.EQ)
        else:
            token = Token(literal=ch, token_type=TokenType.ASSIGN) 
        return token

    def token_lookup(self, key: Char) -> Token:
        simple_token_type_map: dict[Char, TokenType] = {
            Char("+"): TokenType.PLUS,
            Char("("): TokenType.LPAREN,
            Char(")"): TokenType.RPAREN,
            Char("{"): TokenType.LBRACE,
            Char("}"): TokenType.RBRACE,
            Char(","): TokenType.COMMA,
            Char(";"): TokenType.SEMICOLON,
            Char(""): TokenType.EOF,
        }
        function_token_map: dict[Char, typing.Callable] = {
            Char("!"): self.handle_not_operator,
            Char("="): self.handle_assign_operator
        }
        token = None
        if token_type := simple_token_type_map.get(key):
            token = Token(literal=str(key), token_type = token_type)
        else:
            token_handler_func = function_token_map.get(key)
            if token_handler_func:
                token = token_handler_func()
        return token


    def skip_whitespace(self):
        while self._char in (Char(" "), Char("\t"), Char("\n"), Char("\r")):
            self._read_char()

    def _peek_char(self):
        if self._read_position >= len(self.source_code):
            return 0
        else:
            return self.source_code[self._read_position]

    def next_token(self) -> Token:
        self.skip_whitespace()
        token = self.token_lookup(self._char)
        if not token:
            if self._char.isalpha():
                identifier = self._read_identifier()
                keyword = keyword_map.get(identifier)
                return Token(literal=identifier, token_type=keyword) if keyword else Token(literal=identifier, token_type=TokenType.IDENT)
            elif self._char.isdigit():
                return Token(literal=self._read_number(), token_type=TokenType.INT)
            elif self._char.strip() == Char(""):
                return TokenType(literal="", token_type=TokenType.EOF)
            else:
                return Token(literal=self._char, token_type=TokenType.ILLEGAL)
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
