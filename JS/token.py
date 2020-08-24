from enum import Enum

class Token:
    def __init__(self, type, value, row, column):
        self.__type = type
        self.__value = value
        self.__row = row
        self.__column = column

    def get_value(self):
        return self.__value

    def get_type(self):
        return self.__type

    def get_column(self):
        return str(self.__column)

    def get_row(self):
        return str(self.__row)


