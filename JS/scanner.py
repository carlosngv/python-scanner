import re
from HTML.token import Token
class Error:
    def __init__(self, value, message):
        self.__value = value
        self.message = message

    def get_value(self):
        return self.__value

    def get_message(self):
        return self.message

class Scanner:
    def __init__(self):
        self.token_list = []
        self.error_list = []
        self.reserved = [
            'function', 'return', 'while', 'for', 'document', 'getElementById', 'if', 'else', 'constructor', 'console', 'log',
            'break', 'true', 'false', 'value', 'new', 'Object', 'push', 'Array', 'appendChild', 'setAttribute',
            'innerHTML', 'innerText', 'element', 'createElement', 'JSON', 'Items', 'stringify', 'clear', 'fromHTML', 'forEach',
            'location', 'href', 'sessionStorage', 'getItem', 'null', 'this', 'Math', 'pow', 'class', 'save', 'ajax', 'parseInt',
            'instanceof', 'default', 'break', 'debugger', 'in', 'void','typeof','try','switch', 'throw', 'catch', 'finally'
        ]
        self.aux = ''
        self.state = 0
        self.row = 1
        self. column = 0
        self.dataAux = ''
        self.route = ''

    def scan(self,data):

        #Validations
        comment_found = False
        self.dataAux = data
        input = data.splitlines()
        data = list(data)
        for line in input:
            lineAux = line
            if re.findall('PATHL:', line):
                lineAux = lineAux.replace(' ','')
                lineAux = lineAux.replace('//','')
                lineAux = lineAux.replace('PATHL:','')
                self.route = lineAux
                print(lineAux)
                continue
            line = list(line)
            if comment_found == True:
                self.set_token('COMMENT', self.aux)
                comment_found = False
            for char in line:
                if self.state == 0:
                    if char == '"':
                        self.aux += char
                        self.state = 12
                    elif char == "'":
                        self.aux += char
                        self.state = 13
                    elif char == '/':
                        self.state = 1
                        self.aux += char
                    elif char == ' ':
                        pass
                    elif char == '\t':
                        pass
                    elif char.isdigit():
                        self.aux += char
                        self.state = 11
                    elif char == 'ç':
                        self.set_error(char, self.row)
                    elif char.isalpha():
                        self.aux += char
                        self.state = 5
                    elif char == '(':
                        self.set_token('LEFT_PARENT', char)
                    elif char == ')':
                        self.set_token('RIGHT_PARENT', char)
                    elif char == ';':
                        self.set_token('SEMICOLON', char)
                    elif char == '.':
                        self.set_token('DOT', char)
                    elif char == ':':
                        self.set_token('COLON', char)
                    elif char == '{':
                        self.set_token('LEFT_BRACE', char)
                    elif char == '}':
                        self.set_token('RIGHT_BRACE', char)
                    elif char == ',':
                        self.set_token('COMMA', char)
                    elif char == '*':
                        self.set_token('MULT_OPT', char)
                    elif char == '<':
                        self.aux += char
                        self.state = 9
                    elif char == '>':
                        self.aux += char
                        self.state = 10
                    elif char == '+':
                        self.aux += char
                        self.state = 6
                    elif char == '-':
                        self.aux += char
                        self.state = 7
                    elif char == '=':
                        self.aux += char
                        self.state = 8
                    elif char == '&':
                        self.aux += char
                        self.state = 14

                    else:
                        self.set_error(char, self.row)
                elif self.state == 1:
                    if char == '*':
                        self.aux += char
                        self.state = 2
                    elif char == '/':
                        self.aux += char
                        self.state = 4
                        comment_found = True
                    else:
                        self.set_token('DIV_OPT', self.aux)
                        if char.isdigit():
                            self.state = 11
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                        elif char == '.':
                            self.set_token('DOT', char)
                        elif char == ':':
                            self.set_token('COLON', char)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                        elif char == ',':
                            self.set_token('COMMA', char)
                        elif char == '=':
                            self.set_token('EQUAL_OPT', char)
                        elif char == '<':
                            self.set_token('LESS_THAN', char)
                        elif char == '>':
                            self.set_token('GREATER_THAN', char)
                        elif char == '*':
                            self.set_token('MULT_OPT', char)
                        elif char == '+':
                            self.set_token('ADD_OPT', char)
                        elif char == '-':
                            self.set_token('SUBS_OPT', char)
                        elif char == '/':
                            self.set_token('DIV_OPT', char)
                        elif char.isalpha():
                            self.aux += char
                            self.state = 5
                elif self.state == 2:
                    if char == '*':
                        self.aux += char
                        self.state = 2
                    elif char == '/' and self.aux.endswith("*"):
                        self.aux += char
                        self.set_token('COMMENT', self.aux)
                    else:
                        self.aux += char
                        self.state = 2
                elif self.state == 3:
                    if char == '/':
                        self.aux += char
                        self.set_token('COMMENT', self.aux)
                    else:
                        self.aux += char
                        self.state = 2
                elif self.state == 4:
                    self.aux += char
                    self.state = 4

                elif self.state == 5:
                    if not char.isalpha():
                        self.set_token(self.reservedToken(self.aux), self.aux)
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                        elif char == '.':
                            self.set_token('DOT', char)
                        elif char == ':':
                            self.set_token('COLON', char)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                        elif char == ',':
                            self.set_token('COMMA', char)
                        elif char == '=':
                            self.set_token('EQUAL_OPT', char)
                        elif char == '<':
                            self.set_token('LESS_THAN', char)
                        elif char == '>':
                            self.set_token('GREATER_THAN', char)
                        elif char == '*':
                            self.set_token('MULT_OPT', char)
                        elif char == '+':
                            self.set_token('ADD_OPT', char)
                        elif char == '-':
                            self.set_token('SUBS_OPT', char)
                        elif char == '/':
                            self.set_token('DIV_OPT', char)
                    else:
                        self.state = 5
                        self.aux += char
                elif self.state == 6:
                    if char == '+':
                        self.aux += char
                        self.set_token("INCR_OPT", self.aux)
                    else:
                        self.set_token("ADD_OPT", self.aux )
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                        elif char == '.':
                            self.set_token('DOT', char)
                        elif char == ':':
                            self.set_token('COLON', char)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                        elif char == ',':
                            self.set_token('COMMA', char)
                        elif char == '=':
                            self.set_token('EQUAL_OPT', char)
                        elif char == '<':
                            self.set_token('LESS_THAN', char)
                        elif char == '>':
                            self.set_token('GREATER_THAN', char)
                        elif char == '*':
                            self.set_token('MULT_OPT', char)
                        elif char == '+':
                            self.set_token('ADD_OPT', char)
                        elif char == '-':
                            self.set_token('SUBS_OPT', char)
                        elif char == '/':
                            self.set_token('DIV_OPT', char)
                elif self.state == 7:
                    if char == '-':
                        self.aux += char
                        self.set_token("DECR_OPT", self.aux)
                    else:
                        self.set_token("SUBS_OPT", self.aux )
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                        elif char == '.':
                            self.set_token('DOT', char)
                        elif char == ':':
                            self.set_token('COLON', char)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                        elif char == ',':
                            self.set_token('COMMA', char)
                        elif char == '=':
                            self.set_token('EQUAL_OPT', char)
                        elif char == '<':
                            self.set_token('LESS_THAN', char)
                        elif char == '>':
                            self.set_token('GREATER_THAN', char)
                        elif char == '*':
                            self.set_token('MULT_OPT', char)
                        elif char == '+':
                            self.set_token('ADD_OPT', char)
                        elif char == '-':
                            self.set_token('SUBS_OPT', char)
                        elif char == '/':
                            self.set_token('DIV_OPT', char)
                elif self.state == 8:
                    if char == '=':
                        self.aux += char
                        self.set_token("EQUAL_OPT", self.aux)
                    elif char == "'":
                        self.set_token("EQUAL_OPT", self.aux)
                        self.aux += char
                        self.state = 13
                    elif char == '"':
                        self.set_token("EQUAL_OPT", self.aux)
                        self.aux += char
                        self.state = 12
                    elif char.isdigit():
                        self.set_token("EQUAL_OPT", self.aux)
                        self.aux += char
                        self.state = 11
                    else:
                        self.set_token("EQUAL_OPT", self.aux )
                elif self.state == 9:
                    if char == '=':
                        self.aux += char
                        self.set_token("GREATER_THAN", self.aux)
                    else:
                        self.set_token("GREATER_THAN", self.aux )
                elif self.state == 10:
                    if char == '=':
                        self.aux += char
                        self.set_token("LESS_THAN", self.aux)
                    else:
                        self.set_token("LESS_THAN", self.aux )
                elif self.state == 11:
                    if not char.isdigit():
                        self.set_token("NUMBER", self.aux)
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                        elif char == '.':
                            self.set_token('DOT', char)
                        elif char == ':':
                            self.set_token('COLON', char)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                        elif char == '.':
                            self.set_token('DOT', char)
                        elif char == ',':
                            self.set_token('COMMA', char)
                        elif char == '=':
                            self.set_token('EQUAL_OPT', char)
                        elif char == '<':
                            self.set_token('LESS_THAN', char)
                        elif char == '>':
                            self.set_token('GREATER_THAN', char)
                        elif char == '*':
                            self.set_token('MULT_OPT', char)
                        elif char == '+':
                            self.set_token('ADD_OPT', char)
                        elif char == '-':
                            self.set_token('SUBS_OPT', char)
                        elif char == '/':
                            self.set_token('DIV_OPT', char)
                    else:
                        self.state = 11
                        self.aux += char
                elif self.state == 12:
                    if not char == '"':
                        self.aux += char
                        self.state = 12
                    else:
                        self.aux += char
                        self.set_token('STRING', self.aux)
                elif self.state == 13:
                    if not char == "'":
                        self.aux += char
                        self.state = 13
                    else:
                        self.aux += char
                        self.set_token('STRING', self.aux)
                elif self.state == 14:
                    if char == "&":
                        self.aux += char
                        self.set_token("AND_OPT", self.aux)
                    else:
                        self.set_token('AND_OPT', self.aux)

            self.row += 1
            self.column = 0

    def set_token(self, token_type, value):
        self.column += 1
        self.state = 0
        self.aux = ''
        new_token = Token(token_type, value, self.row, self.column)
        if new_token not in self.token_list:
            self.token_list.append(new_token)
        else:
            print('Token is already in.')

    def set_error(self, value, row):
        self.dataAux = self.dataAux.replace(value, '')
        self.aux = ""
        new_error = Error(value, "La entrada \"" + value + "\" en la fila " + str(row) + " no pertenece al lenguaje.")
        self.error_list.append(new_error)

    def reservedToken(self, word):
        for item in self.reserved:
            if word == item:
                return 'RESERVED_' + item.upper()
        return 'ID'