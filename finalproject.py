import tkinter as tk
import tkinter.ttk as ttk
import numpy as np


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)
        
        self.funcs = 'c^s%SCT)LlF/789*456-123+ 0.='
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
        if (app.label_var.get() == "0"): x = self.text + '('
        else: x = str(app.label_var.get()) + str(self.text) + '('
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
                func = equation[start_index - 4:start_index]
                if func.isalpha():
                    num = float(sub_eq)
                    if "sin" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.sin(num)))
                    elif "cos" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.cos(num)))
                    elif "tan" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.tan(num)))
                    elif "log" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.log(num)))
                    elif "ln" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.natlog(num)))
                    elif "sqrt" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.square_root(num)))
                    elif "fact" in func:
                        equation = equation.replace(equation[start_index:end_index + 1], str(op.factorial(int(num))))
                else:
                    # Process remaining part of equation
                    equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
            else:
                # Evaluate inner parentheses first
                equation = equation[:start_index] + str(calculating(sub_eq)) + equation[end_index + 1:]
        elif "^" in equation:
            op_index = equation.index("^")
            
            leftSide = ""
            rightSide = ""
            
            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                leftSide = equation[i] + leftSide
                i -= 1
            
            i = op_index + 1
            while i < len(equation) and equation[i].isdigit():
                rightSide += equation[i]
                i += 1
            
            result = op.exponent(float(leftSide), float(rightSide))
            equation = equation[:i - len(rightSide) - 1] + str(result) + equation[i:]
            
            
            
            
            
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

    