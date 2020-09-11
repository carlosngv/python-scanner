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
class Transition:
    def __init__(self, value, state):
        self.__value = value
        self.__state = state

    def get_value(self):
        return self.__value

    def get_state(self):
        return self.__state

class Scanner:
    def __init__(self):
        self.transitions_list = []
        self.token_list = []
        self.error_list = []
        self.aux = ''
        self.dataAux = ''
        self.state = 0
        self.row = 1
        self. column = 0
        self.reserved = ['color', 'border', 'background-color', 'Opacity', 'font-family', ' font-size', 'padding-right',
                         'padding width', 'margin-right', 'margin position', 'right', 'clear', 'max-height',
                         'background-image', 'url', 'width'
                         'background', 'font-style', 'font', 'padding-bottom', 'display', 'height', 'margin-bottom',
                         'border-style',
                         'bottom', 'left', 'max-width', 'min-height', 'text-align', 'font-weight', 'padding-left',
                         'padding-top', 'font-size', 'sans-serif', 'img'
                         'line-height', 'margin-top', 'margin-left', 'display', 'top', 'float', 'min-width', 'content',
                         'rgba', 'px', 'em', 'vh', 'vw', 'in', 'cm', 'mm', 'pt', 'pc', 'rem']

    def scan(self,data):

        hex_regp = '[#]([a-fA-F]|[0-9]){6}'

        input = data.splitlines()
        self.dataAux = data
        data = list(data)
        for line in input:
            line = list(line)
            for char in line:
                if self.state == 0:
                    if char == '"':
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 3
                    elif char == "'":
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 4
                    elif char == '/':
                        self.state = 1
                        self.set_transition(self.aux, self.state)
                        self.aux += char
                    elif char.isalpha():
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 5
                    elif char == ' ' or char == '\t':
                        pass
                    elif char.isdigit():
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 6
                    elif char == '%' :
                        self.set_token('PERCENTAGE_SIGN', char)
                    elif char == '#':
                        self.set_token('HASHTAG_SYMB', char)
                    elif char == '+':
                        self.set_token('ADD_OPT', char)
                    elif char == '*':
                        self.set_token('ASTERISK', char)
                    elif char == '-':
                        self.set_token('SUBS_OPT', char)
                    elif char == ':':
                        self.set_token('COLON', char)
                    elif char == ';':
                        self.set_token('SEMICOLON', char)
                    elif char == '=':
                        self.set_token('EQUAL_OPT', char)
                    elif char == '{':
                        self.set_token('LEFT_BRACE', char)
                    elif char == '}':
                        self.set_token('RIGHT_BRACE', char)
                    elif char == ')':
                        self.set_token('RIGHT_PARENT', char)
                    elif char == '(':
                        self.set_token('LEFT_PARENT', char)
                    elif char == '.':
                        self.set_token('DOT', char)
                    elif char == '>':
                        self.set_token('GREATER_THAN', char)
                    elif char == '<':
                        self.set_token('LESS_THAN', char)

                    else:
                        self.set_error(char, self.row)
                        new_transition = Transition('**** ERROR ' + char + ' *****', 0)

                        self.transitions_list.append(new_transition)
                elif self.state == 1:
                    if char == '*':
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 2
                    elif char == '/':
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 4
                        comment_found = True
                    else:
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.set_token('SLASH', self.aux)
                elif self.state == 2:
                    if char == '*':
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 2
                    elif char == '/' and self.aux.endswith("*"):
                        self.aux += char

                        self.set_token('COMMENT', self.aux)
                        new_transition = Transition('Input ' + self.aux + ' accepted', 2)
                        self.transitions_list.append(new_transition)
                    else:
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 2
                elif self.state == 3:
                    if not char == '"':
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 3
                    else:
                        self.aux += char
                        self.set_token('STRING', self.aux)
                        new_transition = Transition('Input ' + self.aux + ' accepted', 3)
                        self.transitions_list.append(new_transition)
                elif self.state == 4:
                    if not char == "'":
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 4
                    else:
                        self.aux += char
                        self.set_token('STRING', self.aux)
                elif self.state == 5:
                    if char.isalpha():
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 5
                    elif char == '-':
                        self.aux += char
                        self.set_transition(self.aux, self.state)
                        self.state = 5
                    elif char == '#':
                        self.set_transition(self.aux, self.state)
                        self.token_list.append(Token('ID', self.aux, self.row, self.column))
                        self.aux = ''
                        self.set_transition('#', self.state)
                        new_token = Token('HASHTAG_SYMB',char,self.row ,self.column)
                        self.token_list.append(new_token)
                        self.state = 5
                    else:
                        if char.isdigit():
                            self.aux += char
                            self.state = 5
                        self.set_token(self.reservedToken(self.aux), self.aux)
                        new_transition = Transition('Input ' + self.aux + ' accepted', 6)
                        self.transitions_list.append(new_transition)
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '.':
                            self.set_token('DOT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == ':':
                            self.set_token('COLON', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '.':
                            self.set_token('DOT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == ',':
                            self.set_token('COMMA', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '*':
                            self.set_token('ASTERISK', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char == '>':
                            self.set_token('GREATER_THAN', char)
                        elif char == '<':
                            self.set_token('LESS_THAN', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        elif char.isdigit():
                            self.aux += char
                            self.state = 5
                            self.set_transition(self.aux, self.state)
                        elif char == ' ' or char == '\t':
                            pass
                        elif char == '=':
                            self.set_token('EQUAL_OPT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 5)
                            self.transitions_list.append(new_transition)
                        else:
                            new_transition = Transition('**** ERROR ' + char + ' *****', 5)
                            self.transitions_list.append(new_transition)
                            self.set_error(char, self.row)
                elif self.state == 6:
                    if not char.isdigit():
                        self.set_token("NUMBER", self.aux)
                        new_transition = Transition('Input ' + self.aux + ' accepted', 6)
                        self.transitions_list.append(new_transition)
                        if char == ')':
                            self.set_token('RIGHT_PARENT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == '(':
                            self.set_token('LEFT_PARENT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == ';':
                            self.set_token('SEMICOLON', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == '.':
                            self.set_token('DOT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == ':':
                            self.set_token('COLON', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == '{':
                            self.set_token('LEFT_BRACE', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == '}':
                            self.set_token('RIGHT_BRACE', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == '.':
                            self.set_token('DOT', char)
                            new_transition = Transition('Input ' + char + ' accepted', 6)
                            self.transitions_list.append(new_transition)
                        elif char == ',':
                            self.set_token('COMMA', char)
                            new_transition = Transition('Input accepted ' + char, 6)
                            self.transitions_list.append(new_transition)
                        elif char == '%':
                            self.set_token('PERCENTAGE_SIGN', char)
                            new_transition = Transition('Input accepted ' + char, 6)
                            self.transitions_list.append(new_transition)
                        elif char == '*':
                            self.set_token('ASTERISK', char)
                            new_transition = Transition('Input accepted ' + char, 6)
                            self.transitions_list.append(new_transition)
                        elif char.isalpha():
                            self.state = 0
                            self.aux += char
                            self.set_transition(self.aux, self.state)
                        else:
                            self.aux += char

                    else:
                        self.state = 6
                        self.aux += char
                        self.set_transition(self.aux, self.state)
            self.row += 1
            self.column = 0

    def set_token(self, token_type, value):
        self.column += 1
        self.state = 0
        self.aux = ''
        new_token = Token(token_type,value,self.row ,self.column)
        if new_token not in self.token_list:
            self.token_list.append(new_token)

        else:
            print('Token is already in.')

    def set_error(self, value,row):
        self.dataAux = self.dataAux.replace(value, '')
        self.aux = ""
        new_error = Error(value, "La entrada \"" + value + "\" en la fila " + str(row) + " no pertenece al lenguaje.")
        self.error_list.append(new_error)

    def reservedToken(self, word):
        for item in self.reserved:
            if word == item:
                return 'RESERVED_' + item.upper()
        return 'ID'

    def set_transition(self, value, state):
        new_transition = Transition(value, state)
        self.transitions_list.append(new_transition)

