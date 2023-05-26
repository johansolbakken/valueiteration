"""
statement = board_definition | value_definition | block_definition
board_definition = BOARD UINT X UINT
value_definition = SET UINT COMMA UINT TO number
number = UINT | FLOAT | INT
block_definition = BLOCK UINT COMMA UINT
"""

from lexer import Lexer, TokenType
from spec import Spec


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.lex()
        self.spec = Spec()

    def parse(self) -> Spec:
        self.statement()
        return self.spec

    def statement(self):
        if self.current_token.type == TokenType.BOARD:
            self.board_definition()
        elif self.current_token.type == TokenType.SET:
            self.value_definition()
        elif self.current_token.type == TokenType.BLOCK:
            self.block_definition()
        if self.current_token.type != TokenType.EOF:
            self.statement()

    def board_definition(self):
        self.eat(TokenType.BOARD)
        height = self.eat(TokenType.UINT)
        self.eat(TokenType.X)
        width = self.eat(TokenType.UINT)
        self.spec.set_width(width.value)
        self.spec.set_height(height.value)

    def value_definition(self):
        self.eat(TokenType.SET)
        x = self.eat(TokenType.UINT)
        self.eat(TokenType.COMMA)
        y = self.eat(TokenType.UINT)
        self.eat(TokenType.TO)
        value = self.number().value
        self.spec.add_value(x.value, y.value, value)

    def block_definition(self):
        self.eat(TokenType.BLOCK)
        x = self.eat(TokenType.UINT)
        self.eat(TokenType.COMMA)
        y = self.eat(TokenType.UINT)
        self.spec.add_block(x.value, y.value)

    def number(self):
        if self.current_token.type == TokenType.UINT:
            return self.eat(TokenType.UINT)
        elif self.current_token.type == TokenType.FLOAT:
            return self.eat(TokenType.FLOAT)
        elif self.current_token.type == TokenType.INT:
            return self.eat(TokenType.INT)
        else:
            raise Exception(f"Invalid number: {self.current_token.value}")

    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            token = self.current_token
            self.current_token = self.lexer.lex()
            return token
        else:
            raise Exception(f"Invalid token: {self.current_token.value}")

if __name__ == "__main__":
    lexer = Lexer("""
    board 3 x 4
set 3, 0 to 1
set 3, 1 to -1
block 1,1""")
    parser = Parser(lexer)
    spec = parser.parse()
    print(spec)
