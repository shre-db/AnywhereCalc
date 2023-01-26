class Converter:

    # Initialize an empty stack and empty postfix list
    def __init__(self, expression: str) -> None:
        self.infix = expression
        self.stack = []
        self.postfix = []
        self.operands = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
        self.operators = {'+': 0, '-': 0, '*': 1, '/': 1}

    # Pop an item from stack
    def pop(self):
        return self.stack.pop()

    # Push an item to stack
    def push(self, item):
        self.stack.append(item)

    # Return last item in the stack
    def peek(self):
        try:
            return self.stack[-1]
        except IndexError:
            print("Stack is empty")

    # Discard last item from the stack
    def discard(self):
        self.stack.pop()

    # Check if a character is an operand
    def is_operand(self, char):
        return True if char in self.operands else False

    # Check if a character is an operator
    def is_operator(self, char):
        return True if char in self.operators else False

    # Check if the stack is empty
    def is_empty(self):
        return True if len(self.stack) == 0 else False

    # This function converts the infix expression to postfix
    def convert(self):
        index = 0
        while index < len(self.infix):

            # if character is an OPERAND push to the postfix expression
            char = self.infix[index]
            if self.is_operand(char):
                self.postfix.append(char)

            # else if the character is an OPERATOR
            elif self.is_operator(char):
                # if stack is empty, push the incoming operator to stack.
                if self.is_empty():
                    self.push(char)
                # if '(' is present on top the stack, directly push incoming operators to the stack.
                elif self.peek() == '(':
                    self.push(char)
                # else if stack is not empty.
                else:
                    # while the precedence of the incoming operator is less than or equal to that on top of the stack
                    while not self.is_empty() and not self.peek() == '(' and self.operators[char] <= self.operators[self.peek()]:
                        # if '(' is present on top the stack, directly push incoming operators to the stack.
                        if self.peek() == '(':
                            self.push(char)
                        else:
                            popped_item = self.pop()  # pop item from top of the stack
                            self.postfix.append(popped_item)  # push popped item to postfix expression
                    # while the precedence of the incoming operator is greater than that on top of the stack,
                    self.push(char)  # push the incoming item to the stack

            # else if the character is '(', push it to the stack
            elif char == "(":
                self.push(char)

            # else if the character is ')'
            elif char == ")":
                while self.peek() != '(':  # until a '(' is encountered,
                    popped_item = self.pop()  # pop items from stack.
                    self.postfix.append(popped_item)  # push the popped item to postfix.
                self.discard()  # discard the '('

            index += 1

        while not self.is_empty():
            popped_item = self.pop()
            self.postfix.append(popped_item)

        postfix_exp = "".join(self.postfix)

        return postfix_exp
