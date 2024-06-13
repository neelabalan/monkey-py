import abc
from _token import Token
import io


class Node(abc.ABC):
    @abc.abstractmethod
    def token_literal(self) -> str:
        pass

    @abc.abstractmethod
    def to_string(self) -> str:
        pass


class Statement(Node):
    @abc.abstractmethod
    def statement_node(self):
        pass


class Expression(Node):
    @abc.abstractmethod
    def expression_node(self):
        pass


#  going to be the root node of every AST our parser produces
class Program(Node):
    def __init__(self, statements: list[Statement] = []):
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def to_string(self) -> str:
        out = io.StringIO()
        for s in self.statements:
            out.write(s.to_string())
        return out.getvalue()


class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def to_string(self) -> str:
        return self.token.literal


class LetStatement(Statement):
    def __init__(self, token: Token, name: Identifier, value: Expression):
        self.token = token
        self.name = name
        self.value = value

    def statement_node(self): ...
    def token_literal(self) -> str:
        return self.token.literal

    def to_string(self) -> str:
        out = io.StringIO()
        out.write(self.token_literal() + " ")
        out.write(self.name.to_string())
        out.write(" = ")
        if self.value:
            out.write(self.value.to_string())
        out.write(";")
        return out.getvalue()
