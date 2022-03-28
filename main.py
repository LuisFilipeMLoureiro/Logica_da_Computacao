import sys
import re



class Node():   

    def __init__(self, value, ListOfNodes = []):
        self.value = value
        self.children = ListOfNodes

    def Evaluate(self):
        pass

class BinOp(Node):

    def Evaluate(self):
        cria1 = self.children[0].Evaluate()
        cria2 = self.children[1].Evaluate()
        if self.value == "plus":
            result = cria1 + cria2
        elif self.value == "minus":
            result  = cria1 - cria2
        elif self.value == "mult":
            result  = cria1 * cria2
        elif self.value == "div":
            result  = int(cria1 / cria2)
        else:
            sys.stderr.write("Erro no BinOp!")
            raise ValueError

        return int(result)

class UnOp(Node):
    def Evaluate(self):
        result = self.children[0].Evaluate()

        if self.value == "minus":
            result = result * -1
        elif self.value == "plus":
            result = result

        return int(result)

class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass

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
                result = BinOp("plus", [result, Parser.parseTerm()])                
                           
                               
            if(Parser.token.actual.type == "minus"):
                Parser.token.selectNext()
                result = BinOp("minus", [result, Parser.parseTerm()])          

            
            
        return result
        




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
                result = BinOp("mult", [result, Parser.parseFactor()])
                               
                                               

            elif(Parser.token.actual.type == "div"):   
                Parser.token.selectNext()
                result = BinOp("div", [result, Parser.parseFactor()])
                    

            Parser.token.selectNext()

        return result

    @staticmethod
    def parseFactor():  

        if(Parser.token.actual.type == "int"):
            number = int(Parser.token.actual.value) 
            result = IntVal(number)
            return result

        elif(Parser.token.actual.type == "plus"):
            Parser.token.selectNext()
            return UnOp("plus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "minus"):
            Parser.token.selectNext() 
            return UnOp("minus", [Parser.parseFactor()]) ### Recursion

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
        result = Parser.parseExpression() #result é a arvore de nodes
       

        if Parser.token.actual.type != "EOF":
            sys.stderr.write("Codigo fonte não foi inteiro consumido!")
            raise ValueError
        else:
            return result.Evaluate() #retorna valor final da arvore


if ".c" in sys.argv[1]:
    with open(sys.argv[1], "r") as file:
        print(Parser.run(file.read()))
        
else:
    print("Must be a c file!")










