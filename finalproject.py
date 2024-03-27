import tkinter as tk
import tkinter.ttk as ttk
import numpy as np


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)
        
        self.funcs = 'c ^s%SCTLlF/789*456-123+ 0.='
        for i, b in enumerate(self.funcs):            
            if b == "c": ClearButton(b, row = i//4+1, column = i%4)
            elif b.isalpha(): 
                if b == "S": x = "sin"
                elif b == "C": x = "cos"
                elif b == "T": x = "tan"
                elif b == "s" : x = "sqrt"
                elif b == "l": x = "ln"
                elif b == "F": x = "fact"
                elif b == "L": x = "log"
                FuncButton(x, row = i//4+1, column = i%4)
            elif b == "=": EqualsButton(b, row = i//4+1, column = i%4)
            
            else: Button(b, row = i//4+1, column = i%4)
                    
    def run(self):
        self.root.mainloop()
        
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.text = text
        self.grid(row = row, column = column)
        
    def counter(self):
        global app
        if (app.label_var.get() == "0"): x = self.text
        else: x = str(app.label_var.get()) + str(self.text)
        app.label_var.set(x)

class ClearButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)
    def counter(self):
        global app
        x = "0"
        app.label_var.set(x)
        
class FuncButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)
    def counter(self):
        global app
        if (app.label_var.get() == "0"): x = self.text
        else: x = str(app.label_var.get()) + str(self.text) + "("
        app.label_var.set(x)
        
class EqualsButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)
    def counter(self):
        global app
        x = "ANS"
        app.label_var.set(x)

def isFloat(equation):
    try: 
        float(equation)
        return True
    except ValueError: 
        return False
    
def calculating(equation):
    op = Simple_Operations()
    
    while not isFloat(equation):
        if "(" in equation:
            start_index = equation.index("(")
            end_index = start_index + equation[start_index:].index(")")
            sub_eq = equation[start_index + 1:end_index]

            if isFloat(sub_eq):
                # Evaluate functions
                func = equation[start_index - 3:start_index]
                if func.isalpha():
                    num = float(sub_eq)
                    if func == "sin":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.sin(num)))
                    elif func == "cos":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.cos(num)))
                    elif func == "tan":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.tan(num)))
                    elif func == "log":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.log(num)))
                    elif func == "log":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.log(num)))
                    elif func == "sqrt":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.square_root(num)))
                    elif func == "fact":
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.factorial(int(num))))
                else:
                    # Process remaining part of equation
                    equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]

            else:
                # Evaluate inner parentheses first
                equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]

        elif "^" in equation:
            op_index = equation.index("^")
            
            left_operand = ""
            right_operand = ""
            
            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                left_operand = equation[i] + left_operand
                i -= 1
            
            i = op_index + 1
            while i < len(equation) and equation[i].isdigit():
                right_operand += equation[i]
                i += 1
            
            result = op.exponent(float(left_operand), float(right_operand))
            equation = equation[:i - len(right_operand) - 1] + str(result) + equation[i:]

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
            left_operand = ""
            right_operand = ""
            
            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                left_operand = equation[i] + left_operand
                i -= 1
            
            i = op_index + 1
            while i < len(equation) and equation[i].isdigit():
                right_operand += equation[i]
                i += 1
            
            if operator == "*":
                result = op.multiplication(float(left_operand), float(right_operand))
            else: 
                result = op.division(float(left_operand), float(right_operand))
                
            equation = equation[:i - len(right_operand) - 1] + str(result) + equation[i:]

        elif "+" in equation or "-" in equation:
            add_index = equation.find("+")
            sub_index = equation.find("-")
            if add_index == -1:
                op_index = sub_index
            elif sub_index == -1:
                op_index = add_index
            else:
                op_index = min(add_index, sub_index)

            operator = equation[op_index]
            left_operand = ""
            right_operand = ""
            # Get left operand
            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                left_operand = equation[i] + left_operand
                i -= 1
            # Get right operand
            i = op_index + 1
            while i < len(equation) and equation[i].isdigit():
                right_operand += equation[i]
                i += 1
            # Perform addition or subtraction
            if operator == "+":
                result = op.addition(float(left_operand), float(right_operand))
            else:  # operator == "-"
                result = op.subtraction(float(left_operand), float(right_operand))
            equation = equation[:i - len(right_operand) - 1] + str(result) + equation[i:]

    return float(equation)
        
        
        
class Label(tk.Label):
    def __init__(self, **kwargs):
        global app
        super().__init__(relief='solid', **kwargs)
        self.grid(columnspan = 4)



class Simple_Operations:
    @staticmethod
    def addition(number1,number2):
        return number1 + number2
    @staticmethod
    def subtraction(number1,number2):
        return number1 - number2
    @staticmethod
    def multiplication(number1,number2):
        return number1 * number2
    @staticmethod
    def division(number1,number2):
        if(number2 == 0): return "ERROR"
        else: return number1 / number2
    @staticmethod
    def exponent(number1,number2):
        return number1 ** number2
    
    @staticmethod
    def square_root(number1):
        return number1**0.5
    
    @staticmethod
    def square(number1):
        return number1**2
    
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
        else:
            return number * Simple_Operations.factorial(number - 1)
    

def main():
    global app
    app = App()
    app.run()
main()

    