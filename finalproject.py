#Final Project
import numpy as np

class Calculator: #(for graphics)
    pass


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

class Complex_Operations(Simple_Operations):
    
    @staticmethod
    def exponent(number1,number2):
        return number1 ** number2
    
    @staticmethod
    def square(number1):
        return number1**0.5
    
    @staticmethod
    def sin(number1):
       return np.sin(number1)
   
    @staticmethod
    def cos(number1):
        return np.cos(number1)
    
    @staticmethod
    def tan(number1):
        return np.tan(number1)
    
    