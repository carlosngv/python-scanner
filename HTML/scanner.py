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
        self.aux = ''
        self.state = 0
        self.row = 1
        self. column = 0
        self.dataAux = ''
        self.route = ''
        self.reserved = [
            'HTML', 'html', 'form', 'method', 'METHOD', 'p', 'DOCUMENT', 'DOCTYPE', 'meta', 'title', 'script','body'
            , 'head', 'td', 'ul', 'th', 'tr', 'table', 'label', 'input','br', 'type', 'id', 'action', 'onsubmit', 'h1',
            'h2', 'h3', 'h4','h5','h6', 'colgroup', 'img', 'li','caption', 'col', 'thead', 'tbody', 'tfoot', 'footer',
            'lang', 'src', 'a','!DOCTYPE', 'charset', 'img'

        ]

    def scan(self,data):
        input = data.splitlines()
        self.dataAux = data
        data = list(data)
        for line in input:
            lineAux = line
            if re.match('<!DOCTYPE HTML>', line):
                self.set_token('LESS_THAN','<')
                self.set_token('RESERVED_!DOCTYPE','!DOCTYPE')
                self.set_token('RESERVED_HTML','HTML')
                self.set_token('GREATER_THAN','>')
                continue

            if re.findall('PATHL:', lineAux):
                lineAux = lineAux.replace(' ', '')
                lineAux = lineAux.replace('<!--', '')
                lineAux = lineAux.replace('-->', '')
                lineAux = lineAux.replace('PATHL:', '')
                self.route = lineAux


            line = list(line)
            for char in line:
                if self.state == 0:

                    if char == '>':
                        self.set_token('GREATER_THAN', char)
                        self.state = 57
                    elif char == '=':
                        self.set_token('EQUAL', char)
                        self.state = 0
                    elif char == '/':
                        self.set_token('SLASH', char)
                        self.state = 0
                    elif char == '-':
                        self.set_token('HYPHEN', char)
                    elif char == '!':
                        self.set_token('EXCL_SYMB', char)
                        self.state = 0
                    elif char == '<':
                        self.aux += char
                        self.state = 1
                    elif char.isalpha():
                        self.aux += char
                        self.state = 62
                    elif char.isdigit():
                        self.aux += char
                        self.state = 63
                    # HTML, HEADER and tittles
                    elif char == '"':
                        self.aux += char
                        self.state = 44
                    elif char == ' ' or char == '\n':
                        pass
                    else:
                        self.set_error(char, self.row)
                # Comment
                elif self.state == 1:
                    if char == '!':
                        self.aux += char
                        self.state = 2
                    else:
                        self.set_token('LESS_THAN', self.aux)
                        if char.isalpha():
                            self.aux += char
                            self.state = 62
                elif self.state == 2:
                    if char == '-':
                        self.aux += char
                        self.state = 3
                    else:
                        self.set_token('ID', self.aux)
                elif self.state == 3:
                    if char == '-':
                        self.aux += char
                        self.state = 4
                    else:
                        self.set_token('ID', self.aux)
                elif self.state == 4:
                    if char == '>':
                        self.aux += char
                        print(self.aux)
                        self.aux = self.aux.replace('<','')
                        self.set_token('COMMENT', self.aux)
                    else:
                        self.aux += char
                        self.state = 4
                        # STRING
                elif self.state == 44:
                    if char != '"':
                        self.aux += char
                        self.state = 44
                    elif char == '"':
                        self.aux += char
                        self.set_token('STRING', self.aux)

                # TEXT BETWEEN > example <
                elif self.state == 57:
                    if char != '<':
                        if char == '\n':
                            pass
                        else:
                            self.aux += char
                        self.state = 57
                    elif char == '<':
                        if not re.match('(^$| +)', self.aux):
                            self.set_token('TEXT', self.aux)
                        self.set_token('LESS_THAN', char)
                        self.state = 1
                elif self.state == 62:
                    if char.isdigit():
                        self.aux += char
                        self.state = 62
                    elif not char.isalpha():
                        self.set_token(self.reservedToken(self.aux), self.aux)
                        if char == '>':
                            self.set_token('GREATER_THAN', char)
                            self.state = 57
                    else:
                        self.aux += char
                        self.state = 62
                elif self.state == 63:
                    if not char.isdigit():
                        self.set_token('NUMBER', self.aux)
                        if char == '>':
                            self.set_token('GREATER_THAN', char)
                            self.state = 57
                    else:
                        self.aux += char
                        self.state = 63
            self.row += 1
            self.column = 0

    def reservedToken(self, word):
        for item in self.reserved:
            if word == item:
                return 'RESERVED_' + item.upper()
        return 'ID'

    def set_token(self, token_type, value):
        if len(value) == 0:
            return
        self.column += 1
        self.state = 0
        self.aux = ''
        new_token = Token(token_type,value,self.row ,self.column)
        self.token_list.append(new_token)

    def set_error(self, value,row):
        self.dataAux = self.dataAux.replace(value, '')
        self.aux = ""
        new_error = Error(value, "La entrada \"" + value + "\" en la fila " + str(row) + " no pertenece al lenguaje.")
        self.error_list.append(new_error)