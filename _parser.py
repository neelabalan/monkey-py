# A parser is a software component that takes input data (frequently text) and builds
# a data structure – often some kind of parse tree, abstract syntax tree or other
# hierarchical structure – giving a structural representation of the input, checking for
# correct syntax in the process. […] The parser is often preceded by a separate lexical
# analyser, which creates tokens from the sequence of input characters

import enum
import types
import typing

import typing_extensions

import _abstract_syntax_tree as _ast
import _lexer
import _token


class Precedence(enum.IntEnum):
    LOWEST = 1
    # ==
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


precendence_map = types.MappingProxyType(
    {
        _token.TokenType.EQ: Precedence.EQUALS,
        _token.TokenType.NOT_EQ: Precedence.EQUALS,
        _token.TokenType.LT: Precedence.LESSGREATER,
        _token.TokenType.GT: Precedence.LESSGREATER,
        _token.TokenType.PLUS: Precedence.SUM,
        _token.TokenType.MINUS: Precedence.SUM,
        _token.TokenType.SLASH: Precedence.PRODUCT,
        _token.TokenType.ASTERISK: Precedence.PRODUCT,
    }
)


class Parser:
    def __init__(self, lexer: _lexer.Lexer):
        self.lexer = lexer
        self._current_token = None
        self._peek_token = None

        self.next_token()
        self.next_token()

        self._register_infix_parse_functions()
        self._register_prefix_parse_functions()

    def _register_prefix_parse_functions(self):
        self.prefix_parse_functions = types.MappingProxyType(
            {
                _token.TokenType.IDENT: self._parse_identifier,
                _token.TokenType.INT: self._parse_integer_literal,
                _token.TokenType.BANG: self._parse_prefix_expression,
                _token.TokenType.MINUS: self._parse_prefix_expression,
                _token.TokenType.TRUE: self._parse_boolean,
                _token.TokenType.FALSE: self._parse_boolean,
                _token.TokenType.LPAREN: self._parse_group_expression,
                _token.TokenType.IF: self._parse_if_expression,
                _token.TokenType.FUNCTION: self._parse_function_literal,
                _token.TokenType.STRING: self._parse_string_literal,
                _token.TokenType.LBRACKET: self._parse_array_literal,
                _token.TokenType.LBRACE: self._parse_hash_literal,
            }
        )

    def _register_infix_parse_functions(self):
        self.infix_parse_functions = types.MappingProxyType(
            {
                _token.TokenType.PLUS: self._parse_infix_expression,
                _token.TokenType.MINUS: self._parse_infix_expression,
                _token.TokenType.SLASH: self._parse_infix_expression,
                _token.TokenType.ASTERISK: self._parse_infix_expression,
                _token.TokenType.EQ: self._parse_infix_expression,
                _token.TokenType.NOT_EQ: self._parse_infix_expression,
                _token.TokenType.LT: self._parse_infix_expression,
                _token.TokenType.GT: self._parse_infix_expression,
                _token.TokenType.LPAREN: self._parse_call_expression,
                _token.TokenType.LBRACKET: self._parse_index_expression,
            }
        )

    def _parse_group_expression(self): ...

    def _parse_if_expression(self): ...

    def _parse_function_literal(self): ...

    def _parse_string_literal(self): ...

    def _parse_array_literal(self): ...

    def _parse_hash_literal(self): ...

    def _parse_call_expression(sefl): ...

    def _parse_index_expression(self): ...

    def _parse_boolean(self):
        return _ast.Boolean(token=self._current_token, value=self._current_token.token_type == _token.TokenType.TRUE)

    def _parse_integer_literal(self):
        return _ast.IntegerLiteral(token=self._current_token, value=int(self._current_token.literal))

    def _parse_prefix_expression(self):
        current_token = self._current_token
        return _ast.PrefixExpression(
            current_token, operator=current_token.literal, right=self.next_token()._parse_expression(Precedence.PREFIX)
        )

    def _parse_infix_expression(self, left: _ast.Expression):
        current_token = self._current_token
        precedence = precendence_map.get(self._current_token.token_type) or Precedence.LOWEST

        return _ast.InfixExpression(
            token=current_token, operator=current_token.literal, left=left, right=self.next_token()._parse_expression(precedence)
        )

    def next_token(self) -> typing_extensions.Self:
        self._current_token = self._peek_token
        self._peek_token = self.lexer.next_token()
        return self

    def parse_program(self) -> typing.Optional[_ast.Program]:
        program = _ast.Program([])
        while self._current_token.token_type not in (_token.TokenType.EOF, _token.TokenType.ILLEGAL):
            statement = self._parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()
        return program

    def _parse_statement(self) -> typing.Optional[_ast.Statement]:
        match self._current_token.token_type:
            case _token.TokenType.LET:
                return self._parse_let_statement()
            case _token.TokenType.RETURN:
                return self._parse_return_statement()
            case _:
                return self._parse_expression_statement()

    def _parse_expression(self, precendence: Precedence) -> _ast.Expression:
        prefix = self.prefix_parse_functions.get(self._current_token.token_type)
        if not prefix:
            return None
        left_exp = prefix()

        while self._peek_token.token_type != _token.TokenType.SEMICOLON and precendence < precendence_map.get(
            self._peek_token.token_type, Precedence.LOWEST
        ):
            infix = self.infix_parse_functions.get(self._peek_token.token_type)
            if not infix:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

    def _parse_identifier(self) -> _ast.Expression:
        return _ast.Identifier(self._current_token, value=self._current_token.literal)

    def _parse_expression_statement(self) -> _ast.Expression:
        statement = _ast.ExpressionStatement(
            token=self._current_token, expression=self._parse_expression(Precedence.LOWEST)
        )
        if self._peek_token.token_type == _token.TokenType.SEMICOLON:
            self.next_token()
        return statement

    def _parse_return_statement(self):
        token = self._current_token

        return_value = self.next_token()._parse_expression_statement()

        if self._peek_token.token_type == _token.TokenType.SEMICOLON:
            self.next_token()
        return _ast.ReturnStatement(token, return_value)

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
