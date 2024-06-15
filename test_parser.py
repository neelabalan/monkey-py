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
