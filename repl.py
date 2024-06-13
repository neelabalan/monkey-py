from _lexer import Lexer
from _token import TokenType

def run():
    while True:
        source = input("\n> ")
        # source = "==="
        lexer = Lexer(source)
        token_type = None
        while True:
            token = lexer.next_token()
            token_type = token.token_type
            if token_type == TokenType.ILLEGAL or token_type == TokenType.EOF:
                break
            print(f"{token.literal} -> {token.token_type}")

if __name__ == "__main__":
    run()