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

        elif self.value == "doubleEqual":
            result = (cria1 == cria2)

        elif self.value == "and":
            result = (cria1 and cria2)

        elif self.value == "above":
            result = (cria1 > cria2)

        elif self.value == "below":
            result = (cria1 < cria2)

        elif self.value == "or":
            result = (cria1 or cria2)
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
        elif self.value == "not":
            result = not(result)



        return int(result)

class WHILE(Node):
    def Evaluate(self):
        while self.children[0].Evaluate():
            self.children[1].Evaluate()

class SCANF(Node):
    def Evaluate(self):
        resultado =  int(input())
        return resultado

class IF(Node):
    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()

        elif len(self.children) > 2:
            self.children[2].Evaluate()


class Block(Node):
    def Evaluate(self):
        for n in self.children:
            n.Evaluate()

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
        
    
        numero = ""
        numbers = ["1", "2", "3", "4", "5", "6","7", "8","9","0"]
        ReservedWords = ["printf", "scanf", "if", "while"]
        
    # pula os espcos em branco e \n com while
    # começa os ifs
    #erro eh para dar no parser
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

            if i == ">":
                self.actual = Token("above", ">")
                self.position +=1
                return self.actual

            if i == "<":
                self.actual = Token("below", "<")
                self.position +=1
                return self.actual

            if i == "!":
                self.actual = Token("not", "!")
                self.position +=1
                return self.actual

            if i == "&":
                self.position +=1
                if self.origin[self.position] == "&":
                    self.actual = Token("and", "&&")
                    self.position +=1

                else:
                    sys.stderr.write("Missing & in AND operator")
                    raise ValueError 
                return self.actual


            if i == "|":
                self.position +=1
                if self.origin[self.position] == "|":
                    self.actual = Token("or", "||")
                    self.position +=1

                else:
                    sys.stderr.write("Missing | in OR operator")
                    raise ValueError 
                return self.actual

            if i == "=":
                self.position +=1
                if self.origin[self.position] == "=":
                    self.actual = Token("doubleEqual", "==")
                    self.position +=1
                else:
                    self.actual = Token("equal", "=") 

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
        return Block("", nodes)


    @staticmethod
    def parseStatement():

        node = NoOp(None)

        if(Parser.token.actual.type == "END"):
            Parser.token.selectNext()
            return node


        if(Parser.token.actual.type == "ID"):
            node = Parser.token.actual.value
            Parser.token.selectNext()


            if(Parser.token.actual.type == "equal"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()
                node =  Assignment("equal", [node, result]) 
                if(Parser.token.actual.type == "END"):
                    Parser.token.selectNext()
                    return node
                else: 
                    sys.stderr.write("Missing closing token ;")
                    raise ValueError  
            else:
                sys.stderr.write("Missing =")
                raise ValueError
        
        elif(Parser.token.actual.type == "printf"):

            Parser.token.selectNext()

            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()

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

        elif(Parser.token.actual.type == "while"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()
                
                
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()                  
                    result2 = Parser.parseStatement()
                    node = WHILE("", [result, result2])
                    return node
                    

                else:
                    sys.stderr.write("Missing closing parenteses in while")
                    raise ValueError


            else:
                sys.stderr.write("Missing opening parenteses in while")
                raise ValueError


        elif(Parser.token.actual.type == "if"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                result = Parser.parseRelExpression()


                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    result2 = Parser.parseStatement()      

                    if(Parser.token.actual.type == "else"):
                        Parser.token.selectNext()
                        result3 = Parser.parseStatement()
                        node = IF("",[result, result2, result3])
                        return node
                        
                    else:                        
                        node = IF("",[result, result2])
                        return node


                else:
                    sys.stderr.write("Missing opening parenteses in if")
                    raise ValueError

            else:
                sys.stderr.write("Missing opening parenteses in if")
                raise ValueError

        else:
            node = Parser.parseBlock()
            return node

    @staticmethod
    def parseRelExpression():

        result = Parser.parseExpression()

        while(Parser.token.actual.type == "doubleEqual" or Parser.token.actual.type == "above" or Parser.token.actual.type == "below"):   
            
            if(Parser.token.actual.type == "doubleEqual"):
                Parser.token.selectNext()
                result = BinOp("doubleEqual", [result, Parser.parseExpression()]) 

            if(Parser.token.actual.type == "above"):
                Parser.token.selectNext()
                result = BinOp("above", [result, Parser.parseExpression()]) 

            if(Parser.token.actual.type == "below"):
                Parser.token.selectNext()
                result = BinOp("below", [result, Parser.parseExpression()]) 

        return result
        

    @staticmethod
    def parseExpression():
        
        result = Parser.parseTerm()


        while(Parser.token.actual.type == "plus" or Parser.token.actual.type == "minus" or Parser.token.actual.type == "or" ):       

            if(Parser.token.actual.type == "plus"): 
                Parser.token.selectNext()                   
                result = BinOp("plus", [result, Parser.parseTerm()])                
                           
                               
            if(Parser.token.actual.type == "minus"):
                Parser.token.selectNext()
                result = BinOp("minus", [result, Parser.parseTerm()])

            if(Parser.token.actual.type == "or"):
                Parser.token.selectNext()
                result = BinOp("or", [result, Parser.parseTerm()])            

            
            
        return result
        




    @staticmethod
    def parseTerm():       
        
        result = Parser.parseFactor()
        #Parser.token.selectNext()
    

        if (type(result) == int) & (Parser.token.actual.type == "int"):
            sys.stderr.write("Faltou operador")
            raise ValueError


        while(Parser.token.actual.type == "mult" or Parser.token.actual.type == "div" or Parser.token.actual.type == "and"):
            if(Parser.token.actual.type == "mult"):
                Parser.token.selectNext()
                result = BinOp("mult", [result, Parser.parseFactor()])
                               
                                               

            elif(Parser.token.actual.type == "div"):   
                Parser.token.selectNext()
                result = BinOp("div", [result, Parser.parseFactor()])


            elif(Parser.token.actual.type == "and"):   
                Parser.token.selectNext()
                result = BinOp("and", [result, Parser.parseFactor()])
                    

            #Parser.token.selectNext()
        return result

    @staticmethod
    def parseFactor():  

        if(Parser.token.actual.type == "int"):
            number = int(Parser.token.actual.value) 
            result = IntVal(number)
            Parser.token.selectNext()
            return result
        
        elif(Parser.token.actual.type == "ID"):
            result = Parser.token.actual.value
            Parser.token.selectNext()
            return Identifier(result)

        elif(Parser.token.actual.type == "plus"):
            Parser.token.selectNext()
            return UnOp("plus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "minus"):
            Parser.token.selectNext() 
            return UnOp("minus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "diff"):
            Parser.token.selectNext() 
            return UnOp("not", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "open_p"):
            Parser.token.selectNext()
            result = Parser.parseRelExpression()
            if(Parser.token.actual.type == "close_p"):
                Parser.token.selectNext()
                return result
            else:
                sys.stderr.write("Sequencia invalida de parenteses")
                raise ValueError


        elif(Parser.token.actual.type == "scanf"):
            if(Parser.token.actual.type == "open_p"):
                node = SCANF()
                Parser.token.selectNext()
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    return node
                else:
                    sys.stderr.write("Missing closing parenteses in scanf")
                    raise ValueError
                

            else:
                sys.stderr.write("Missing opening parenteses in scanf")
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
            
 
        else:
            return result
            

if ".c" in sys.argv[1]:
    with open(sys.argv[1], "r") as file:
        result = Parser.run(file.read())
        result.Evaluate()

        
else:
    sys.stderr.write("Must be a .c file!")
    raise ValueError








