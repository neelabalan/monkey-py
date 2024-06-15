from _lexer import Lexer
from _token import TokenType


def test_next_token():
    input = '=+()\{\},;'
    lexer = Lexer(input)

    assert lexer.next_token().token_type == TokenType.ASSIGN
    assert lexer.next_token().token_type == TokenType.PLUS


def test_complex_token():
    source_code = """
let five = 5;
let ten = 10;

let add = fn(x, y) {
    x + y;
};

let result = add(five, ten);
"""
    lexer = Lexer(source_code)
    assert lexer.next_token().token_type == TokenType.LET
    assert lexer.next_token().token_type == TokenType.IDENT
    assert lexer.next_token().token_type == TokenType.ASSIGN
    assert lexer.next_token().token_type == TokenType.INT
    assert lexer.next_token().token_type == TokenType.SEMICOLON
    assert lexer.next_token().token_type == TokenType.LET


def test_function_calling():
    lexer = Lexer('== !=')
    assert lexer.next_token().token_type == TokenType.EQ
    assert lexer.next_token().token_type == TokenType.NOT_EQ


# def test_invalid_inputs():
#     source_code = """
# let five = 5;
# let ten = 10;
# let add = fn(x, y) {
#     x + y;
# };

# let result = add(five, ten);

# !-/*5;

# 5 < 10 > 5;

# if (5 < 10) {
#     return true;
# } else {
#     return false;
# }
# // [...]
# """
#     lexer = Lexer(source_code)
#     while True:
#         token = lexer.next_token()
#         assert not token.token_type == TokenType.ILLEGAL
#         if token.token_type == TokenType.EOF:
#             break
#         # if token.token_type == TokenType.ILLEGAL:
#         #     break
