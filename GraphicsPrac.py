import tkinter as tk
import tkinter.ttk as ttk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.label_var = tk.StringVar(value="CALCULATING")
        self.box = Label(textvariable=self.label_var)
        
        self.funcs = 'c^%/789*456-123+ 0.='
        self.funcs = "0"
        for i, b in enumerate(self.funcs):
            Button(b, row = i//4+1, column = i%4)
        
    def run(self):
        self.root.mainloop()
        
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.grid(row = row, column = column)
        
    def counter(self):
        global app
        app.label_var.set("Updates")
        
class Label(tk.Label):
    def __init__(self, **kwargs):
        global app
        super().__init__(relief='solid', **kwargs)
        self.grid(columnspan = 4)



def main():
    global app
    app = App()
    app.run()

main()
