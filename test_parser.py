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


def test_prefix_expression_parsing():
    lexer = _lexer.Lexer('!true;')
    parser = _parser.Parser(lexer)
    program = parser.parse_program()
    expression_statement = program.statements[0]
    assert isinstance(expression_statement, _ast.ExpressionStatement)
    assert isinstance(expression_statement.expression, _ast.PrefixExpression)


def test_infix_expression_parsing():
    test_cases = [
        ('!-a', '(!(-a))'),
        ('a+b+c', '((a + b) + c)'),
        (
            'a + b - c',
            '((a + b) - c)',
        ),
        (
            'a * b * c',
            '((a * b) * c)',
        ),
        (
            'a * b / c',
            '((a * b) / c)',
        ),
        (
            'a + b / c',
            '(a + (b / c))',
        ),
        (
            'a + b * c + d / e - f',
            '(((a + (b * c)) + (d / e)) - f)',
        ),
        (
            '3 + 4; -5 * 5',
            '(3 + 4)((-5) * 5)',
        ),
        (
            '5 > 4 == 3 < 4',
            '((5 > 4) == (3 < 4))',
        ),
        (
            '5 < 4 != 3 > 4',
            '((5 < 4) != (3 > 4))',
        ),
        (
            '3 + 4 * 5 == 3 * 1 + 4 * 5',
            '((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))',
        ),
    ]
    for test_case in test_cases:
        lexer = _lexer.Lexer(test_case[0])
        parser = _parser.Parser(lexer)
        program = parser.parse_program()
        assert program.statements
        assert program.to_string() == test_case[1]
