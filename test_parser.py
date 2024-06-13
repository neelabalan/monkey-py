from _parser import Parser
from _lexer import Lexer

def test_let_statements():
    source = """
    let x = 5;
    let y = 10;
    let foobar = 131313;
"""
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 3
    identifers = ["x", "y", "foobar"]
    for idx, statement in enumerate(program.statements):
        assert statement.token_literal() == "let"
