import _lexer
import _parser


def run():
    while True:
        source = input('\n> ')
        # source = "==="
        lexer = _lexer.Lexer(source)
        parser = _parser.Parser(lexer)
        program = parser.parse_program()
        print(program.to_string())

        # while True:
        #     token = lexer.next_token()
        #     token_type = token.token_type
        #     if token_type == _token.TokenType.ILLEGAL or token_type == _token.TokenType.EOF:
        #         break
        #     print(f'{token.literal} -> {token.token_type}')


if __name__ == '__main__':
    run()
