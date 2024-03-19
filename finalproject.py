#Final Project

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
   def trig