"""
lexer.py - Lexical Analyzer for the TUI Visual Compiler
Converts raw text into a stream of tokens (type, value, line, col)
without terminating on unrecognized characters.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TokenType(Enum):
    # Keywords
    KEYWORD_LET = auto()
    KEYWORD_IF = auto()
    TYPE_INT = auto()
    TYPE_BOOL = auto()
    TYPE_STRING = auto()
    BOOL_LITERAL = auto()

    # Identifiers & Literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING_LITERAL = auto()

    # Operators
    ASSIGN = auto()          # =
    EQ = auto()              # ==
    NEQ = auto()             # !=
    LT = auto()              # <
    LTE = auto()             # <=
    GT = auto()              # >
    GTE = auto()             # >=
    PLUS = auto()            # +
    MINUS = auto()           # -
    STAR = auto()            # *
    SLASH = auto()           # /

    # Delimiters
    COLON = auto()           # :
    SEMICOLON = auto()       # ;
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACE = auto()          # {
    RBRACE = auto()          # }

    # Meta Tokens
    UNKNOWN = auto()         # Deliberate error containment
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, Ln {self.line}, Col {self.column})"


KEYWORDS = {
    "let": TokenType.KEYWORD_LET,
    "if": TokenType.KEYWORD_IF,
    "int": TokenType.TYPE_INT,
    "bool": TokenType.TYPE_BOOL,
    "string": TokenType.TYPE_STRING,
    "true": TokenType.BOOL_LITERAL,
    "false": TokenType.BOOL_LITERAL,
}


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        return self.source[idx] if idx < self.length else "\0"

    def _advance(self) -> str:
        ch = self._peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.length:
            ch = self._peek()

            # Ignore whitespace
            if ch in (" ", "\t", "\r", "\n"):
                self._advance()
                continue

            start_line = self.line
            start_col = self.column

            # Identifiers and Keywords
            if ch.isalpha() or ch == "_":
                ident = ""
                while self._peek().isalnum() or self._peek() == "_":
                    ident += self._advance()
                token_type = KEYWORDS.get(ident, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, ident, start_line, start_col))
                continue

            # Numeric Literals
            if ch.isdigit():
                num = ""
                while self._peek().isdigit():
                    num += self._advance()
                tokens.append(Token(TokenType.NUMBER, num, start_line, start_col))
                continue

            # String Literals
            if ch == '"':
                self._advance()  # Skip opening quote
                literal = ""
                while self._peek() not in ('"', "\0", "\n"):
                    literal += self._advance()
                if self._peek() == '"':
                    self._advance()  # Skip closing quote
                    tokens.append(Token(TokenType.STRING_LITERAL, literal, start_line, start_col))
                else:
                    # Unterminated string
                    tokens.append(Token(TokenType.UNKNOWN, f'"{literal}', start_line, start_col))
                continue

            # Two-character relational operators
            two_char = ch + self._peek(1)
            if two_char == "==":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.EQ, "==", start_line, start_col))
                continue
            elif two_char == "!=":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.NEQ, "!=", start_line, start_col))
                continue
            elif two_char == "<=":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.LTE, "<=", start_line, start_col))
                continue
            elif two_char == ">=":
                self._advance(); self._advance()
                tokens.append(Token(TokenType.GTE, ">=", start_line, start_col))
                continue

            # Single-character tokens
            single_map = {
                "=": TokenType.ASSIGN,
                "<": TokenType.LT,
                ">": TokenType.GT,
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,
                ":": TokenType.COLON,
                ";": TokenType.SEMICOLON,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
            }

            if ch in single_map:
                tokens.append(Token(single_map[ch], ch, start_line, start_col))
                self._advance()
                continue

            # Unrecognized character handling (does not halt)
            tokens.append(Token(TokenType.UNKNOWN, ch, start_line, start_col))
            self._advance()

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens