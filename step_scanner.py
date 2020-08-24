from JS.token import Token

# Comment, var, if, do, for, while, string with ", string with ', CONST, CONSOLE, CONSTRUCTOR, CONTINUE, function, (, ), *, +, -, /, . "
class Error:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self__value

class Scanner:
    def __init__(self):
        self.token_list = []
        self.error_list = []
        self.aux = ""
        self.state = 0

    def scan(self, data):
        for letter in data:
            if self.state == 0:
                if letter == '/':
                    self.state = 1
                    self.aux += letter
                elif letter == 'v':
                    self.state = 4
                    self.aux += letter
                elif letter == 'i':
                    self.state = 6
                    self.aux += letter
                elif letter == 'd':
                    self.state = 7
                    self.aux += letter
                elif letter == 'f':
                    self.state = 8
                    self.aux += letter
                elif letter == 'w':
                    self.state = 10
                    self.aux += letter
                elif letter == '"':
                    self.state = 14
                    self.aux += letter
                elif letter == '\'':
                    self.state = 15
                    self.aux += letter
                elif letter == 'c':
                    self.state = 16
                    self.aux += letter
                elif letter == 'M':
                    self.state = 37
                    self.aux += letter
                elif letter == '"':
                    self.aux += letter
                    self.set_token('QUOTE', self.aux)
                elif letter == '.':
                    self.aux += letter
                    self.set_token('DOT', self.aux)
                elif letter == '+':
                    self.aux += letter
                    self.set_token('OPERAND_SUM', self.aux)
                elif letter == '-':
                    self.aux += letter
                    self.set_token('OPERAND_SUBS', self.aux)
                elif letter == '*':
                    self.aux += letter
                    self.set_token('OPERAND_MULT', self.aux)
                elif letter == '/':
                    self.aux += letter
                    self.set_token('OPERAND_DIV', self.aux)
                elif letter == '(':
                    self.aux += letter
                    self.set_token('LEFT_PARENT', self.aux)
                elif letter == ')':
                    self.aux += letter
                    self.set_token('RIGH_PARENT', self.aux)
                elif letter == '=':
                    self.aux += letter
                    self.set_token('EQUAL_OPERAND', self.aux)




            elif self.state == 1:
                if letter == '*':
                    self.state = 2
                    self.aux += letter


            elif self.state == 2:
                if letter == '*':
                    self.state = 3
                    self.aux += letter
                else:
                    self.aux += letter


            elif self.state == 3:
                if letter == '/':
                    self.aux += letter
                    self.set_token('COMMENT', self.aux)
                elif letter != '/':
                    self.aux += letter
                    self.state = 2
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 4:
                if letter == 'a':
                    self.aux += letter
                    self.state = 5
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 5:
                if letter == 'r':
                    self.aux += letter
                    self.set_token('RESERVED_VAR', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 6:
                if letter == 'f':
                    self.aux += letter
                    self.set_token('RESERVED_IF', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 7:
                if letter == 'o':
                    self.aux += letter
                    self.set_token('RESERVED_DO', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 8:
                if letter == 'o':
                    self.aux += letter
                    self.state = 9
                elif letter == 'u':
                    self.aux += letter
                    self.state = 31
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 9:
                if letter == 'r':
                    self.aux += letter
                    self.set_token('RESERVED_FOR', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 10:
                if letter == 'h':
                    self.aux += letter
                    self.state = 11
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 11:
                if letter == 'i':
                    self.aux += letter
                    self.state = 12
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 12:
                if letter == 'l':
                    self.aux += letter
                    self.state = 13
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 13:
                if letter == 'e':
                    self.aux += letter
                    self.set_token('RESERVED_WHILE', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 14:
                if letter == '"':
                    self.aux += letter
                    self.set_token('STRING', self.aux)
                else:
                    self.aux += letter

            elif self.state == 15:
                if letter == '\'':
                    self.aux += letter
                    self.set_token('STRING', self.aux)
                else:
                    self.aux += letter


            elif self.state == 16: # CONST, CONSOLE, CONSTRUCTOR, CONTINUE
                if letter == 'o':
                    self.aux += letter
                    self.state = 17
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 17:
                if letter == 'n':
                    self.aux += letter
                    self.state = 18
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 18:
                if letter == 's':
                    self.aux += letter
                    self.state = 19
                elif letter == 't':
                    self.aux += letter
                    self.state = 27
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 19:
                if letter == 'o':
                    self.aux += letter
                    self.state = 20
                elif letter == 't':
                    self.aux += letter
                    self.state = 22
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 20:
                if letter == 'l':
                    self.aux += letter
                    self.state = 21
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 21:
                if letter == 'e':
                    self.aux += letter
                    self.set_token('RESERVED_CONSOLE', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 22:
                if letter == 'r':
                    self.aux += letter
                    self.state = 23
                else:
                    self.set_token('RESERVED_CONST',self.aux)

            elif self.state == 23:
                if letter == 'u':
                    self.aux += letter
                    self.state = 24
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 24:
                if letter == 'c':
                    self.aux += letter
                    self.state = 25
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 24:
                if letter == 't':
                    self.aux += letter
                    self.state = 25
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 25:
                if letter == 'o':
                    self.aux += letter
                    self.state = 26
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 26:
                if letter == 'r':
                    self.aux += letter
                    self.set_token('RESERVED_CONSTRUCTOR', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 27:
                if letter == 'i':
                    self.aux += letter
                    self.state = 28
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 28:
                if letter == 'n':
                    self.aux += letter
                    self.state = 29
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 29:
                if letter == 'u':
                    self.aux += letter
                    self.state = 30
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 30:
                if letter == 'e':
                    self.aux += letter
                    self.set_token('RESERVED_CONTINUE', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 31:
                if letter == 'n':
                    self.aux += letter
                    self.state = 32
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 32:
                if letter == 'c':
                    self.aux += letter
                    self.state = 33
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 33:
                if letter == 't':
                    self.aux += letter
                    self.state = 34
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 34:
                if letter == 'i':
                    self.aux += letter
                    self.state = 35
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 35:
                if letter == 'o':
                    self.aux += letter
                    self.state = 36
                else:
                    self.aux += letter
                    self.set_error(self.aux)


            elif self.state == 36:
                if letter == 'n':
                    self.aux += letter
                    self.set_token('RESERVED_FUNCTION', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 37:
                if letter == 'a':
                    self.aux += letter
                    self.state = 38
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 38:
                if letter == 'i':
                    self.aux += letter
                    self.state = 39
                else:
                    self.aux += letter
                    self.set_error(self.aux)

            elif self.state == 39:
                if letter == 'n':
                    self.aux += letter
                    self.set_token('RESERVED_MAIN', self.aux)
                else:
                    self.aux += letter
                    self.set_error(self.aux)



    def set_token(self, token_type, value):
        self.aux = ""
        new_token = Token(token_type,value, 0 ,0)
        self.token_list.append(new_token)
        self.state = 0

    def set_error(self, value):
        self.aux = ""
        print(value, 'does not belong to language!')
        new_error = Error(value)
        self.error_list.append(new_error)
        self.state = 0


