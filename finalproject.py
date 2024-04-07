import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import math as m

# Define the main application class
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')

        # Variable to hold the value displayed on the calculator
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)

        # Define the buttons and their corresponding key bindings
        self.funcs = [('c', 'C'), ('^', '^'), ('s', ' '), ('(', '('),
                      ('S', ' '), ('C', ' '), ('T', ' '), (')', ')'),
                      ('L', ' '), ('l', ' '), ('F', '!'), ('/', '/'),
                      ('7', '7'), ('8', '8'), ('9', '9'), ('*', '*'),
                      ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
                      ('1', '1'), ('2', '2'), ('3', '3'), ('+', '+'),
                      ('d', '<BackSpace>'), ('0', '0'), ('.', '.'), ('=', '<Return>')]

        # Dictionary to hold the buttons
        self.buttons = {}

        # Create buttons and bind key presses
        for i, (b, key) in enumerate(self.funcs):
            if b == "c":
                self.buttons[b] = ClearButton(row=i//4+1, column=i%4)
                self.root.bind(key, self.key_press)
            elif b == 'd':
                self.buttons[b] = DelButton(row=i//4+1, column=i%4)
                self.root.bind(key, self.key_press)
            elif b == "=":
                self.buttons[b] = EqualsButton(b, row=i//4+1, column=i%4)
                self.root.bind(key, self.key_press)
            elif b.isalpha() == False:
                self.buttons[b] = Button(b, row=i//4+1, column=i%4)
                self.root.bind(key, self.key_press)
            else:
                if b == "S":
                    x = "sin"
                elif b == "C":
                    x = "cos"
                elif b == "T":
                    x = "tan"
                elif b == "s":
                    x = "sqrt"
                elif b == "L":
                    x = "ln"
                elif b == "l":
                    x = "log"
                elif b == "F":
                    x = "!"
                self.buttons[b] = FuncButton(x, row=i//4+1, column=i%4)
                if(key != ' '):
                    self.root.bind(key, self.key_press)
            

    # Run the application
    def run(self):
        self.root.mainloop()

    # Handle key press events
    def key_press(self, event):
        if event.keysym == 'C':
            self.label_var.set('0')
        elif event.keysym == '^':
            self.label_var.set(self.label_var.get() + '^')
        elif event.keysym == '/':
            self.label_var.set(self.label_var.get() + '/')
        elif event.keysym == '*':
            self.label_var.set(self.label_var.get() + '*')
        elif event.keysym == '-':
            self.label_var.set(self.label_var.get() + '-')
        elif event.keysym == '+':
            self.label_var.set(self.label_var.get() + '+')
        elif event.keysym == '.':
            self.label_var.set(self.label_var.get() + '.')
        elif event.keysym == 'Space':
            self.label_var.set(self.label_var.get() + ' ')
        elif event.keysym == 'BackSpace':
            if app.label_var.get() != "0":
                x = str(app.label_var.get())[:-1]
                app.label_var.set(x)
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == '(':
            self.label_var.set(self.label_var.get() + '(')
        elif event.keysym == ')':
            self.label_var.set(self.label_var.get() + ')')
        else:
            self.label_var.set(self.label_var.get() + event.char)


#=============================================================================

class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.text = text
        self.grid(row=row, column=column)

    def counter(self):
        global app
        if app.label_var.get() == "0":
            x = self.text
        else:
            x = str(app.label_var.get()) + str(self.text)
        app.label_var.set(x)

#=============================================================================

class FuncButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)

    def counter(self):
        global app
        if app.label_var.get() == "0":
            x = self.text + "("
        else:
            x = str(app.label_var.get()) + str(self.text) + "("
        app.label_var.set(x)
        
#=============================================================================

class ClearButton(Button):
    def __init__(self, row, column):
        text = "clear"
        super().__init__(text, row, column)

    def counter(self):
        global app
        x = "0"
        app.label_var.set(x)
        
#=============================================================================

class DelButton(Button):
    def __init__(self, row, column):
        text = "del"
        super().__init__(text, row, column)
    def counter(self):
        global app
        if app.label_var.get() == "0":
            x = app.label_var.get()
        else:
            x = str(app.label_var.get())[:-1]
            app.label_var.set(x)

#=============================================================================

class EqualsButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)

    def counter(self):
        global app
        app.label_var.set(calculating(app.label_var.get()))

#=============================================================================

def isFloat(equation):
    try:
        float(equation)
        return True
    except ValueError:
        return False

#=============================================================================

def calculating(equation):
    op = Simple_Operations()
    i = 0
    while not isFloat(equation):
        
        if "!" in equation:
            op_index = equation.index("!")
            leftSide = ""
            
            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                leftSide = equation[i] + leftSide
                i -= 1
            
            result = op.factorial(float(leftSide))
            equation = str(equation[:op_index - len(leftSide)]) + str(result) + equation[op_index+1:]

        elif "(" in equation:
            start_index = equation.index("(")
            end_index = start_index + equation[start_index:].index(")")
            sub_eq = calculating(equation[start_index + 1:end_index])

            if isFloat(sub_eq):
                if start_index - 4 < 0:
                    start = 0
                else:
                    start = start_index - 4
                func = equation[start:start_index]
                if len(func) > 3:
                    if func[0].isalpha() or func[1].isalpha() or func[2].isalpha() or func[3].isalpha() or func[4].isalpha():
                        num = float(sub_eq)
                        if "sin" in func:
                            equation = equation.replace(equation[start_index - 3:end_index + 1], str(m.sin(num)))
                        elif "cos" in func:
                            equation = equation.replace(equation[start_index - 3:end_index + 1], str(m.cos(num)))
                        elif "tan" in func:
                            equation = equation.replace(equation[start_index - 3:end_index + 1], str(m.tan(num)))
                        elif "log" in func:
                            equation = equation.replace(equation[start_index - 3:end_index + 1], str(m.log(num)))
                        elif "ln" in func:
                            equation = equation.replace(equation[start_index - 2:end_index + 1], str(op.natlog(num)))
                        elif "sqrt" in func:
                            equation = equation.replace(equation[start_index - 4:end_index + 1], str(op.square_root(num)))
                    else:
                        equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
                else:
                    equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
            else:
                equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
        elif "^" in equation:
            op_index = equation.index("^")

            leftSide = ""
            rightSide = ""

            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                leftSide = equation[i] + leftSide
                i -= 1
            start = i
            i = op_index + 1
            while i <= len(equation) - 1 and (equation[i].isdigit() or equation[i] == '.' or equation[i] == ''):
                rightSide += equation[i]
                i += 1

            result = op.exponent(float(leftSide), float(rightSide))
            equation = str(equation[:start + 1] if start > 0 else '') + str(result) + equation[i:]
        elif "*" in equation or "/" in equation:
            mul_index = equation.find("*")
            div_index = equation.find("/")
            if mul_index == -1:
                op_index = div_index
            elif div_index == -1:
                op_index = mul_index
            else:
                op_index = min(mul_index, div_index)

            operator = equation[op_index]
            leftSide = ""
            rightSide = ""

            i = op_index - 1
            while i >= 0 and (equation[i].isdigit() or equation[i] == '.' or equation[i] == "-"):
                leftSide = equation[i] + leftSide
                i -= 1
            start = i
            i = op_index + 1
            while i <= len(equation) - 1 and (equation[i].isdigit() or equation[i] == '.' or (equation[i] == "-" and equation[i-1].isdigit() != True)):
                rightSide += equation[i]
                i += 1
            if operator == "*":
                result = op.multiplication(float(leftSide), float(rightSide))
            else:
                result = op.division(float(leftSide), float(rightSide))
            equation = str(equation[:start + 1] if start > 0 else '') + str(result) + equation[i:]
        elif "+" in equation or "-" in equation:
            add_index = equation.find("+")
            sub_index = equation.find("-")
            if add_index == -1:
                op_index = sub_index
            elif sub_index == -1:
                op_index = add_index
            elif sub_index == 0:
                op_index = add_index
            else:
                op_index = min(add_index, sub_index)
            operator = equation[op_index]
            leftSide = ""
            rightSide = ""

            i = op_index - 1
            while i >= 0 and (equation[i].isdigit() or equation[i] == "." or equation[i] == "-"):
                leftSide = equation[i] + leftSide
                i -= 1

            i = op_index + 1
            while i < len(equation) and (equation[i].isdigit() or equation[i] == "." or equation[i] == "-"):
                rightSide += equation[i]
                i += 1

            if operator == "+":
                result = op.addition(float(leftSide), float(rightSide))
            else:
                result = op.subtraction(float(leftSide), float(rightSide))

            equation = (equation[:(op_index - len(leftSide))]) + str(result) + (equation[i:])
            if equation[-2:] == ".0":
                equation = equation[:-2]

    return float(equation)

class Label(tk.Label):
    def __init__(self, **kwargs):
        global app
        super().__init__(relief='solid', **kwargs)
        self.grid(columnspan=4)

class Simple_Operations:
    @staticmethod
    def addition(number1, number2):
        return number1 + number2

    @staticmethod
    def subtraction(number1, number2):
        return number1 - number2

    @staticmethod
    def multiplication(number1, number2):
        return number1 * number2

    @staticmethod
    def division(number1, number2):
        if (number2 == 0):
            return "ERROR"
        else:
            return number1 / number2

    @staticmethod
    def exponent(number1, number2):
        return number1 ** number2

    @staticmethod
    def square_root(number1):
        return number1 ** 0.5

    @staticmethod
    def square(number1):
        return number1 ** 2

    @staticmethod
    def fact(number1):
        return np.math.factorial(number1)

    @staticmethod
    def natlog(number1):
        return np.log(number1)

    @staticmethod
    def log10(number1):
        return np.log10(number1)

    @staticmethod
    def factorial(number):
        if number == 0:
            return 1
        if number < 0 or number > 10:
            return "ERROR"
        else:
            return number * Simple_Operations.factorial(number - 1)
        
    @staticmethod
    def sin(number1):
       return np.sin(number1)
   
    @staticmethod
    def cos(number1):
        return np.cos(number1)
    
    @staticmethod
    def tan(number1):
        return np.tan(number1)

def main():
    global app
    app = App()
    app.run()

main()
