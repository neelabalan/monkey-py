import abc
from _token import Token
import io


class AbstractNode(abc.ABC):
    @abc.abstractmethod
    def token_literal(self) -> str:
        pass

    @abc.abstractmethod
    def to_string(self) -> str:
        pass

class BaseNode(AbstractNode):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.token_literal

    def to_string(self) -> str:
        return self.token.token_literal



class Statement(BaseNode):
    def __init__(self, token: Token):
        super().__init__(token)


class Expression(BaseNode):
    def __init__(self, token: Token):
        super().__init__(token)


#  going to be the root node of every AST our parser produces
class Program(BaseNode):
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
        return self.value


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

class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Expression):
        self.token = token
        self.return_value = return_value

    def token_literal(self) -> str:
        return self.token.literal

    def to_string(self) -> str:
        out = io.StringIO()
        out.write(self.token_literal() + " ")

        if not self.return_value:
            out.write(self.return_value.to_string())

        out.write(";")
        return out.getvalue()

class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

    def token_literal(self) -> str:
        return self.token.literal

    def to_string(self) -> str:
        if not self.expression:
            return self.expression.to_string()
        return ""
