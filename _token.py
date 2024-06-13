import dataclasses
import enum
import types


# lexer -> It will take source code as input and output the tokens that represent the source code
@enum.unique
class TokenType(enum.Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"  # 1343456

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"

    LT = "<"
    GT = ">"

    EQ = "=="
    NOT_EQ = "!="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"


keyword_map: dict[str, TokenType] = types.MappingProxyType(
    {"fn": TokenType.FUNCTION, "let": TokenType.LET, "true": TokenType.TRUE, "false": TokenType.FALSE, "if": TokenType.IF, "else": TokenType.ELSE, "return": TokenType.RETURN}
)


@dataclasses.dataclass(frozen=True)
class Token:
    literal: str
    token_type: TokenType
