import sys
import re


#https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
class PrePro:
    @staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", "", arg)
        return new_arg

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self,origin):
        self.origin = origin #codigo fonte
        self.position = 0 #posição inicial é 0
        self.actual = self.origin[0] #inicio no primeiro token


    
    def selectNext(self):
        
        valid_tokens = [" ", "+" "-", "", "*", "/", "(", ")"]
        numero = ""
        numbers = ["1", "2", "3", "4", "5", "6","7", "8","9","0"]

        
        
        
        while(self.position <= len(self.origin) - 1):
            i = self.origin[self.position]

            if i in numbers:                
                numero += i 
                     
             
                              
            
            elif (numero != ""):
                
                self.actual = Token("int",int(numero))
                               
                         
                numero = ""
                return self.actual
           
            if(self.position == len(self.origin) - 1) & (i in numero):
               
                self.actual = Token("int",int(numero))               
                 
                self.position +=1 
                
                return self.actual

            if i == "+":                 
                self.actual = Token("plus", "+")
                self.position +=1  
                return self.actual       
              
            if i == "-":
                self.actual = Token("minus", "-")
                self.position +=1
                return self.actual   
            if i == "*":
                self.actual = Token("mult", "*")
                self.position +=1
                return self.actual  
            if i == "/":
                self.actual = Token("div", "/")
                self.position +=1
                return self.actual
            
            if i == "(":
                self.actual = Token("open_p", "(")
                self.position +=1
                return self.actual
            
            if i == ")":
                self.actual = Token("close_p", ")")
                self.position +=1
                return self.actual


            if (i in numbers) or (i  in valid_tokens):
                self.position +=1 
                
                
            else:
                sys.stderr.write("Invalid Token")
                raise ValueError
                
                
        self.actual = Token("EOF", "")
        

        return self.actual
        

class Parser:

    @staticmethod
    def parseExpression():
        
        result = Parser.parseTerm()


        while(Parser.token.actual.type == "plus" or Parser.token.actual.type == "minus"):       

            if(Parser.token.actual.type == "plus"): 
                Parser.token.selectNext()                   
                resultTerm = Parser.parseTerm()
                result += resultTerm
                           
                               
            if(Parser.token.actual.type == "minus"):
                Parser.token.selectNext()
                resultTerm = Parser.parseTerm()
                result -= resultTerm  
            
        if(Parser.token.actual.type == "EOF"):
               
            return result
            
        result = Parser.parseTerm()  #fim sempre no final da cadeia




    @staticmethod
    def parseTerm():       
        
        result = Parser.parseFactor()
        Parser.token.selectNext()


        if (type(result) == int) & (Parser.token.actual.type == "int"):
            sys.stderr.write("Faltou operador")
            raise ValueError


        while(Parser.token.actual.type == "mult" or Parser.token.actual.type == "div"):       
            if(Parser.token.actual.type == "mult"):
                Parser.token.selectNext()
                resultFactor = Parser.parseFactor()
                result *= int(resultFactor)               
                                               

            elif(Parser.token.actual.type == "div"):   
                Parser.token.selectNext()
                resultFactor = Parser.parseFactor()
                result /= resultFactor    

            Parser.token.selectNext()

        return int(result)

    @staticmethod
    def parseFactor():  
       
        if(Parser.token.actual.type == "int"):
            result = int(Parser.token.actual.value) 
            return result

        elif(Parser.token.actual.type == "plus"):
            Parser.token.selectNext()
             
            return Parser.parseFactor() ### Recursion

        elif(Parser.token.actual.type == "minus"):
            Parser.token.selectNext() 
            return Parser.parseFactor() * -1 ### Recursion

        elif(Parser.token.actual.type == "open_p"):
            Parser.token.selectNext()
            result = Parser.parseExpression()
            if(Parser.token.actual.type == "close_p"):
                return result
            else:
                sys.stderr.write("Sequencia invalida de parenteses")
                raise ValueError

        else:
            sys.stderr.write("Token invalido na posicao")
            raise ValueError


    
        

    @staticmethod
    def run(codigo_fonte):
        codigo_base = PrePro.filter(codigo_fonte)
        Parser.token = Tokenizer(codigo_base)
        Parser.token.selectNext()
        return Parser.parseExpression()
        
        
        

print(Parser.run(sys.argv[1]))









