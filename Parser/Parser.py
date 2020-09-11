from Stack import Stack
class Parser:

    def parse(self):
        stack = Stack()
        data = '(7/6*2)-(var1 * exp1/r)/(6-8))'
        data = list(data)
        for char in data:
            if char == '(' or char == '[' or char == '{':
                stack.push(char)
            else:
                if char == ')':
                    if stack.peek() != '(':
                        return 'No válido'
                else:
                    if char == ']':
                        if stack.peek() != '[':
                            return 'No válido'
                    else:
                        if char == '}':
                            if stack.peek() != '{':
                                return 'No válido'

        return stack.isEmpty()



new_parser = Parser()
print(new_parser.parse())
