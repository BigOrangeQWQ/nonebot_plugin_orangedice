"""
写的很不好，欢迎PR
参考BLOG:https://ruslanspivak.com/lsbasi-part1/
"""

from enum import Enum
from random import randint
from typing import Any, Optional, Union


class TokenType(Enum):
    """符号表枚举类"""
    NUMBER = 'NUMBER' #123456789
    PLUS = 'PLUS' # +
    MINUS = 'MINUS' # -
    MUL = 'MUL' # *
    DIV = 'DIV' # /
    LPAREN = 'LPAREN' # (
    RPAREN = 'RPAREN' # )
    DICE = 'DICE' # d
    DICE_POOL = 'DICE_POOL' #骰子池 a
    DICE_LEVEL = 'DICE_LEVEL' #选取线 k/q
    DICE_GIVE = 'DICE_GIVE' #奖惩 p/b
    EOF = 'EOF'
    

class Token:
    """令牌"""
    def __init__(self, type: TokenType, value: Any) -> None:
        self.value = value
        self.type = type

class Lexer:
    """词法解析"""
    
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.loc: int = 0
        self.cache: Optional[str] = self.text[self.loc]
    
    def _advance(self):
        """
        前进并解析下一个token
        """
        self.loc+=1 #前进一步
        # self.cache = self.text[self.loc]
        if self.loc > len(self.text) - 1:
            self.cache = None 
        else:
            self.cache = self.text[self.loc]

    def _skip_whitespace(self):
        """
        跳过空格
        """
        while self.cache is not None and self.cache.isspace():
            self._advance()
        
    def _integer(self):
        """
        解析Int/Float并返回
        """
        result = ''
        while self.cache is not None and self.cache.isdigit():
            result += self.cache
            self._advance()
        return int(result)

    def get_next(self) -> Token:
        """
        解析各类运算符
        """
        while self.cache is not None:
            if self.cache.isspace():
                self._skip_whitespace()
                continue
            if self.cache.isdigit():
                return Token(TokenType.NUMBER, self._integer())
            if self.cache == '+':
                self._advance()
                return Token(TokenType.PLUS, '+')
            if self.cache == '-':
                self._advance()
                return Token(TokenType.MINUS, '-')
            if self.cache == '*' or self.cache == 'x':
                self._advance()
                return Token(TokenType.MUL,'*')
            if self.cache == '/':
                self._advance()
                return Token(TokenType.DIV, '/')
            if self.cache == 'd':
                self._advance()
                return Token(TokenType.DICE, 'd')
            if self.cache == 'k':
                self._advance()
                return Token(TokenType.DICE_LEVEL, 'k')
            if self.cache == 'q':
                self._advance()
                return Token(TokenType.DICE_LEVEL, 'q')
            if self.cache == 'a':
                self._advance()
                return Token(TokenType.DICE_POOL, 'a')
            if self.cache == 'p':
                self._advance()
                return Token(TokenType.DICE_GIVE, 'p')
            if self.cache == 'b':
                self._advance()
                return Token(TokenType.DICE_GIVE, 'b')
            if self.cache == '(':
                self._advance()
                return Token(TokenType.LPAREN, '(')
            if self.cache == ')':
                self._advance()
                return Token(TokenType.RPAREN, ')')
            raise Exception(f"no this key-word: {self.cache}")
        return Token(TokenType.EOF,None)
        
class Parser:
    """语法解析"""
    def __init__(self, tokens: Lexer):
        self.tokens = tokens
        self.next_token: Token = Token(TokenType.EOF, None)
        self.token: Token = Token(TokenType.EOF, None)
        self._advance()#初始化next token/token
        
    def _advance(self):
        """获得下一个令牌"""
        self.token = self.next_token
        self.next_token = self.tokens.get_next()
        
    def _accept(self, type: TokenType) -> bool:
        """
        是否接收到指定类型的令牌
        接收到指定令牌，令牌前进一步
        """
        if self.next_token and self.next_token.type == type:
            self._advance() #前进一步
            return True
        else:
            return False
        
    def _expect(self, type: TokenType):
        """
        下一个令牌为某Type
        若不为则丢出SyntaxError报错
        """
        if not self._accept(type):
            raise SyntaxError(f'Expected {type.name}')
        
    def _random(self, start: int = 1, end: int =100):
        """随机数"""
        return randint(start,end)
        
    def expr(self) -> Union[int,float]:
        """expr ::= expr | expr '+' term  | expr '-' term  | term"""
        left = self.term() #左值
        while self._accept(TokenType.PLUS) or self._accept(TokenType.MINUS):
            op = self.token.type #获取运算 符
            right = self.term() #获取右值
            if op == TokenType.PLUS:
                left += right 
            elif op == TokenType.MINUS:
                left -= right 
        return left
    
    def term(self) -> Union[int,float]:
        """term ::= term | term '*' dice| term 'x' dice | term '/' dice | dice"""
        left = self.dice() #左值
        while self._accept(TokenType.MUL) or self._accept(TokenType.DIV):
            op = self.token.type #获取运算 符
            right = self.dice() #获取右值
            if op == TokenType.MUL:
                left *= right 
            elif op == TokenType.DIV:
                left /= right 
        return left
    
    def dice(self) -> Union[int,float]:
        """
        dice ::=  dice 'd' atom ['k'|'q'] atom ['p'|'b'] atom ['a'] atom | atom
        """
        left = result = self.atom()
        while self._accept(TokenType.DICE):
            right = self.atom()
            _cache = [self._random(1,int(right)) for i in range(0,int(left))] #储存骰子结果
            result = 0
            #选取线 k大 q小
            if self._accept(TokenType.DICE_LEVEL):
                arg = int(self.atom())
                if self.token.value == 'k':
                    _cache.sort(reverse=True)
                if self.token.value == 'p':
                    _cache.sort()
                for i in range(0,arg):
                    result += _cache[i]
            #奖惩骰 p b
            if self._accept(TokenType.DICE_GIVE):
                arg = int(self.atom())
                _cache = [self._random(1,100) % 10]
                _cache_list = [self._random(1,10) for i in range(0,arg)]
                if self.token.value == 'p':
                    _cache_list.sort(reverse=True)
                if self.token.value == 'b':
                    _cache_list.sort()
                return int(f'{_cache_list[0]}{_cache}')
            #骰池 a
            if self._accept(TokenType.DICE_POOL):
                arg = int(self.atom())
                for i in _cache:
                    if (i > arg):
                        result+=1
                return result
            return sum(_cache)
        return result
    
    def atom(self) -> Union[float,int]:
        """
        atom ::= digit | ('+'|"-") atom | '(' expr ')'
        """
        if self._accept(TokenType.NUMBER):
            return self.token.value
        elif self._accept(TokenType.LPAREN):
            exprval = self.expr()
            self._expect(TokenType.RPAREN)
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')
        
    def parse(self):
        return self.expr()

# ——TEST——
# args = [
#         '2.2+3',
#         '2+3*44.6',
#         '2+(3+4)*2',
#         '(((1)))',
#         '1d5',
#         '1d100a25',
#         '3d100k3'
#         ]
# for i in args:
#     parser = Parser(Lexer(i))
#     print(parser.parse())