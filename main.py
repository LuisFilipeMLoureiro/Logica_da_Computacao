import sys
import re

#parte mais dificil: evaluate do funccall

class Node():   

    def __init__(self, value, ListOfNodes = []):
        self.value = value
        self.children = ListOfNodes

    def Evaluate(self, st):
        pass

class BinOp(Node):

    def Evaluate(self,st):

        cria1 = self.children[0].Evaluate(st)
        cria2 = self.children[1].Evaluate(st)

        if (cria1[1] == "int") and (cria2[1] == "int"):
            if self.value == "plus":
                
                result = cria1[0] + cria2[0]

            elif self.value == "minus":
                result  = cria1[0] - cria2[0]

            elif self.value == "mult":
                result  = cria1[0] * cria2[0]

            elif self.value == "div":
                result  = int(cria1[0] / cria2[0])

            elif self.value == "doubleEqual":
                result = (cria1[0] == cria2[0])

            elif self.value == "and":
                result = (cria1[0] and cria2[0])

            elif self.value == "above":
                result = (cria1[0] > cria2[0])

            elif self.value == "below":
                result = (cria1[0] < cria2[0])

            elif self.value == "or":
                result = (cria1[0] or cria2[0])

            elif self.value == "concat":
                result = str(cria1[0]) + str(cria2[0])
                return (str(result), "str")
            else:
                sys.stderr.write("Invalid operation with integer in BinOp!")
                raise ValueError

            return (int(result), "int")

        elif (cria1[1] == "str") and (cria2[1] == "str"):
            if self.value == "concat":
                result = str(cria1[0]) + str(cria2[0])
                return (str(result), "str")

            if self.value == "doubleEqual":
                result = str(cria1[0]) == str(cria2[0])
                return (int(result), "int")
            elif self.value == "above":
                result = (str(cria1[0]) > str(cria2[0]))
                return (int(result), "int")
            elif self.value == "below":
                result = (str(cria1[0]) < str(cria2[0]))
                return (int(result), "int")

            else:
                sys.stderr.write("Invalid operation with string in BinOp!")
                raise ValueError
        
        elif (cria1[1] == "str") or (cria2[1] == "str"):
            if self.value == "concat":
                result = str(cria1[0]) + str(cria2[0])
                return (str(result), "str")

            else:
                sys.stderr.write("Invalid operation with string and int in BinOp!")
                raise ValueError



class UnOp(Node):
    def Evaluate(self, st):
        result = self.children[0].Evaluate(st)

         
        if result[1] == "int":
            if self.value == "minus":
                output = result[0] * -1
            elif self.value == "plus":
                output = result[0]
            elif self.value == "not":
                output = not(result[0])
        else:
            sys.stderr.write("Must be a int to be operated!")
            raise ValueError




        return (int(output), "int")

class WHILE(Node):
    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)

class SCANF(Node):
    def Evaluate(self, st):
        resultado =  int(input())
        return (resultado, "int")

class IF(Node):
    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)

        elif len(self.children) > 2:
            self.children[2].Evaluate(st)

#CHECAR
class Block(Node):
    def Evaluate(self, st):
        for n in self.children:
            n.Evaluate(st)

class IntVal(Node):
    def Evaluate(self, st):
        return (self.value, "int")

class NoOp(Node):
    def Evaluate(self, st):
        pass


# OK
dic_FuncTable = {}
class FuncTable:

    @staticmethod
    def create(nome, value, tipo): #evaluate do funcdec

        if nome in dic_FuncTable:
            sys.stderr.write("Invalid casting or more than one declaration of a function")
            raise ValueError 
        else:
            dic_FuncTable[nome] = [value, tipo]
        
        

    @staticmethod
    def getter(chave):
        return dic_FuncTable[chave]



class SymbolTable:
    def __init__(self):
        self.SymbolTable = {}
    
    def create(self,nome, tipo):
        if nome in self.SymbolTable.keys():
            sys.stderr.write("Invalid casting or more than one declaration of a variable")
            raise ValueError 
        else:
            self.SymbolTable[nome] = [None, tipo]
   
    def getter(self,chave):
        return  self.SymbolTable[chave]       

    def setter(self,nome, valor):
        if nome in self.SymbolTable.keys():
            if valor[1] == self.SymbolTable.keys()[nome][1]:
                self.SymbolTable.keys()[nome] = [valor[0], valor[1]]

            else:
                sys.stderr.write("Invalid association")
                raise ValueError 
        else:
            sys.stderr.write("Variable not declared")
            raise ValueError 


# ok
class FuncDec(Node):
    def Evaluate(self, st):
        vardec = self.children[0]
        neto = vardec.children
        FuncTable.create(neto, self, vardec.value)


