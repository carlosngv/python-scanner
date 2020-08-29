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

    def scan(self,data):
        input = data.splitlines()
        data = list(data)
       # print(data)
        for line in input:
            line = list(line)
            for char in line:
               # print(char)
                if self.state == 0:
                    if char == '<':
                        self.set_token('LESS_THAN', char)
                        self.state = 0
                    elif char == '>':
                        self.set_token('GREATER_THAN', char)
                        self.state = 0
                    elif char == '=':
                        self.set_token('EQUAL', char)
                        self.state = 0
                    elif char == '/':
                        self.set_token('SLASH', char)
                        self.state = 0
                    # HTML, HEADER and tittles
                    elif char == 'h' or char == 'H':
                        self.aux += char
                        self.state = 1
                    # Title, table, th, tr, td, thead, tbody, tfoot
                    elif char == 't' or char == 'T':
                        self.aux += char
                        self.state = 6
                    elif char == 'b' or char == 'B':
                        self.aux += char
                        self.state = 23
                    elif char == 'c' or char == 'C':
                        self.aux += char
                        self.state = 26
                    elif char == 'p' or char == 'P':
                        self.set_token('P_TAG', char)
                        self.state = 0
                    elif char == 'l' or char == 'L':
                        self.aux += char
                        self.state = 41
                    elif char == 'a' or char == 'A':
                        self.set_token('A_TAG', char)
                        self.state = 0
                    elif char == 'u' or char == 'U':
                        self.aux += char
                        self.state = 45
                    elif char == '"':
                        self.aux += char
                        self.state = 44
                    elif char == ' ' or char == '\n':
                        pass
                    else:
                        self.set_error(char, self.row)

                # HTML, HEADER and tittles
                elif self.state == 1:
                    if re.match('[0-9]', char):
                        self.aux += char
                        self.set_token('TITLE_TAG', self.aux)
                        self.state = 0
                    elif char == 't' or char == 'T':
                        self.aux += char
                        self.state = 2
                    elif char == 'e' or char == 'E':
                        self.aux += char
                        self.state = 4
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                elif self.state == 2:
                    if char == 'm' or char == 'M':
                        self.aux += char
                        self.state = 3
                    else:
                        self.set_token('ID', self.aux)

                elif self.state == 3:
                    if char == 'l' or char == 'L':
                        self.aux += char
                        self.set_token('HTML_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                elif self.state == 4:
                    if char == 'a' or char == 'A':
                        self.aux += char
                        self.state = 5
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                elif self.state == 5:
                    if char == 'd' or char == 'D':
                        self.aux += char
                        self.set_token('HEAD_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                # -Title, -table, -th, -tr, -td, -thead, -tbody, -tfoot
                elif self.state == 6:
                    if char == 'i' or char == 'I':
                        self.aux += char
                        self.state = 7
                    elif char == 'r' or char == 'R':
                        self.aux += char
                        self.set_token('TR_TAG', self.aux)
                    elif char == 'd' or char == 'D':
                        self.aux += char
                        self.set_token('TD_TAG', self.aux)
                    elif char == 'h' or char == 'H':
                        self.aux += char
                        self.state = 10
                    elif char == 'b' or char == 'B':
                        self.aux += char
                        self.state = 13
                    elif char == 'f' or char == 'F':
                        self.aux += char
                        self.state = 16
                    elif char == 'a' or char == 'A':
                        self.aux += char
                        self.state = 19
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                elif self.state == 7:
                    if char == 't' or char == 'T':
                        self.aux += char
                        self.state = 8
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                elif self.state == 8:
                    if char == 'l' or char == 'L':
                        self.aux += char
                        self.state = 9
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

                elif self.state == 9:
                    if char == 'e' or char == 'E':
                        self.aux += char
                        self.set_token('TITLE_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 10:

                    if char == 'e' or char == 'E':
                        self.aux += char
                        self.state = 11
                    elif self.aux == 'th':
                        self.set_token('TH_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 11:
                    if char == 'a' or char == 'A':
                        self.aux += char
                        self.state = 12
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 12:
                    if char == 'd' or char == 'D':
                        self.aux += char
                        self.set_token('THEAD_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 13:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 14
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 14:
                    if char == 'd' or char == 'D':
                        self.aux += char
                        self.state = 15
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 15:
                    if char == 'y' or char == 'Y':
                        self.aux += char
                        self.set_token('TBODY_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 16:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 17
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 17:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 18
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 18:
                    if char == 't' or char == 'T':
                        self.aux += char
                        self.set_token('TFOOT_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 19:
                    if char == 'b' or char == 'B':
                        self.aux += char
                        self.state = 20
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 20:
                    if char == 'l' or char == 'L':
                        self.aux += char
                        self.state = 22
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 22:
                    if char == 'e' or char == 'E':
                        self.aux += char
                        self.set_token('TABLE_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                # BODY
                elif self.state == 23:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 24
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 24:
                    if char == 'd' or char == 'D':
                        self.aux += char
                        self.state = 25
                    elif char == 'r' or char == 'R':
                        self.aux += char
                        self.state = 33
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 25:
                    if char == 'y' or char == 'Y':
                        self.aux += char
                        self.set_token('BODY_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                # CAPTION, COLGROUP, COL
                elif self.state == 26:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 27
                    elif char == 'a' or char == 'A':
                        self.aux += char
                        self.state = 36
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 27:
                    if char == 'l' or char == 'L':
                        self.aux += char
                        self.state = 28
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 28:
                    if char == 'g' or char == 'G':
                        self.aux += char
                        self.state = 29
                    elif self.aux == 'col' or 'COL':
                        self.set_token('COL_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 29:
                    if char == 'r' or char == 'R':
                        self.aux += char
                        self.state = 30
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 30:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 31
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 31:
                    if char == 'u' or char == 'U':
                        self.aux += char
                        self.state = 32
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 32:
                    if char == 'p' or char == 'P':
                        self.aux += char
                        self.set_token('COLGROUP_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 33:
                    if char == 'd' or char == 'D':
                        self.aux += char
                        self.state = 34
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 34:
                    if char == 'e' or char == 'E':
                        self.aux += char
                        self.state = 35
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 35:
                    if char == 'r' or char == 'R':
                        self.aux += char
                        self.set_token('RESERVED_BORDER', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 36:
                    if char == 'p' or char == 'P':
                        self.aux += char
                        self.state = 37
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 37:
                    if char == 't' or char == 'T':
                        self.aux += char
                        self.state = 38
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 38:
                    if char == 'i' or char == 'i':
                        self.aux += char
                        self.state = 39
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 39:
                    if char == 'o' or char == 'O':
                        self.aux += char
                        self.state = 40
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 40:
                    if char == 'n' or char == 'N':
                        self.aux += char
                        self.set_token('CAPTION_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 41:
                    if char == 'i' or char == 'I':
                        self.aux += char
                        self.set_token('LI_TAG',self.aux)
                    elif char == 'a' or char == 'A':
                        self.aux += char
                        self.state = 42
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 42:
                    if char == 'n' or char == 'N':
                        self.aux += char
                        self.state = 43
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                elif self.state == 43:
                    if char == 'g' or char == 'G':
                        self.aux += char
                        self.set_token('RESERVED_LANG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)
                # STRING
                elif self.state == 44:
                    if char != '"':
                        self.aux += char
                        self.state = 44
                    elif char == '"':
                        self.aux += char
                        self.set_token('STRING', self.aux)
                # UL
                elif self.state == 45:
                    if char == 'L' or char == 'l':
                        self.aux += char
                        self.set_token('UL_TAG', self.aux)
                    else:
                        self.aux += char
                        self.set_token('ID', self.aux)

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
        self.aux = ""
        new_error = Error(value, "La entrada \"" + value + "\" en la fila " + str(row) + " no pertenece al lenguaje.")
        self.error_list.append(new_error)