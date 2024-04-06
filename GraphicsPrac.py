import tkinter as tk
import tkinter.ttk as ttk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.label_var = tk.StringVar(value="0")
        self.box = Label(textvariable=self.label_var)
        
        self.funcs = 'c^%/789*456-123+ 0.='
        self.buttons = {}
        for i, b in enumerate(self.funcs):
            self.buttons.update({b:Button(b, row = i//4+1, column = i%4)})
        
        self.keyBind()
        
    def run(self):
        print(self.buttons)
        self.root.mainloop()
        
    def keyBind(self):
        #keys = self.buttons.keys()
        for i in range(10):
            self.root.bind(str(i), self.key_press)
            
    def key_press(self,a):
        x = str(self.label_var.get()) + str(self.text)
        self.label_var.set(x)
        
        
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text=text, command=self.counter, **kwargs)
        self.text = text
        self.grid(row = row, column = column)
        
        
    def counter(self):
        global app
        x = str(app.label_var.get()) + str(self.text)
        app.label_var.set(x)
    '''    
    def keyBind(self):
        global app
        x = str(app.label_var.get()) + str(self.text)
  '''      
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
