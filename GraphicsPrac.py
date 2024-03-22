import tkinter as tk
import tkinter.ttk as ttk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculator')
        
        self.box = Label("CALC")
        
        self.funcs = 'c^%/789*456-123+ 0.='
        #self.funcs = [['c','^','%','/'],[7,8,9,'*'],[4,5,6,'-'],[1,2,3,'+'],['',0,'.','=']]       
        for i, b in enumerate(self.funcs):
            Button(b, row = i//4+1, column = i%4)
        
    def run(self):
        self.root.mainloop()
        
class Button(ttk.Button):
    def __init__(self, text, row, column, **kwargs):
        super().__init__(text = text, **kwargs)
        self.grid(row = row,column = column)

        
class Label(tk.Label):
    def __init__(self, text, **kwargs):
        super().__init__(text = text, relief = 'solid', **kwargs)
        self.grid()




def main():
    calc = App()
    calc.run()
main()