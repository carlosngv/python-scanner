from JS.token import Token
import re

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

    def scan(self, data):
        comment_found = False
        class_def_found = False
        variable_found = False
        condition_found = False
        comment_oneline_found = False
        string_found = False
        string_found2= False
        parameters_found = False
        ifparameters_found = False
        clgstring_found = False
        clg_pattern = '[a-zA-Z]+([a-zA-Z]*|[0-9]*|[-]?|[_]?)*"[)][;]?'
        variable_end_patter = "[a-zA-Z]+([a-zA-Z]*|[0-9]|[-]?|[_]?)[;]"
        constructor_pattern = "constructor[(][a-zA-Z]+([0-9]|[a-zA-Z]|[,]?|\s)*[)]"
        function_pattern = "[a-zA-Z]+[0-9]*[(][a-zA-Z]+([0-9]|[a-zA-Z]|[,]?|\s)*[)]"
        function_id_pattern = "[(][a-zA-Z]+([0-9]|[a-zA-Z]|[,]?|\s)*[)]"
        string_func ="(\"([a-zA-Z]*|[0-9]*|[,]*|\s*)\")"
        function_call_pattern = "([a-zA-Z]+|[0-9]*)[(]([a-zA-Z]*|[0-9]*)[)]"


        column = 1
        row = 1

        input = data.splitlines()
        for line in input:
            words = line.split()
            print(words)
            if comment_oneline_found == True:
                comment_oneline_found = False
                self.set_token('COMMENT', self.aux, row, column)
            for word in words:

                word = word.lstrip('\t')
                if word.endswith('*/'):
                    self.aux += word
                    comment_found = False
                    self.set_token('COMMENT', self.aux, row, column)
                    continue
                elif re.match(clg_pattern, word) and clgstring_found == True:
                    x = re.sub("\)", '', word)
                    semicolon = re.findall('[;]', x)
                    if len(semicolon) > 0:
                        y = re.sub('[;]','',x)
                        self.aux += y + ' '
                        self.set_token('STRING', self.aux, row, column)
                        self.set_token('RIGHT_PARENT', ')', row, column + 1)
                        self.set_token('SEMICOLON', ';', row, column + 1)
                    else:
                        self.aux += x + ' '
                        self.set_token('STRING', self.aux, row, column)
                        self.set_token('RIGHT_PARENT', ')', row, column + 1)
                    clgstring_found = False
                    continue

                elif (word.endswith(')') or word.endswith(';')) and parameters_found == True:
                    if re.findall(';', word):
                        x = re.sub(';', '', word)
                        y = re.sub('\)', '', x)
                        if re.match('[0-9]+', y):
                            self.set_token('NUMBER', y, row, column)
                        else:
                            self.set_token('ID', y, row, column)
                        self.set_token('RIGHT_PARENT',')',row,column+1)
                        self.set_token('SEMICOLON ',';',row,column+1)
                        parameters_found = False
                    else:
                        y = re.sub('\)', '', word)
                        if re.match('[0-9]+', y):
                            self.set_token('NUMBER', y, row, column)
                        else:
                            self.set_token('ID', y, row, column)
                        self.set_token('RIGHT_PARENT',')',row,column+1)
                        parameters_found =False

                elif word.endswith(';') and (len(re.findall('\(',word)) == 0):
                    x = re.sub(';', '', word)
                    if x == 'true':
                        self.set_token('RESERVED_TRUE', x, row, column)
                        self.set_token('SEMICOLON', ';', row, column)

                    elif x == 'false':
                        self.set_token('RESERVED_FALSE', x, row, column)
                        self.set_token('SEMICOLON', ';', row, column)

                    elif x == '++':
                        self.set_token('INCR_OP', x, row, column)
                        self.set_token('SEMICOLON', ';', row, column)

                    elif x == '--':
                        self.set_token('DECR_OP', x, row, column)
                        self.set_token('SEMICOLON', ';', row, column)
                    elif re.match('[0-9]+', x):
                        self.set_token('NUMBER', x, row, column)
                        self.set_token('SEMICOLON', ';', row, column)
                    else:
                        self.set_token('ID', x, row, column)
                        self.set_token('SEMICOLON', ';', row, column)
                    continue

                elif re.findall('for', word):
                    self.set_token('RESERVED_FOR', 'for', row, column)
                    if re.findall('\(', word):
                        self.set_token('LEFT_PARENT', '(', row, column + 1)
                        x = re.sub('for\(', '', word)
                        self.set_token('ID', x, row, column + 1)
                    continue



                elif re.findall('while', word):
                    self.set_token('RESERVED_WHILE', 'while', row, column)
                    if re.findall('\(', word):
                        self.set_token('LEFT_PARENT', '(', row, column + 1)
                        x = re.sub('while\(', '', word)
                        self.set_token('ID', x, row, column + 1)
                        if re.findall('\)', word):
                            y = re.sub('\)', '', x)
                            if re.match('[0-9]*', y):
                                self.set_token('NUMBER', y, row, column + 1)
                            else:
                                self.set_token('ID', y, row, column + 1)
                        else:
                            ifparameters_found = True
                    continue
                elif re.match(function_call_pattern, word):
                    argsp = re.split('\(',word) # myfunction, aarg);
                    argsp2 = re.sub('\)','',argsp[1])
                    r = re.sub('[(]', '', word)
                    x = re.sub('[)]','',r)
                    if re.findall(';', x):
                        y = re.sub(';', '', x)
                        arg = re.sub(';','',argsp2)
                        if len(arg) == 0:
                            self.set_token('ID', argsp[0], row, column)
                            self.set_token('LEFT_PARENT','(',row, column + 1)
                            self.set_token('RIGHT_PARENT',')',row, column + 1)
                            self.set_token('SEMICOLON',';',row, column + 1)
                        else:
                            self.set_token('ID', argsp[0], row, column)
                            self.set_token('LEFT_PARENT', '(', row, column + 1)
                            self.set_token('ID', arg, row, column + 1)
                            self.set_token('RIGHT_PARENT', ')', row, column + 1)
                            self.set_token('SEMICOLON', ';', row, column + 1)
                    else:
                        self.set_token('ID', argsp[0], row, column)
                        self.set_token('LEFT_PARENT', '(', row, column + 1)
                        self.set_token('RIGHT_PARENT', ')', row, column + 1)
                    continue
                elif re.findall('if', word):
                    self.set_token('RESERVED_IF', 'if', row, column)
                    if re.findall('\(', word):
                        self.set_token('LEFT_PARENT', '(', row, column + 1)
                        x = re.sub('if\(','', word)
                        self.set_token('ID', x, row, column + 1)
                        if re.findall('\)', word):
                            y = re.sub('\)', '', x)
                            if re.match('[0-9]+', y):
                                self.set_token('NUMBER', y, row, column + 1)
                            else:
                                self.set_token('ID', y, row, column + 1)
                        else:
                            ifparameters_found = True
                elif re.findall ('\)[{]', word) and ifparameters_found == True:
                    x = re.sub('\)[{]', ' ', word)
                    if x:
                        if re.match('[0-9]+', x):
                            self.set_token('NUMBER', x, row, column + 1)
                            ifparameters_found = False
                            self.set_token('RIGHT_PARENT', ')', row, column)
                            self.set_token('LEFT_BRACE', '{', row, column + 1)
                        else:
                            self.set_token('ID', x, row, column + 1)
                            ifparameters_found= False
                            self.set_token('RIGHT_PARENT', ')', row, column)
                            self.set_token('LEFT_BRACE', '{', row, column + 1)
                    continue
                elif word.endswith(')') and ifparameters_found == True:
                    x = re.sub('\)','',word)
                    if re.match('[0-9]+', x):
                        self.set_token('NUMBER', x, row, column + 1)
                        self.set_token('RIGHT_PARENT', ')', row, column + 1)

                        ifparameters_found = False
                    else:
                        self.set_token('ID', x, row, column + 1)
                        self.set_token('RIGHT_PARENT', ')', row, column + 1)

                        ifparameters_found = False
                    continue
                elif re.findall("constructor",word):
                    self.set_token("RESERVED_CONSTRUCTOR", 'constructor', row, column)
                    if re.findall('\(',word):
                        self.set_token("LEFT_PARENT", '(', row, column+1)
                        x = re.sub('^constructor\(','',word)
                        if re.findall(',', word):
                            y = re.sub(',','',x) # FIRST PARAMETER
                            self.set_token('ID', y, row, column + 1)
                            self.set_token('COMA', ',', row, column + 1)
                            parameters_found = True
                        else:
                            self.set_token('ID', x, row, column + 1)
                        continue

                elif re.findall("Math.pow", word) and parameters_found == False:
                    self.set_token("RESERVED_MATH", 'Math', row, column)
                    self.set_token("RESERVED_POW", 'pow', row, column+1)
                    self.set_token("DOT", '.', row, column+1)
                    if re.findall("\(", word):
                        self.set_token('LEFT_PARENT','(', row, column+1)
                        x = re.sub("^Math.pow\(", "", word)
                        if re.findall(',', x):
                            y = re.sub(',', '', x)
                            self.set_token('ID', y, row, column+1) # FIRST PARAMETER
                        else:
                            self.set_token('ID', x, row, column+1) # FIRST PARAMETER
                        parameters_found = True
                        if re.findall(",", word):
                            self.set_token('COMA', ',', row, column + 1)
                    continue

                elif parameters_found == True:
                    self.aux += word + ' '

                elif re.findall('console.log', word) and string_found == False:
                    self.set_token('RESERVED_CONSOLE', 'console', row, column)
                    self.set_token('DOT', '.', row, column + 1)
                    self.set_token('RESERVED_LOG', 'log', row, column + 1)
                    if re.findall('\(', word):
                        self.set_token('LEFT_PARENT','(', row, column+1)
                        z = re.sub("console.log", '', word)
                        y = re.sub("\(", '', z)
                        w = re.sub("\)", '', y)
                        if w.startswith('"'):
                            self.aux += w + ' '
                            clgstring_found = True
                        else:
                            self.set_token('ID', w, row, column + 1)
                            variable_found = True
                            self.set_token('RIGHT_PARENT', ')', row, column + 1)

                    continue


                elif comment_oneline_found == True:
                    self.aux += word + ' '

                elif word.endswith('"') and string_found == True:
                    self.aux += word
                    self.set_token("STRING", self.aux, row, column)
                    string_found = False
                    continue

                elif string_found == True:
                    self.aux += word + ' '

                elif word.endswith(')') and clgstring_found == True: # WITHOUT COMA
                    self.aux += word
                    x = re.sub('\)', '', self.aux)
                    print('AUX:', x)
                    self.set_token("STRING", x, row, column)
                    self.set_token("RIGHT_PARENT", ')', row, column+1)
                    clgstring_found = False
                    continue

                elif clgstring_found == True:
                    self.aux += word + ' '
                    continue

                elif word.endswith(';') and clgstring_found == True: # WITHOUT COMA
                    self.aux += word
                    x = re.sub('\)', '', self.aux)
                    y = re.sub('[;]', '', x)
                    print('AUX:', y)
                    self.set_token("STRING", y, row, column)
                    self.set_token("RIGHT_PARENT", ')', row, column+1)
                    self.set_token("SEMICOLON", ';', row, column+1)
                    clgstring_found = False
                    continue

                elif clgstring_found == True:
                    self.aux += word + ' '
                    continue

                elif re.match("constructor", word):
                    self.set_token('RESERVED_CONSTRUCTOR', 'constructor', row, column)

                elif word.endswith('\''):
                    self.aux += word + ' '
                    self.set_token("STRING", self.aux, row, column)
                    string_found2 = False

                elif string_found2 == True:
                    self.aux += word + ' '

                elif re.match(variable_end_patter, word):
                    x = re.sub(';', '', word)
                    if x == 'false':
                        self.set_token('RESERVED_FALSE', x, row, column)
                    elif x == 'true':
                        self.set_token('RESERVED_TRUE', x, row, column)
                    else:
                        self.set_token('ID', x, row, column)
                    self.set_token('SEMICOLON',';', row, column+1)

                elif re.match(function_pattern, word):
                    x = re.sub(function_id_pattern, '', word)
                    y = re.findall("[;]",x)
                    z = re.sub("[;]", "", x)
                    self.set_token('LEFT_PARENT', '(', row, column)
                    self.set_token('ID', z, row, column + 1)
                    self.set_token('RIGHT_PARENT', ')', row, column+1)
                    if len(y) > 0:
                        self.set_token('SEMICOLON', ';', row, column+1)
                    continue

                elif comment_found == True:
                    self.aux += word + ' '

                elif class_def_found == True:
                    self.aux += word
                    self.set_token('ID', self.aux, row, column)
                    class_def_found = False

                elif variable_found == True:
                    self.aux += word
                    self.set_token('VARIABLE', self.aux, row, column)
                    variable_found = False

                elif comment_found == False and variable_found == False and string_found == False and string_found2 == False and parameters_found == False and class_def_found == False:
                    if word == 'function':
                        self.set_token('RESERVED_FUNCTION', word, row, column)

                    elif word.startswith('/*'):
                        self.aux += word + ' '
                        comment_found = True

                    elif re.match('[0-9]', word):
                        x = re.sub("[^0-9]",'', word)
                        self.set_token('NUMBER', x, row, column)

                    elif word == ')':
                        self.set_token('RIGHT_PARENT', word, row, column)

                    elif word == '(':
                        self.set_token('LEFT_PARENT', word, row, column)
                        self.aux += word

                    elif word.startswith('('):
                        x = re.sub('\(','', word)
                        self.set_token('LEFT_PARENT', '(', row, column + 1)
                        if re.findall(',', word):
                            y = re.sub(',','',x)
                            self.set_token('ID', y, row, column + 1)
                            self.set_token('COMA',',', row, column + 1)
                        else:
                            self.set_token('ID', x, row, column + 1)
                        continue

                    elif word.endswith(')'):
                        x = re.sub('\)','', word)
                        if re.match('[0-9]+', x):
                            self.set_token('NUMBER', x, row, column)
                            self.set_token('RIGHT_PARENT', ')', row, column + 1)
                        elif re.findall('[+]+', x):
                            y = re.sub('[+]+','', x)
                            if y:
                                self.set_token('ID', y, row, column + 1)
                            self.set_token('INCR_OP', '++',row, column+1)
                            self.set_token('RIGHT_PARENT', ')', row, column + 1)
                        elif re.findall('[-]+', x):
                            y = re.sub('[-]+','', x)
                            if y:
                                self.set_token('ID', y, row, column + 1)
                            self.set_token('DECR_OP', '--',row, column+1)
                            self.set_token('RIGHT_PARENT', ')', row, column + 1)
                        else:
                            self.set_token('ID', x, row, column + 1)
                            self.set_token('RIGHT_PARENT', ')', row, column + 1)
                        continue

                    elif word == 'var':
                        self.set_token('RESERVED_VAR', word, row, column)
                        variable_found = True
                    elif word == 'const':
                        self.set_token('RESERVED_CONST', word, row, column)
                        variable_found = True
                    elif word == 'console':
                        self.set_token('RESERVED_CONSOLE', word, row, column)
                    elif word == '=':
                        self.set_token('OPERAND_EQUAL', word, row, column)
                    elif word == '+':
                        self.set_token('OPERAND_SUM', word, row, column)
                    elif word == '-':
                        self.set_token('OPERAND_SUBS', word, row, column)
                    elif word == '*':
                        self.set_token('OPERAND_MULT', word, row, column)
                    elif word == 'while':
                        self.set_token('RESERVED_WHILE', word, row, column)
                        condition_found = True
                    elif word == 'continue':
                        self.set_token('RESERVED_CONTINUE', word, row, column)
                    elif word == '.':
                        self.set_token('OPERAND_SUBS', word, row, column)
                    elif word == 'break':
                        self.set_token('RESERVED_BREAK', word, row, column)
                    elif word == 'true':
                        self.set_token('RESERVED_TRUE', word, row, column)
                    elif word == 'false':
                        self.set_token('RESERVED_FALSE', word, row, column)
                    elif word == 'for':
                        self.set_token('RESERVED_FOR', word, row, column)
                        condition_found = True
                    elif word == 'else':
                        self.set_token('RESERVED_ELSE', word, row, column)
                    elif word == 'do':
                        self.set_token('RESERVED_DO', word, row, column)
                    elif word == '}':
                        self.set_token('RIGHT_BRACE', word, row, column)
                    elif word == 'class':
                        self.set_token('RIGHT_CLASS', word, row, column)
                        class_def_found = True
                    elif word == '{':
                        self.set_token('LEFT_BRACE', word, row, column)
                    elif word == ']':
                        self.set_token('RIGHT_BRACKET', word, row, column)
                    elif word == '[':
                        self.set_token('LEFT_BRACKET', word, row, column)
                    elif word == ';':
                        self.set_token('SEMICOLON', word, row, column)
                    elif word == '>':
                        self.set_token('GREATER_OP', word, row, column)
                    elif word == '<':
                        self.set_token('LESS_OP', word, row, column)
                    elif word == '*=':
                        self.set_token('ASSIGNMENT', word, row, column)
                    elif word == '>=':
                        self.set_token('GREATER_EQUAL', word, row, column)
                    elif word == '<=':
                        self.set_token('LESS_EQUAL', word, row, column)
                    elif word == '+=':
                        self.set_token('ASSIGNMENT', word, row, column)
                    elif word == '===':
                        self.set_token('EQUAL_OP', word, row, column)

                    elif word.startswith('"') and string_found == False:
                        self.aux += word + ' '
                        string_found = True
                        if word.endswith('"') and string_found == True:
                            self.set_token('STRING', word, row, column)
                            string_found = False
                            continue
                        continue

                    elif word == 'return':
                        self.set_token('RESERVED_RETURN',word, row, column)
                    elif word.startswith('\''):
                        self.aux += word + ' '
                        string_found2 = True
                        if word.endswith('\'') and string_found2 == True:
                            self.set_token('STRING', word, row, column)
                            string_found2 = False
                            continue
                        continue

                    elif word.endswith('"'):
                        self.aux += word
                        self.set_token('STRING', self.aux, row, column)

                    elif word.endswith('=='):
                        self.aux += word
                        self.set_token('EQUAL_OP', self.aux, row, column)

                    elif word.startswith('\''):
                        self.aux += word + ' '
                        continue

                    elif word.startswith('this'):
                        self.set_token('RESERVED_THIS','this', row, column)
                        self.set_token('DOT','.', row, column+1)
                        x = re.sub('this\.','',word)
                        self.set_token('ID', x, row,column+1)
                        continue
                    elif word.endswith('\''):
                        self.aux += word
                        self.set_token('STRING', self.aux, row, column)

                    elif word.endswith('++'):
                        self.aux += word
                        self.set_token('INCR_OP', self.aux, row, column)

                    elif word.endswith('--'):
                        self.aux += word
                        self.set_token('DECR_OP', self.aux, row, column)

                    elif word.endswith('&&'):
                        self.aux += word
                        self.set_token('AND_OP', self.aux, row, column)

                    elif word.endswith('=>'):
                        self.aux += word
                        self.set_token('RESERVED_ARROW', self.aux, row, column)

                    elif word == '//':
                        self.aux += word
                        comment_oneline_found = True
                        continue

                    else:
                        x = re.match('^[A-Za-z0-9_-]*$', word)
                        if x:
                            self.set_token('ID', word, row, column)
                        else:
                            self.set_error(word, row)
                        continue
                    column = column + 1
            column = 1
            row = row + 1





    def set_token(self, token_type, value, row, column):
        self.aux = ""
        new_token = Token(token_type,value,row ,column)
        if new_token not in self.token_list:
            self.token_list.append(new_token)
        else:
            print('Token is already in.')

    def set_error(self, value,row):
        self.aux = ""
        new_error = Error(value, "La entrada \"" + value + "\" en la fila " + str(row) + " no pertenece al lenguaje.")
        self.error_list.append(new_error)


