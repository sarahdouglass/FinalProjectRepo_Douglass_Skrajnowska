#GUI Calculator created for Spring 2024 EECE 2140 Final Project

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import math as m

#define the main application class
class App:
    def __init__(self):
        self.root = tk.Tk() #initialize tkinter window
        self.root.title('Calculator')  #set window title

        #variable to hold the value displayed on the calculator
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var) #create label widget for displaying calculator value

        #define the buttons and their corresponding key bindings
        self.funcs = [('c', 'C'), ('^', '^'), ('s', 's'), ('(', '('),
                      ('S', 'S'), ('C', 'c'), ('T', 't'), (')', ')'),
                      ('L', 'L'), ('l', 'l'), ('!', '!'), ('/', '/'),
                      ('7', '7'), ('8', '8'), ('9', '9'), ('*', '*'),
                      ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
                      ('1', '1'), ('2', '2'), ('3', '3'), ('+', '+'),
                      ('d', '<BackSpace>'), ('0', '0'), ('.', '.'), ('=', '<Return>')]

        #dictionary to hold the buttons
        self.buttons = {}

        #create buttons and bind key
        for i, (b, key) in enumerate(self.funcs):
            if b == "c":
                self.buttons[b] = ClearButton(row=i // 4 + 1, column=i % 4)  #create clearing button instance
                self.root.bind(key, self.key_press)  #bind C key to key_press method
            elif b == 'd':
                self.buttons[b] = DelButton(row=i // 4 + 1, column=i % 4)  #create delete button instance
                self.root.bind(key, self.key_press)  #bind BackSpace key to key_press method
            elif b == "=":
                self.buttons[b] = EqualsButton(b, row=i // 4 + 1, column=i % 4)  #create equals button instance
                self.root.bind(key, self.key_press)  #bind = key to key_press method
            elif b.isalpha() == False:
                self.buttons[b] = Button(b, row=i // 4 + 1, column=i % 4)  #create not alphabetical key instances
                self.root.bind(key, self.key_press)  #bind respective key to key_press method
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
                self.buttons[b] = FuncButton(x, row=i // 4 + 1, column=i % 4)  #create function button instance
                if key != ' ':
                    self.root.bind(key, self.key_press)  #bind respective key to key_press method

    #run the application
    def run(self):
        self.root.mainloop()

    #method to set new value to the label_var
    def setNew(self, key):
        if self.label_var.get() == '0':
            self.label_var.set(key)
        else:
            self.label_var.set(self.label_var.get() + key)

    #handle key press events
    def key_press(self, event):
        if event.char == 'C':
            self.label_var.set('0')
            app.box.config(fg="black")
        elif event.char == 'c':
            self.setNew("cos(")
        elif event.char == 'S':
            self.setNew("sin(")
        elif event.char == 's':
            self.setNew("sqrt(")
        elif event.char == 't':
            self.setNew("tan(")
        elif event.char == 'l':
            self.setNew("log(")
        elif event.char == 'L':
            self.setNew("ln(")
        elif event.keysym == '.':
            self.label_var.set(self.label_var.get() + '.')
        elif event.keysym == 'Space':
            self.label_var.set(self.label_var.get() + ' ')
        elif event.keysym == 'BackSpace':
            if app.label_var.get() != "0":
                x = str(app.label_var.get())[:-1]
                app.label_var.set(x)
                app.box.config(fg="black")
        elif event.keysym == 'Return':
            app.label_var.set(calculating(app.label_var.get()))
        else:
            self.setNew(event.char)


# =============================================================================

#button class inheriting the button class from the ttk library
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.text = text
        self.grid(row=row, column=column)
        
    #counter method to handle button clicks
    def counter(self):
        global app
        if app.label_var.get() == "0":
            x = self.text
        else:
            x = str(app.label_var.get()) + str(self.text)
        app.label_var.set(x)


# =============================================================================

class FuncButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)

    #override counter method for function buttons
    def counter(self):
        global app
        if app.label_var.get() == "0":
            x = self.text + "("
        else:
            x = str(app.label_var.get()) + str(self.text) + "("
        app.label_var.set(x)


# =============================================================================

class ClearButton(Button):
    def __init__(self, row, column):
        text = "clear"
        super().__init__(text, row, column)
        
    #override counter method for clear button
    def counter(self):
        global app
        x = "0"
        app.label_var.set(x)
        app.box.config(fg="black")

# =============================================================================

class DelButton(Button):
    def __init__(self, row, column):
        text = "del"
        super().__init__(text, row, column)
        
    #override counter method for delete button
    def counter(self):
        global app
        if app.label_var.get() == "0":
            x = app.label_var.get()
        else:
            x = str(app.label_var.get())[:-1]
            app.label_var.set(x)
            app.box.config(fg="black")

# =============================================================================

class EqualsButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)

    #override counter method for equals button
    def counter(self):
        global app
        app.label_var.set(calculating(app.label_var.get()))


# =============================================================================

def isFloat(equation):
    try:
        float(equation)
        return True
    except ValueError:
        return False


# =============================================================================

def calculating(equation):
    #create an instance of the Simple_Operations class to perform operations
    op = Simple_Operations()
    i = 0

    #iterate until the equation is converted to a float number
    while not isFloat(equation):

        #check if there are parentheses in the equation
        if "(" in equation:
            try:
                #index the opening and closing parentheses
                start_index = equation.index("(")
                end_index = start_index + equation[start_index:].index(")")
                #extract the expression within the parentheses and evaluate it with recursion
                sub_eq = calculating(equation[start_index + 1:end_index])
                #check if the expression is a float number
                if isFloat(sub_eq):
                    #determine the function before the opening parenthesis
                    if start_index - 4 < 0:
                        start = 0
                    else:
                        start = start_index - 4
                    func = equation[start:start_index]
                    #handle functions like sin, cos, tan
                    if len(func) > 1:
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
                                equation = equation.replace(equation[start_index - 4:end_index + 1],
                                                            str(op.square_root(num)))
                        else:
                            equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
                    else:
                        equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
                else:
                    equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
            #handle exceptions
            except Exception:
                app.label_var.set("ERROR: SYNTAX")
                app.box.config(fg="red")
                break
        #handle factorial operation in the equation
        elif "!" in equation:
            op_index = equation.index("!")
            leftSide = ""
            i = op_index - 1
            #extract the left side of the factorial operation
            while i >= 0 and (equation[i].isdigit() or equation[i] == '.' or equation[i] == '-'):
                leftSide = equation[i] + leftSide
                i -= 1
            #calculate the factorial of the left side
            result = op.factorial(float(leftSide))
            #check for errors, negative numbers in the factorial
            if result == 'ERROR':
                app.label_var.set("ERROR")
                app.box.config(fg="red")
                break
            #replace the factorial operation with the result
            equation = str(equation[:op_index - len(leftSide)]) + str(result) + equation[op_index + 1:]
        #handle exponent
        elif "^" in equation:
            op_index = equation.index("^")
            leftSide = ""
            rightSide = ""
            i = op_index - 1
            #extract the left side of the exponent op
            while i >= 0 and (equation[i].isdigit() or equation[i] == '.'):
                leftSide = equation[i] + leftSide
                i -= 1
            start = i + 1
            i = op_index + 1
            #extract the right side of the exponent op
            while i <= len(equation) - 1 and (equation[i].isdigit() or equation[i] == '.' or equation[i] == '' or (equation[i] == "-" and equation[i+1].isdigit() and '-' in rightSide == False)):
                rightSide += equation[i]
                i += 1
            #calculate the result of exponent
            result = op.exponent(float(leftSide), float(rightSide))
            #replace the exponent operation with the result
            equation = str(equation[:start] if start > 0 else '') + str(result) + equation[i:]
        #handle multiplication or division
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
            #extract the left side of the multiplication or division operation
            while i >= 0 and (equation[i].isdigit() or equation[i] == '.' or (equation[i] == "-" and equation[i - 1].isdigit() != True)):
                leftSide = equation[i] + leftSide
                i -= 1
            start = i + 1
            i = op_index + 1
            #extract the right side of the multiplication or division operation
            while i <= len(equation) - 1 and (equation[i].isdigit() or equation[i] == '.' or (equation[i] == "-" and equation[i - 1].isdigit() != True)):
                rightSide += equation[i]
                i += 1
            #perform multiplication or division and replace the operation with the result
            if operator == "*":
                result = op.multiplication(float(leftSide), float(rightSide))
            else:
                if rightSide == '0':
                    app.label_var.set("ERROR")
                    app.box.config(fg="red")
                    break
                else:
                    result = op.division(float(leftSide), float(rightSide))
            equation = str(equation[:start] if start > 0 else '') + str(result) + equation[i:]
        #handle addition and subtraction
        elif "+" in equation or "-" in equation:
            add_index = equation.find("+")
            sub_index = equation.find("-")
            if add_index == -1:
                op_index = sub_index
            elif sub_index == -1:
                op_index = add_index
            elif sub_index == 0:
                op_index = add_index
            elif sub_index - 1 == '':
                sub_eq = equation[sub_index + 1:]
                sub_index = equation.find("-")
                op_index = min(add_index, sub_index)
            else:
                op_index = min(add_index, sub_index)
            operator = equation[op_index]
            leftSide = ""
            rightSide = ""

            i = op_index - 1
            #extract the left side of the addition or subtraction operation
            while i >= 0 and (equation[i].isdigit() or equation[i] == "." or (equation[i] == "-" and equation[i-1].isdigit() == False)):
                leftSide = equation[i] + leftSide
                i -= 1

            i = op_index + 1
            #extract the right side of the addition or subtraction operation
            while i < len(equation) and (equation[i].isdigit() or equation[i] == "." or (equation[i] == "-" and equation[i-1].isdigit() == False)):
                rightSide += equation[i]
                i += 1

            #perform addition or subtraction and replace the operation with the result
            if operator == "+":
                result = op.addition(float(leftSide), float(rightSide))
            else:
                result = op.subtraction(float(leftSide), float(rightSide))

            equation = (equation[:(op_index - len(leftSide))]) + str(result) + (equation[i:])
            #remove trailing .0 if present (caused issues earlier on)
            if equation[-2:] == ".0":
                equation = equation[:-2]

    #convert the final result to a float number and return it
    return float(equation)


# =============================================================================

class Label(tk.Label):
    def __init__(self, **kwargs):
        #call the constructor of the parent class tk.Label
        super().__init__(relief='solid', **kwargs)
        #position the label widget to span across all columns in the grid
        self.grid(columnspan=4)


# =============================================================================

#simple operations within a class so they can be called easily
class Simple_Operations:
    
    @staticmethod #static methods as they don't change instances within the class
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


# =============================================================================

#call the main application class and call main to run calculator
def main():
    global app
    app = App()
    app.run()


main()