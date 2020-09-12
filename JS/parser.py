from JS.token import Token

class Error:
    def __init__(self, error):
        self.error = error

    def get_error(self):
        return self.error
# For each Non-Terminal on the left-side implement a method. For each Non-Terminal on the right-side make a call to corresponded method.
# For each Terminal on the right-side, match.
class JSParser:
    def __init__(self):
        self.error_list = []
        self.numPreToken = 0
        self.preToken = ''
        self.data = ''

    def parse(self, dataAux):
        self.data = dataAux
        self.numPreToken = 0
        self.preToken = self.data[self.numPreToken]
        self.E()

    def E(self):
        # E-> T EP
        self.T()
        self.EP()

    def EP(self):
        if self.preToken.get_type() == 'ADD_OPT':
            # EP-> + T EP
            self.match('ADD_OPT')
            self.T()
            self.EP()
        elif self.preToken.get_type() == 'SUBS_OPT':
            # EP-> - T EP
            self.match('SUBS_OPT')
            self.T()
            self.EP()
        else:
            return
        # EP-> EPSILON

    def T(self):
        # T->F TP
        self.F()
        self.TP()

    def TP(self):
        if self.preToken.get_type() == 'MULT_OPT':
            # TP-> * F TP
            self.match('MULT_OPT')
            self.F()
            self.TP()
        elif self.preToken.get_type() == 'DIV_OPT':
            # TP-> / F TP
            self.match('DIV_OPT')
            self.F()
            self.TP()
        else:
            return
        # TP-> EPSILON

    def F(self):
        if self.preToken.get_type() == 'LEFT_PARENT':
            # F-> ( E )
            self.match('LEFT_PARENT')
            self.E()
            self.match('RIGHT_PARENT')

        elif self.preToken.get_type() == 'ID':
            # F -> ID
            self.match('ID')
        else:
            # F -> NUMBER
            self.match('NUMBER')

    def match(self, type):
        if type != self.preToken.get_type():
            new_error = Error(self.getError(type))
            self.error_list.append(new_error)
            print("expected", self.getError(type))
        if self.preToken.get_type() != 'LAST':
            self.numPreToken = self.numPreToken + 1
            self.preToken = self.data[self.numPreToken]


    def getError(self, p):
        if p == "RIGHT_PARENT":
            return ')'
        elif p == "LEFT_PARENT":
            return '('
        elif p == "DIV_OPT":
            return '/'
        elif p == "ADD_OPT":
            return '+'
        elif p == "MULT_OPT":
            return '*'
        elif p == "SUBS_OPT":
            return '-'
        elif p == "LEFT_BRACE":
            return '{'
        elif p == "RIGHT_BRACE":
            return '}'
        elif p == "NUMBER":
            return 'Numero'
        elif p == "ID":
            return 'ID'
        else:
            return "Desconocido"
