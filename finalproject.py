# COMMENTS TO BE ADDED AFTER CODE STARTS WORKING
#Trig and logs still dont work

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')

        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)

        self.funcs = [('c', 'C'), ('^', '^'), ('%', '%'), ('L', ' '),
                      ('S', ' '), ('C', ' '), ('T', ' '), ('/', '/'),
                      ('7', '7'), ('8', '8'), ('9', '9'), ('*', '*'),
                      ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
                      ('1', '1'), ('2', '2'), ('3', '3'), ('+', '+'),
                      ('del', '<BackSpace>'), ('0', '0'), ('.', '.'), ('=', '<Return>')]
        
        self.buttons = {}
        for i, (b, key) in enumerate(self.funcs):
           if b == "c":
              self.buttons[b] = ClearButton(b, row=i//4+1, column=i%4)
              self.root.bind(key, self.key_press)
           elif b == 'del':
               self.buttons[b] = DelButton(b, row=i//4+1, column=i%4)
               self.root.bind(key, self.key_press)
           elif b == "=":
               self.buttons[b] = EqualsButton(b, row=i//4+1, column=i%4)
               self.root.bind(key, self.key_press)
           else:
               if b == "S":
                   x = "sin"
               elif b == "C":
                   x = "cos"
               elif b == "T":
                   x = "tan"
               elif b == "L":
                   x = "log"
               else:
                   x = b
               self.buttons[b] = Button(x, row=i//4+1, column=i%4)
               
               if(key != ' '):
                   self.root.bind(key, self.key_press)

    def run(self):
        print(self.buttons.keys())
        self.root.mainloop()
        
        
    def key_press(self, event):
        if event.keysym == 'C':
            self.label_var.set('0')
        elif event.keysym == '^':
            self.label_var.set(self.label_var.get() + '^')
        elif event.keysym == '%':
            self.label_var.set(self.label_var.get() + '%')
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
            eq = self.label_var.get()
            if eq != "0":
                if eq[-1].isalpha():
                    x = str(eq)[:-3]
                else:
                    x = str(eq)[:-1] 
            if x == "":
                x = "0"
            self.label_var.set(str(x))   
        elif event.keysym == 'Return':
            self.calculate()
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

class ClearButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)

    def counter(self):
        global app
        x = "0"
        app.label_var.set(x)

#=============================================================================


class DelButton(Button):
    def __init__(self, text, row, column):
        super().__init__(text, row, column)
    def counter(self):
       global app
       eq = app.label_var.get()
       if eq != "0":
           if eq[-1].isalpha():
               x = str(eq)[:-3]
           else:
               x = str(eq)[:-1]    
       if x == "":
           x = "0"
       app.label_var.set(str(x))   
            
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
    
    while not isFloat(equation):
        funcs = ("sin", "cos", "tan", "log")
        for func in funcs:
            if func in equation:
                start = equation.index(func)
                end = start + len(func)
                
                if equation[start - 1].isalnum():  # so you can multiply without putting * (only applies for functions)
                    equation = equation[:start] + "*" + equation[start:]

                num = ""
                i = end
                while i < len(equation) and (equation[i].isdigit() or equation[i] == '.'):
                    num += equation[i]
                    i += 1

                if func == "sin":
                    result = op.sin(float(num))
                elif func == "cos":
                    result = op.cos(float(num))
                elif func == "tan":
                    result = op.tan(float(num))
                elif func == "log":
                    result = op.log(float(num))

                equation = equation[:start] + str(result) + equation[i:]

        if "^" in equation:
            op_index = equation.index("^")

            left_side = ""
            right_side = ""

            i = op_index - 1
            while i >= 0 and equation[i].isdigit():
                left_side = equation[i] + left_side
                i -= 1
            start = i
            i = op_index + 1
            while i <= len(equation) - 1 and (equation[i].isdigit() or equation[i] == '.' or equation[i] == ''):
                right_side += equation[i]
                i += 1

            result = op.exponent(float(left_side), float(right_side))
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
            left_side = ""
            right_side = ""

            i = op_index - 1
            while i >= 0 and (equation[i].isdigit() or equation[i] == '.' or equation[i] == "-"):
                left_side = equation[i] + left_side
                i -= 1
            start = i
            i = op_index + 1
            while i <= len(equation) - 1 and (equation[i].isdigit() or equation[i] == '.' or (equation[i] == "-" and equation[i-1].isdigit() != True)):
                right_side += equation[i]
                i += 1
            if operator == "*":
                result = op.multiplication(float(left_side), float(right_side))
            else:
                result = op.division(float(left_side), float(right_side))
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
            left_side = ""
            right_side = ""

            i = op_index - 1
            while i >= 0 and (equation[i].isdigit() or equation[i] == "." or equation[i] == "-"):
                left_side = equation[i] + left_side
                i -= 1

            i = op_index + 1
            while i < len(equation) and (equation[i].isdigit() or equation[i] == "." or equation[i] == "-"):
                right_side += equation[i]
                i += 1

            if operator == "+":
                result = op.addition(float(left_side), float(right_side))
            else:
                result = op.subtraction(float(left_side), float(right_side))

            equation = (equation[:(op_index - len(left_side))]) + str(result) + (equation[i:])
            if equation[-2:] == ".0":
                equation = equation[:-2]

    return float(equation)


#=============================================================================

class Label(tk.Label):
    def __init__(self, **kwargs):
        global app
        super().__init__(relief='solid', **kwargs)
        self.grid(columnspan=4)

#=============================================================================

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
    def log(number1):
        if number1 < 0:
            return np.log10(number1)
        else: 
            return "ERROR"

        
    @staticmethod
    def sin(number1):
       try:
           ans = np.sin(number1)
           return ans
       except ValueError:
           return "ERROR"
   
    @staticmethod
    def cos(number1):
        try:
            ans = np.cos(number1)
            return ans
        except ValueError:
            return "ERROR"
    
    @staticmethod
    def tan(number1):
        try:
            ans = np.tan(number1)
            return ans
        except ValueError:
            return "ERROR"

#=============================================================================

def main():
    global app
    app = App()
    app.run()


main()
    