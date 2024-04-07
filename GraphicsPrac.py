import tkinter as tk
import tkinter.ttk as ttk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)
        
        self.funcs = [('c', 'C'), ('^', '^'), ('%', '%'), ('/', '/'),
                      ('7', '7'), ('8', '8'), ('9', '9'), ('*', '*'),
                      ('4', '4'), ('5', '5'), ('6', '6'), ('-', '-'),
                      ('1', '1'), ('2', '2'), ('3', '3'), ('+', '+'),
                      ('del', '<BackSpace>'), ('0', '0'), ('.', '.'), ('=', '<Return>')]
        
        self.buttons = {}
        for i, (btn_text, key) in enumerate(self.funcs):
            self.buttons[btn_text] = Button(btn_text, row=i//4+1, column=i%4)
            self.root.bind(key, self.key_press)
        
    def run(self):
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
        elif event.keysym == 'Return':
            self.calculate()
        else:
            self.label_var.set(self.label_var.get() + event.char)

    def calculate(self):
        try:
            result = eval(self.label_var.get())
            self.label_var.set(str(result))
        except Exception as e:
            self.label_var.set("Error")

        
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.text = text
        self.grid(row=row, column=column)
        
    def counter(self):
        global app
        x = app.label_var.get() + self.text
        app.label_var.set(x)
        

class Label(tk.Label):
    def __init__(self, **kwargs):
        super().__init__(relief='solid', **kwargs)
        self.grid(columnspan=4)

def main():
    global app
    app = App()
    app.run()

main()
