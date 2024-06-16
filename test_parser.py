import pytest

import _abstract_syntax_tree as _ast
import _lexer
import _parser


def test_let_statements():
    source = """
    let x = 5;
    let y = 10;
    let foobar = 131313;
    """
    lexer = _lexer.Lexer(source)
    parser = _parser.Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 3
    identifers = ['x', 'y', 'foobar']
    for idx, statement in enumerate(program.statements):
        assert statement.token_literal() == 'let'
        assert isinstance(statement, _ast.LetStatement)
        assert statement.name.token_literal() == identifers[idx]


def test_let_statement_errors():
    error_cases = ['let = 5', 'let 123 = 123']
    for error_case in error_cases:
        lexer = _lexer.Lexer(error_case)
        parser = _parser.Parser(lexer)
        with pytest.raises(SyntaxError):
            _ = parser.parse_program()


def test_int_parsing():
    lexer = _lexer.Lexer('5;')
    parser = _parser.Parser(lexer)
    program = parser.parse_program()
    expression_statement = program.statements[0]
    assert isinstance(expression_statement, _ast.ExpressionStatement)
    assert isinstance(expression_statement.expression, _ast.IntegerLiteral)
