"""board 3 x 4
set 3, 0 to 1
set 3, 1 to -1
block 1,1"""

# a lexer that takes in a source and makes a list of tokens

import re
from enum import Enum


class TokenType(Enum):
    SET = "SET"
    BLOCK = "BLOCK"
    INT = "INT"
    UINT = "UINT"
    FLOAT = "FLOAT"
    TO = "TO"
    BOARD = "BOARD"
    EOF = "EOF"
    X = "X"
    COMMA = "COMMA"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    """
    Takes in a source and has a function lex() that uses re and returns one token.
    """

    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.current_char = self.source[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self):
        if self.pos + 1 >= len(self.source):
            return None
        else:
            return self.source[self.pos + 1]

    def lex(self):
        self.skip_whitespace()

        if self.current_char is None:
            return Token(TokenType.EOF, None)

        if self.current_char == ",":
            self.advance()
            return Token(TokenType.COMMA, ",")

        if re.match("[a-z]", self.current_char):
            start = self.pos
            while re.match("[a-z]", self.current_char):
                self.advance()
            word = self.source[start:self.pos]
            if word == "set":
                return Token(TokenType.SET, word)
            elif word == "block":
                return Token(TokenType.BLOCK, word)
            elif word == "to":
                return Token(TokenType.TO, word)
            elif word == "board":
                return Token(TokenType.BOARD, word)
            elif word == "x":
                return Token(TokenType.X, word)
            else:
                raise Exception(f"Invalid command: {word}")

        if re.match("-|[0-9]", self.current_char):
            start = self.pos
            while self.current_char is not None and re.match("-|[0-9]|\.", self.current_char):
                self.advance()
            number = self.source[start:self.pos]
            if re.match("[1-9][0-9]*|0", number):
                return Token(TokenType.UINT, int(number))
            if re.match("-?[1-9][0-9]*", number):
                return Token(TokenType.INT, int(number))
            if re.match("-?[1-9][0-9]*\.[0-9]+", number):
                return Token(TokenType.FLOAT, float(number))
            if re.match("-?0\.[0-9]+", number):
                return Token(TokenType.FLOAT, float(number))
            raise Exception(f"Invalid number: {number}")

        raise Exception(f"Invalid character: {self.current_char}")


if __name__ == "__main__":
    lexer = Lexer("""
    board 3 x 4
set 3, 0 to 1
set 3, 1 to -1
block 1,1""")
    token = lexer.lex()
    while token.type != TokenType.EOF:
        print(token.type, token.value)
        token = lexer.lex()
