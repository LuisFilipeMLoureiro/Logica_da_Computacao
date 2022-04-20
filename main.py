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

dic_SymbolTable = {}
class SymbolTable:
    @staticmethod
    def getter(chave):
        return dic_SymbolTable[chave]

    @staticmethod
    def setter(chave, valor):
        dic_SymbolTable[chave] = valor

class Assignment(Node):
    def Evaluate(self):
        cria1 = self.children[0]
        cria2 = self.children[1].Evaluate()

        SymbolTable.setter(cria1, cria2)

class Printf(Node):
    def Evaluate(self):
        cria1 = self.children.Evaluate()
        print(cria1)

class Identifier(Node):
    def Evaluate(self):
        variavel = SymbolTable.getter(self.value)
        return(variavel)


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
        
        valid_tokens = [" ", "+" "-", "", "*", "/", "(", ")", ";", "{", "}"]
        numero = ""
        numbers = ["1", "2", "3", "4", "5", "6","7", "8","9","0"]
        ReservedWords = ["printf"]
        

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

            if i == ";":
                self.actual = Token("END", ";")
                self.position +=1
                return self.actual
            if i == "{":
                self.actual = Token("open_block", "{")
                self.position +=1
                return self.actual
            
            if i == "}":
                self.actual = Token("close_block", "}")
                self.position +=1
                return self.actual

            if i == "=":
                self.actual = Token("equal", "=")
                self.position +=1
                return self.actual

            variavel = ""
            if(self.origin[self.position].isalpha()):          
                while(self.position < len(self.origin)-1) and (self.origin[self.position].isnumeric() or self.origin[self.position].isalpha() or self.origin[self.position] == "_" ):
                    variavel += self.origin[self.position]
                    self.position += 1
                if variavel in ReservedWords:
                    self.actual = Token(variavel,variavel)
                    
                else:
                    self.actual = Token("ID",variavel)
            
                return self.actual

            #if (i in numbers) or (i  in valid_tokens):
            self.position +=1 
                     
                     
                
        self.actual = Token("EOF", "")
        

        return self.actual
        

class Parser:


    @staticmethod
    def parseBlock():
        nodes = []
        if (Parser.token.actual.type != "open_block"):
            sys.stderr.write("Missing opening block {")
            raise ValueError 

        Parser.token.selectNext()
        while(Parser.token.actual.type != "close_block"):

            result = Parser.parseStatement()
            nodes.append(result)



        Parser.token.selectNext()
        return nodes


    @staticmethod
    def parseStatement():

        node = NoOp(None)
        if(Parser.token.actual.type == "ID"):
            node = Parser.token.actual.value
            Parser.token.selectNext()


            if(Parser.token.actual.type == "equal"):
                Parser.token.selectNext()
                result = Parser.parseExpression()
                node =  Assignment("equal", [node, result]) #REVER
                if("TYPE", Parser.token.actual.type == "END"):
                    Parser.token.selectNext()
                    return node
            else:
                sys.stderr.write("Missing =")
                raise ValueError
        
        elif(Parser.token.actual.type == "printf"):
            Parser.token.selectNext()

            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseExpression()

                if(Parser.token.actual.type == "close_p"):
                    node = Printf("printf", result) 
                    Parser.token.selectNext()
                    
                    if(Parser.token.actual.type == "END"):
                        Parser.token.selectNext()
                        return node
                    else:
                        sys.stderr.write("Missing closing statement ;")
                        raise ValueError
                    
                   
                else:
                    sys.stderr.write("Missing closing parenteses")
                    raise ValueError
            else:
                sys.stderr.write("Missing opening parenteses")
                raise ValueError
            
        elif(Parser.token.actual.type == "END"):
            Parser.token.selectNext()
            return node
        else:    
             
            sys.stderr.write("Missing closing token ;")
            raise ValueError      



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
        
        elif(Parser.token.actual.type == "ID"):

            result = Parser.token.actual.value
            return Identifier(result)

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
        result = Parser.parseBlock() #result é a arvore de nodes


        if Parser.token.actual.type != "EOF":
            sys.stderr.write("Codigo fonte não foi inteiro consumido!")
            raise ValueError
 
        for node in result:
            node.Evaluate() #retorna valor final da arvore


if ".c" in sys.argv[1]:
    with open(sys.argv[1], "r") as file:
        Parser.run(file.read())

        
else:
    print("Must be a c file!")








