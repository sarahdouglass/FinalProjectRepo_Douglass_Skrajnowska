import tkinter as tk
import tkinter.ttk as ttk
import numpy as np

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)
        
        self.funcs = 'c^%/789*456-123+ 0.='
        for i, b in enumerate(self.funcs):
            Button(b, row = i//4+1, column = i%4)
        
    def run(self):
        self.root.mainloop()
        
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.text = text
        self.grid(row = row, column = column)
        
    def counter(self):
        global app
        x = str(app.label_var.get()) + str(self.text)
        app.label_var.set(x)
        
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
        return number1 / number2

class Complex_Operations:
    
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
    