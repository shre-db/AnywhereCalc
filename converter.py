import re


class Converter:
    """
    Converts an infix expression to postfix. Supports four elementary arithmetic operations for multi-digit operands.

    Attributes
    ----------
        expression (str): The infix expression to be converted to postfix expression.
        output (str): Whether the output should be a string or a list of items after conversion.

    Methods
    -------
        convert(): This method converts a given infix expression to postfix form.
    """

    # Initialize attributes
    def __init__(self, expression: str, output='list') -> None:
        self.output = output
        self.infix = expression
        self.stack = []
        self.postfix = []
        self.operands = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ' ']
        self.operators = {'+': 0, '-': 0, '*': 1, '/': 1}

    # Pop an item from stack
    def _pop(self):
        return self.stack.pop()

    # Push an item to stack
    def _push(self, item):
        self.stack.append(item)

    # Return last item in the stack
    def _peek(self):
        try:
            return self.stack[-1]
        except IndexError:
            print("Stack is empty")

    # Discard last item from the stack
    def _discard(self):
        self.stack.pop()

    # Check if a character is an operand
    def _is_operand(self, char):
        return True if char in self.operands else False

    # Check if a character is an operator
    def _is_operator(self, char):
        return True if char in self.operators else False

    # Check if the stack is empty
    def _is_empty(self):
        return True if len(self.stack) == 0 else False

    @staticmethod
    def _is_number(string: str) -> bool:
        """
        This method checks if a string is numeric.
        :param string:
        :return: bool
        """
        if string == '.':
            return True
        try:
            float(string)
            return True
        except ValueError:
            return False

    def _inflate(self):
        """
        This method adds space next to numbers in infix expression.
        :return: The inflated infix expression.
        """
        positions = re.finditer(r'\d+(\.\d+)?', self.infix)
        pos = []
        for item in positions:
            pos.append(item.end())

        # Inflate the infix expression
        # Step 1: Convert the expression to list.
        expression = [char for char in self.infix]

        # Step 2: Add space at (index specified by pos + iteration number).
        for i in range(len(pos)):
            expression.insert(pos[i] + i, ' ')

        # Step 3: Convert the inflated list back to string
        expression = ''.join(expression)
        return expression

    # This function converts the infix expression to postfix
    def convert(self):
        """This method converts the infix expression to postfix."""
        self.infix = self._inflate()
        index = 0
        while index < len(self.infix):

            # if character is an OPERAND push to the postfix expression
            char = self.infix[index]
            if self._is_operand(char):
                self.postfix.append(char)

            # else if the character is an OPERATOR
            elif self._is_operator(char):
                # if stack is empty, push the incoming operator to stack.
                if self._is_empty():
                    self._push(char)
                # if '(' is present on top the stack, directly push incoming operators to the stack.
                elif self._peek() == '(':
                    self._push(char)
                # else if stack is not empty.
                else:
                    # while the precedence of the incoming operator is less than or equal to that on top of the stack
                    while not self._is_empty() and not self._peek() == '(' and self.operators[char] <= self.operators[self._peek()]:
                        # if '(' is present on top the stack, directly push incoming operators to the stack.
                        if self._peek() == '(':
                            self._push(char)
                        else:
                            popped_item = self._pop()  # pop item from top of the stack
                            self.postfix.append(popped_item)  # push popped item to postfix expression
                    # while the precedence of the incoming operator is greater than that on top of the stack,
                    self._push(char)  # push the incoming item to the stack

            # else if the character is '(', push it to the stack
            elif char == "(":
                self._push(char)

            # else if the character is ')'
            elif char == ")":
                while self._peek() != '(':  # until a '(' is encountered,
                    popped_item = self._pop()  # pop items from stack.
                    self.postfix.append(popped_item)  # push the popped item to postfix.
                self._discard()  # discard the '('

            index += 1

        while not self._is_empty():
            popped_item = self._pop()
            self.postfix.append(popped_item)

        def _diff(num1: int, num2: int) -> int:
            """
            This is a local function that returns the difference of two numbers.
            :param num1:
            :param num2:
            :return: num2 - num1
            """
            return num2 - num1

        slices = []  # This list stores modified slices of expression
        index = []  # This list stores slicing index of current expression to create new expression.
        num_indices = []  # This list temporarily store indices of numerical strings in the considered expression.

        # 1. Get the postfix expression and store it.
        ex = self.postfix
        slices.append(ex)
        item = 0
        while item < len(ex):
            # 2. Map next item.
            is_num = Converter._is_number(ex[item])
            # 3. If it is a number, append its index, else repeat Step 2.
            if is_num:
                num_indices.append(item)
                # 4. If number of item in num_indices is greater than 1, Calculate the difference of last two items, else repeat Step.
                if len(num_indices) > 1:
                    difference = _diff(num_indices[-2], num_indices[-1])
                    # 5. If the difference is 1, store the slicing index, else repeat Step 2.
                    if difference == 1:
                        index.append(num_indices[-2])
                        # 6. Slice the expression starting from indices that resulted in a difference of 1, else repeat Step.
                        ex = ex[num_indices[-2]:]
                        # 7. Combine first two item in the expression
                        concat_item = ex[0] + ex[1]
                        ex[:2] = [concat_item]
                        # 8. Store the new expression
                        slices.append(ex)
                        # 9. Repeat steps 1 to 8 with the new expression, until the expression exhausts.
                        num_indices = []
                        item = 0
                    else:
                        item += 1
                else:
                    item += 1
            else:
                item += 1

        # 10. Replace part of every old expression with the new one starting from respective slicing indices iteratively.
        # Reverse slices list
        slices = slices[::-1]
        # Reverse index list
        index = index[::-1]
        # Iteratively remove all items from next expression in 'slices' from indices specified by index and replace with the previous expression.
        exp = 0
        while len(slices) > 1:
            slices[exp + 1][index[exp]:] = slices[exp][:]
            slices.remove(slices[0])
            index.remove(index[0])
        slices = sum(slices, [])

        if self.output == 'list':
            return slices
        elif self.output == 'expr':
            return "".join(slices)