#!Duvida!como explorar o FuncDec
class FuncCall(Node):
    def Evaluate(self, st):
        funcName = self.value
        funcdec, tipo = FuncTable.getter(funcName)
        current_st = SymbolTable()
        args = []
        

        if (len(funcdec.children)-2) == len(self.children):            
            for i in range(1,len(funcdec.children)-2):
                vardec = self.children[i]
                neto = vardec.children[i].value
                
                current_st.create(neto, vardec.value)
                current_st.setter(neto, self.children[i-1].Evaluate(st))

            nodeBlock = current_st[-1].evaluate(current_st)
            if Return[1] == vardec.children[0].value:
                return nodeBlock
            else:
                sys.stderr.write("Missing return in function")
                raise ValueError      

                
            
             #rever o que deve ser retornado
        else:
            sys.stderr.write("Inconsistent number of arguments in function")
            raise ValueError      

            #if arg == "return": return algo nessa linha
            
#REVISAR ESSE RETURN
class Return(Node):
    def Evaluate(self, st):
        
        return self.children.Evaluate(st)
        


class Assignment(Node):
    def Evaluate(self, st):
        cria1 = self.children[0]
        cria2 = self.children[1].Evaluate(st)
        

        SymbolTable.setter(cria1, cria2)

class Printf(Node):
    def Evaluate(self, st):
        cria1 = self.children.Evaluate(st)
        print(cria1[0])

class Identifier(Node):
    def Evaluate(self, st):
        variavel = SymbolTable.getter(self.value)
        return(variavel[0],variavel[1])

class Strval(Node):
    def Evaluate(self, st):
        return(self.value, "str")

