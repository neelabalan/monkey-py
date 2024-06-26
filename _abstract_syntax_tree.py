import abc
import typing

from _token import Token


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
        return self.token.literal

    def to_string(self) -> str:
        return self.token.literal


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
            return ''

    def to_string(self) -> str:
        result = ''
        for s in self.statements:
            result += s.to_string()
        return result


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
        result = self.token_literal() + ' ' + self.name.to_string() + ' = '
        if self.value:
            result += self.value.to_string()
        result += ';'
        return result


class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Expression):
        self.token = token
        self.return_value = return_value

    def token_literal(self) -> str:
        return self.token.literal

    def to_string(self) -> str:
        result = self.token_literal() + ' '

        if not self.return_value:
            result += self.return_value.to_string()

        result += ';'
        return result


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

    def token_literal(self) -> str:
        return self.token.literal

    def to_string(self) -> str:
        if self.expression:
            return self.expression.to_string()
        return ''


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int):
        self.token = token
        self.value = value


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression):
        self.token = token
        self.operator = operator
        self.right = right

    def to_string(self) -> str:
        return '(' + self.operator + self.right.to_string() + ')'


class InfixExpression(Expression):
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def to_string(self) -> str:
        return '(' + self.left.to_string() + ' ' + self.operator + ' ' + self.right.to_string() + ')'


class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value


class BlockStatement(Statement):
    def __init__(self, token: Token, statements: list[Statement]):
        super(BlockStatement, self).__init__(token)
        self.statements = statements

    def to_string(self):
        return ''.join([statement.to_string() for statement in self.statements])


class IfExpression(Expression):
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: BlockStatement):
        self.token = token
        self.condition = condition
        self.consquence = consequence
        self.alternative = alternative

    def to_string(self) -> str:
        alternative_str = ''
        if self.alternative:
            alternative_str = 'else ' + self.alternative.to_string()
        return 'if' + self.condition.to_string() + ' ' + self.consquence.to_string() + alternative_str
