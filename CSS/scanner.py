import re
from CSS.token import Token
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
        self.reserved = ['color', 'border', 'background-color', 'Opacity', 'font-family', ' font-size', 'padding-right',
                    'padding width', 'margin-right', 'margin position', 'right', 'clear', 'max-height',
                    'background-image',
                    'background', 'font-style', 'font', 'padding-bottom', 'display', 'height', 'margin-bottom',
                    'border-style',
                    'bottom', 'left', 'max-width', 'min-height', 'text-align', 'font-weight', 'padding-left',
                    'padding-top',
                    'line-height', 'margin-top', 'margin-left', 'display', 'top', 'float', 'min-width', 'content']
        self.unit_measure = ['px', 'em', 'vh', 'vw', 'in', 'cm', 'mm', 'pt', 'pc']


    def scan(self, data):

        #Validations
        comma_found = False
        string_found = False
        comment_found = False
        color_found = False
        semicolon_found = False
        # Rows and columns
        row = 1
        column = 1
        #Patterns
        id_pattern = '[.][a-zA-Z]([a-zA-Z]|[0-9]|[-]?)*'
        id1_pattern = '[#][a-zA-Z]([a-zA-Z]|[0-9]|[-]?)*'
        id2_pattern = '[a-zA-Z]([a-zA-Z]|[0-9])*[#][a-zA-Z]([a-zA-Z]|[0-9])*'
        id3_pattern = '[a-zA-Z]([a-zA-Z]|[0-9])*[:][a-zA-Z]([a-zA-Z]|[0-9])*'
        id4_pattern = '([a-zA-Z]|[*])?([a-zA-Z]|[0-9])*[:][:][a-zA-Z]([a-zA-Z]|[0-9])*'

        input = data.splitlines()
        for line in input:
            words = line.split()
            for word in words:
                print(word)
                # COMMENT VALIDATION
                # STRING VALIDATION
                if word.endswith('*/') and comment_found == True:
                    self.aux += word + ''
                    comment_found = False
                    self.set_token('COMMENT', self.aux, row, column)
                    continue
                elif comment_found == True:
                    self.aux += word + ' '
                    continue
                elif word.endswith('"') and string_found == True:
                    self.aux += word + ' '
                    self.set_token('STRING', self.aux, row, column)
                    string_found = False
                elif word.endswith(';') and string_found == True:
                    word = word.replace(';','')
                    self.aux += word + ' '
                    self.set_token('STRING', self.aux, row, column)
                    column = column + 1
                    self.set_token('SEMICOLON', ';', row, column)
                    string_found = False
                elif string_found == True:
                    self.aux += word + ''
                    continue
                # COMMENTS
                elif word.startswith('/*'):
                    self.aux += word + ' '
                    comment_found = True
                    continue
                # IDS
                elif re.match(id_pattern, word):
                    if word.endswith(','):
                        word = word.replace(',', '')
                        comma_found = True
                    self.set_token('ID', word, row, column)
                    if comma_found == True:
                        column = column + 1
                        self.set_token('COMMA', ',', row, column)
                        comma_found = False
                    continue
                elif re.match(id2_pattern, word):
                    if word.endswith(','):
                        word = word.replace(',', '')
                        comma_found = True
                    x = re.split('[#]', word)
                    self.set_token('ID', x[0], row, column)
                    column = column + 1
                    self.set_token('HASHTAG', '#', row, column)
                    column = column + 1
                    self.set_token('ID', x[1], row, column)
                    if comma_found == True:
                        column = column + 1
                        self.set_token('COMMA', ',', row, column)
                        comma_found = False
                    continue
                elif re.match(id3_pattern, word):
                    if word.endswith(','):
                        word = word.replace(',', '')
                        comma_found = True
                    x = re.split('[:]', word)
                    self.set_token('ID', x[0], row, column)
                    column = column + 1
                    self.set_token('COLON', ':', row, column)
                    column = column + 1
                    self.set_token('ID', x[1], row, column)
                    if comma_found == True:
                        column = column + 1
                        self.set_token('COMMA', ',', row, column)
                        comma_found = False
                    continue
                elif re.match(id4_pattern, word):
                    if word.endswith(','):
                        word = word.replace(',', '')
                        comma_found = True
                    x = re.split('[:][:]', word)
                    if x[0] == '*':
                        self.set_token('ASTERISK', x[0], row, column)
                    else:
                        self.set_token('ID', x[0], row, column)
                    column = column + 1
                    self.set_token('DOUBLE_COLON', '::', row, column)
                    column = column + 1
                    self.set_token('ID', x[1], row, column)
                    if comma_found == True:
                        column = column + 1
                        self.set_token('COMMA', ',', row, column)
                        comma_found = False
                    continue
                elif re.match('[#]([a-fA-F]|[0-9]){6}',word):
                    if word.endswith(';'):
                        word = word.replace(';','')
                        semicolon_found = True
                    self.set_token('HEX_NUMBER', word, row, column)
                    if semicolon_found == True:
                        column = column + 1
                        self.set_token('SEMICOLON', ';', row, column)
                        semicolon_found = False
                elif re.match(id1_pattern, word):
                    if word.endswith(';'):
                        word = word.replace(';', '')
                        semicolon_found = True
                    if word.endswith(','):
                        word = word.replace(',', '')
                        comma_found = True
                    x = re.split('[#]', word)
                    self.set_token('ID', x[1], row, column)
                    column = column + 1
                    self.set_token('HASHTAG', '#', row, column)
                    if comma_found == True:
                        column = column + 1
                        self.set_token('COMMA', ',', row, column)
                        comma_found = False
                    if semicolon_found == True:
                        column = column + 1
                        self.set_token('SEMICOLON', ';', row, column)
                        semicolon_found = False
                    continue

                # PERCENTAGE
                elif re.match('[0-9]*[%]', word):
                    if re.findall(';', word):
                        word = word.replace(';', '')
                        self.set_token('PERCENTAGE_NUMBER', word, row, column)
                        column = column + 1
                        self.set_token('SEMICOLON',';', row, column)
                        continue
                    else:
                        self.set_token('PERCENTAGE_NUMBER', word, row, column)
                        continue
                # NUMBERS
                elif re.match('[-][0-9]+',word):
                    if re.findall(';', word):
                        word = word.replace(';','')
                        semicolon_found = True
                    y = re.findall('[-][0-9]+', word)
                    self.set_token('NEGATIVE_NUMBER', y[0], row, column)
                    x = re.split('[-][0-9]+', word)
                    unit = x[1]
                    measureUnit = self.getUnit(unit)
                    if measureUnit != '':
                        column = column + 1
                        self.set_token('MEASURE_UNIT', measureUnit, row, column)
                    if semicolon_found == True:
                        column = column + 1
                        self.set_token('SEMICOLON',';', row, column)
                        semicolon_found = False
                    continue
                elif re.match('[0-9]+[.][0-9]+',word):
                    if re.findall(';', word):
                        word = word.replace(';','')
                        semicolon_found = True
                    y = re.findall('[0-9]+[.][0-9]+', word)
                    self.set_token('NUMBER', y[0], row, column)
                    x = re.split('[0-9]+[.][0-9]+', word)
                    unit = x[1]
                    measureUnit = self.getUnit(unit)
                elif re.match('[0-9]+',word):
                    if re.findall(';', word):
                        word = word.replace(';','')
                        semicolon_found = True
                    y = re.findall('[0-9]+', word)
                    self.set_token('NUMBER', y[0], row, column)
                    x = re.split('[0-9]+', word)
                    unit = x[1]
                    measureUnit = self.getUnit(unit)

                    if measureUnit != '':
                        column = column + 1
                        self.set_token('MEASURE_UNIT', measureUnit, row, column)
                    if semicolon_found == True:
                        column = column + 1
                        self.set_token('SEMICOLON',';', row, column)
                        semicolon_found = False
                    continue
                # VALUES
                elif word.endswith(';'):
                    word = word.replace(';', '')
                    if re.match('[0-9]+', word):
                        self.set_token('NUMBER', word, row, column)
                    else:
                        self.set_token('ID', word, row, column)
                    column = column + 1
                    self.set_token('SEMICOLON', ';', row, column)
                # RESERVED WORDS
                elif word.endswith(':'):
                    word = word.replace(':', '')
                    self.set_token(self.reservedToken(word), word, row, column)
                    self.set_token('COLON', ':', row, column)
                # CHARACTERS
                elif word == '{':
                    self.set_token('LEFT_BRACE', word, row, column)
                    continue
                elif word == '}':
                    self.set_token('RIGHT_BRACE', word, row, column)
                    continue
                elif word == ';':
                    self.set_token('SEMICOLON', word, row, column)
                    continue
                # STRINGS
                elif word.startswith('"') and string_found == False:
                    self.aux += word + ' '
                    string_found = True
                    if word.endswith('"') and string_found == True:
                        self.set_token('STRING', word, row, column)
                        string_found = False
                        continue
                    if word.endswith(';') and string_found == True:
                        word = word.replace(';','')
                        self.set_token('STRING', word, row, column)
                        column = column + 1
                        self.set_token('SEMICOLON', ';', row, column)
                        string_found = False
                        continue
                    continue
                # ERRORS
                else:
                    x = re.match('^[A-Za-z0-9_-]*$', word)
                    if x:
                        y = self.reservedToken(word)
                        if y != '':
                            self.set_token(y, word, row, column)
                        else:
                            self.set_token('ID', word, row, column)
                        continue
                    else:
                        self.set_error(word, row)
                    continue
                column = column + 1
            column = 1
            row = row + 1


    def reservedToken(self, word):
        for item in self.reserved:
            if word == item:
                return 'RESERVED_' + item.upper()
        return 'ID'
    def getUnit(self, word):
        for unit in self.unit_measure:
            if word == unit:
                return unit
        return ''
    def split(self, text):
        return list(text)

    def set_token(self, token_type, value, row, column):
        self.aux = ''
        new_token = Token(token_type,value,row ,column)
        if new_token not in self.token_list:
            self.token_list.append(new_token)
        else:
            print('Token is already in.')

    def set_error(self, value,row):
        self.aux = ""
        new_error = Error(value, "La entrada \"" + value + "\" en la fila " + str(row) + " no pertenece al lenguaje.")
        self.error_list.append(new_error)