class Vardec(Node):
    def Evaluate(self, st):
        _value = self.value
        for ident in self.children:
            SymbolTable.create(st, ident.value, _value)

            
        


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
        ReservedWords = ["printf", "scanf", "if", "while", "else", "int", "str", "return", "void"]
        
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

            if i == ".":
                self.actual = Token("concat", ".")
                self.position +=1
                return self.actual
            if i == ",":
                self.actual = Token("comma", ",")
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
            if "\"" == i:
                self.position += 1
                while self.origin[self.position] != ("\""):
                    variavel += self.origin[self.position]
                    self.position += 1
                
                self.position += 1
                self.actual = Token("str",variavel)
                return self.actual

            if(self.origin[self.position].isalpha()):          
                while(self.position < len(self.origin)-1) and (self.origin[self.position].isnumeric() or self.origin[self.position].isalpha() or self.origin[self.position] == "_" ):
                    variavel += self.origin[self.position]
                    self.position += 1
                if variavel in ReservedWords:
                    if variavel == "str":
                        self.actual = Token("type","str")
                    elif variavel == "int":
                        self.actual = Token("type","int")
                    elif variavel == "void":
                        self.actual = Token("type","void")
                    else:
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
    def parseDeclaration():
        
        filhos = []
        
        if(Parser.token.actual.type == "type"):
            funcType = Parser.token.actual.value
            Parser.token.selectNext()
            if(Parser.token.actual.type == "ID"):
                funcID = Parser.token.actual.value
                arg0 = Vardec(funcType, funcID)
                filhos.append(arg0)
                Parser.token.selectNext()

                if(Parser.token.actual.type == "open_p"):
                    Parser.token.selectNext()

                    if(Parser.token.actual.type == "close_p"):
                        Parser.token.selectNext()
            
                        result = Parser.parseBlock()

                    # !Duvida! Nao entendi o que devo fazer com a lista de argumentos
                    else:
                        
                        while(Parser.token.actual.type != "close_p"):
                            print("aqui")
                            if(Parser.token.actual.type == "type"):
                                typevar = Parser.token.actual.value
                                Parser.token.selectNext()                                
                                if(Parser.token.actual.type == "ID"):
                                    nomevar = Parser.token.actual.value
                                    filhos.append(Vardec(typevar, nomevar))
                                    Parser.token.selectNext()                                   
                                

                                if(Parser.token.actual.type == "close_p"):
                                    break
                                if(Parser.token.actual.type == "comma"):
                                    Parser.token.selectNext()
                                    if(Parser.token.actual.type == "close_p"):
                                        sys.stderr.write("Extra comma in function declaration")
                                        raise ValueError
                            else:
                                sys.stderr.write("Missing type of argument in function")
                                raise ValueError
                        
                        #DUVIDA: como fazer o block para carregar todo o conteudo da funcao
                        
                        Parser.token.selectNext()
                        print("saindo", Parser.token.actual.value)
                        block = Parser.parseBlock() 
                        filhos.append(block)
                        
                        result = FuncDec(nomevar, filhos)
                        return result


                else:
                    sys.stderr.write("Missing open parentheses in function")
                    raise ValueError 

            else:
                sys.stderr.write("Missing function name")
                raise ValueError 
        else:
            sys.stderr.write("Missinga functiona at the start")
            raise ValueError 
        

    # !Duvida! Verificar o parseProgram
    @staticmethod
    def parseProgram(): #while no EOF
        nodes = []
        while(Parser.token.actual.type != "EOF"):
            
            nodes.append(Parser.parseDeclaration())

        
            
        return Block("Block", nodes)

    @staticmethod #ok
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
            result = Parser.token.actual.value
            argumentos = []
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                print("pre", Parser.token.actual.value)
                Parser.token.selectNext()
                print("pos", Parser.token.actual.value)
                argumentos.append(Parser.parseRelExpression())
                Parser.token.selectNext()
                
                while(Parser.token.actual.type == "comma"):
                    Parser.token.selectNext()
                    argumentos.append(Parser.parseRelExpression())
                if(Parser.token.actual.type == "close_p"):
                    Parser.token.selectNext()
                    return FuncCall(result, argumentos)
                else:
                    sys.stderr.write("Missing opening parenteses in statement")
                    raise ValueError 


            elif(Parser.token.actual.type == "equal"):
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
        elif(Parser.token.actual.type == "type"):

            if (Parser.token.actual.value) == "int":
                result = Vardec("int", [])
                
            elif(Parser.token.actual.value) == "str":
                result = Vardec("str", [])
                
            
            Parser.token.selectNext()
            #if type == id else error
            variavel = Parser.token.actual.value
            result.children.append(Identifier(variavel))
            Parser.token.selectNext()
           

            while Parser.token.actual.type == "comma":
                Parser.token.selectNext()
                #if type == id else error
                variavel = Parser.token.actual.value
                result.children.append(Identifier(variavel))
                Parser.token.selectNext()
            
            #testar se é ponto e virgula else error
            Parser.token.selectNext()

            return result

        elif(Parser.token.actual.type == "return"):
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                result = Parser.parseRelExpression()
                if(Parser.token.actual.type == "close_p"):
                    return result                    

                else:
                    sys.stderr.write("Missing closing parenteses in return")
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


        while(Parser.token.actual.type == "plus" or Parser.token.actual.type == "minus" or Parser.token.actual.type == "or" or Parser.token.actual.type == "concat" ):       

            if(Parser.token.actual.type == "plus"): 
                Parser.token.selectNext()                   
                result = BinOp("plus", [result, Parser.parseTerm()])                
                           
                               
            if(Parser.token.actual.type == "minus"):
                Parser.token.selectNext()
                result = BinOp("minus", [result, Parser.parseTerm()])

            if(Parser.token.actual.type == "or"):
                Parser.token.selectNext()
                result = BinOp("or", [result, Parser.parseTerm()])
            if(Parser.token.actual.type == "concat"):
                Parser.token.selectNext()
                result = BinOp("concat", [result, Parser.parseTerm()])  

            
            
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

        if(Parser.token.actual.type == "str"):
            number = Parser.token.actual.value
            result = Strval(number)
            Parser.token.selectNext()
            return result

        # !Duvida! verificar esse ponto com o RelExpr e o while        
        elif(Parser.token.actual.type == "ID"):
            result = Parser.token.actual.value
            Parser.token.selectNext()

            if(Parser.token.actual.type == "open_p"):
                Parser.token.selectNext()
                argumentos = []
                argumentos.append(Parser.parseRelExpression())
                while(Parser.token.actual.type == "comma"):
                    Parser.token.selectNext()
                    argumentos.append(Parser.parseRelExpression())
                if(Parser.token.actual.type == "close_p"):
                    return FuncCall(result, argumentos)
                else:
                    sys.stderr.write("Missing opening parenteses in factor")
                    raise ValueError               
            
            else:           

                return Identifier(result)

        elif(Parser.token.actual.type == "plus"):
            Parser.token.selectNext()
            return UnOp("plus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "minus"):
            Parser.token.selectNext() 
            return UnOp("minus", [Parser.parseFactor()]) ### Recursion

        elif(Parser.token.actual.type == "not"):
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
            Parser.token.selectNext()
            if(Parser.token.actual.type == "open_p"):
                node = SCANF(Node)
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
  
    # !Duvida! como deve ser o Run? Quem deve ser chamado agora nao eh mais o parseBlock. É o parse.Program?
    @staticmethod
    def run(codigo_fonte):
        codigo_base = PrePro.filter(codigo_fonte)
        Parser.token = Tokenizer(codigo_base)
        Parser.token.selectNext() 
        print(Parser.token.actual.value)    
        
        result = Parser.parseProgram() #result é a arvore de nodes


        if Parser.token.actual.type != "EOF":
            sys.stderr.write("Codigo fonte não foi inteiro consumido!")
            raise ValueError
            
 
        else:
            
            return result
          
# !Duvida![1] - esta certo isso? criar um ditionary fora para o evaluate


if ".c" in sys.argv[1]:
    with open(sys.argv[1], "r") as file:
        result = Parser.run(file.read())
        temp_st = SymbolTable()
        result.Evaluate(temp_st)

        
else:
    sys.stderr.write("Must be a .c file !")
    raise ValueError








