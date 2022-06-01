import sys
import re
import os

programe_name = "program.asm"

class ASM():
    code = '''
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  ; codigo gerado pelo compilador''' + '\n'
    rodape = """; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
"""

    @staticmethod
    def write(cmd):
        ASM.code += (cmd + '\n')

    @staticmethod
    def dump(): 
        with open(programe_name, 'w') as f:
            f.write(ASM.code)
        ASM.code += ASM.rodape


class Node():   
    Id = 0

    def __init__(self, value, ListOfNodes = []):
        self.value = value
        self.children = ListOfNodes
        

    def Evaluate(self):
        pass

    def UpdateId():
        Node.Id +=1
        return Node.Id

class BinOp(Node):

    def Evaluate(self):

        cria1 = self.children[0].Evaluate()
        ASM.write("PUSH EBX")
        cria2 = self.children[1].Evaluate()
        ASM.write("; codigo gerado pelo BinOp" )

        if (cria1[1] == "int") and (cria2[1] == "int"):
            if self.value == "plus":
                ASM.write("POP EAX")
                ASM.write("ADD EAX, EBX" )
                ASM.write("MOV EBX, EAX")
                result = cria1[0] + cria2[0]

            elif self.value == "minus":
                ASM.write("POP EAX" )
                ASM.write("SUB EAX, EBX" )
                ASM.write("MOV EBX, EAX" )
                result  = cria1[0] - cria2[0]

            elif self.value == "mult":
                ASM.write("POP EAX" )
                ASM.write("IMUL EBX" )
                ASM.write("MOV EBX, EAX" )
                result  = cria1[0] * cria2[0]

            elif self.value == "div":
                ASM.write("POP EAX" )
                ASM.write("IDIV EBX" )
                ASM.write("MOV EBX, EAX" )
                result  = int(cria1[0] / cria2[0])

            elif self.value == "doubleEqual":
                ASM.write("POP EAX")
                ASM.write("CMP EAX, EBX")
                ASM.write("CALL binop_je")
                result = bool(cria1[0] == cria2[0])

            elif self.value == "and":
                ASM.write("POP EAX" )
                ASM.write("AND  EAX, EBX" )
                ASM.write("MOV EBX, EAX" )
                result = (cria1[0] and cria2[0])

            elif self.value == "above":
                ASM.write("POP EAX")
                ASM.write("CMP EAX, EBX")
                ASM.write("CALL binop_jg")
                result = bool(cria1[0] > cria2[0])

            elif self.value == "below":
                ASM.write("POP EAX")
                ASM.write("CMP EAX, EBX")
                ASM.write("CALL binop_jl")
                result = bool(cria1[0] < cria2[0])

            elif self.value == "or":
                ASM.write("POP EAX" )
                ASM.write("OR  EAX, EBX" )
                ASM.write("MOV EBX, EAX " )
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



class UnOp(Node): #ok
    def Evaluate(self):
        result = self.children[0].Evaluate()

         
        if result[1] == "int":
            if self.value == "minus":
                ASM.write("MOV EAX,{result[0]}")
                ASM.write("MOV EBX,-1")
                ASM.write("IMUL EBX")
                ASM.write("MOV EBX,EAX")
                output = result[0] * -1
            elif self.value == "plus":
                output = result[0]
            elif self.value == "not":
                ASM.write("NEG EBX")
                ASM.write("MOV EBX, EAX")
                output = not(result[0])
        else:
            sys.stderr.write("Must be a int to be operated!")
            raise ValueError




        return (int(output), "int")

class WHILE(Node): #REVER
    def Evaluate(self):
        new_id = Node.UpdateId()
        ASM.write("LOOP_" + str(new_id) + ":")
        cria1 = self.children[0].Evaluate()[0]
        ASM.write("CMP EBX, False")
        ASM.write("JE EXIT_" + str(new_id) )
        self.children[1].Evaluate()
        ASM.write("JMP LOOP_" + str(new_id) )
        ASM.write("EXIT_"+ str(new_id) + ":" )

        #while self.children[0].Evaluate()[0]:
         #   self.children[1].Evaluate()

class SCANF(Node): #ok
    def Evaluate(self):
        resultado =  int(input())
        return (resultado, "int")

class IF(Node): #ok
    def Evaluate(self):
        new_id = Node.UpdateId()

        ASM.write("IF_"+str(new_id)+":" )
        cria1 = self.children[0].Evaluate()
        ASM.write("CMP EBX, False")

        if len(self.children) > 2:
            ASM.write("JE ELSE_" + str(new_id) )
            self.children[1].Evaluate()
            ASM.write("JMP EXIT_" + str(new_id) )
            ASM.write("ELSE_"+ str(new_id) + ":" )
            self.children[2].Evaluate()
            ASM.write("EXIT_"+ str(new_id) + ":" )
        else:
            ASM.write("JE EXIT_" + str(new_id) )
            self.children[1].Evaluate()
            ASM.write("JMP EXIT_" + str(new_id) )
            ASM.write("EXIT_"+ str(new_id) + ":" )




        #if self.children[0].Evaluate():
         #   self.children[1].Evaluate()

        #elif len(self.children) > 2:
         #   self.children[2].Evaluate()


class Block(Node): #ok
    def Evaluate(self):
        for n in self.children:
            n.Evaluate()

class IntVal(Node): #ok
    def Evaluate(self):
        ASM.write("MOV EBX," + str(self.value))
        return (self.value, "int")

class NoOp(Node): #ok
    def Evaluate(self):
        pass

dic_SymbolTable = {}

class SymbolTable: #ok
    
    

    @staticmethod
    def create(nome, tipo):
        global SymbolId
        
        if not(dic_SymbolTable):
            SymbolId = -4
        else:
            SymbolId -= 4

        if nome in dic_SymbolTable:
            sys.stderr.write("Invalid casting or more than one declaration of variable")
            raise ValueError 
        else:
            dic_SymbolTable[nome] = [None, tipo, SymbolId]
        
        

    @staticmethod
    def getter(chave):
        return dic_SymbolTable[chave]


    @staticmethod
    def setter(nome, valor):
        if nome in dic_SymbolTable:
            if valor[1] == dic_SymbolTable[nome][1]:
                dic_SymbolTable[nome][0] = valor[0]

            else:
                sys.stderr.write("Invalid association")
                raise ValueError 
        else:
            sys.stderr.write("Not declared")
            raise ValueError 


class Assignment(Node): #ok
    def Evaluate(self):
        cria1 = self.children[0]
        cria2 = self.children[1].Evaluate()     

        SymbolTable.setter(cria1, cria2)
        info_var = SymbolTable.getter(cria1) #REVER
        ASM.write("MOV [EBP " + str(info_var[2]) + "], EBX")

class Printf(Node): #ok
    def Evaluate(self):
        cria1 = self.children.Evaluate()
        #print(cria1[0])
        ASM.write("PUSH EBX")
        ASM.write("CALL print")
        ASM.write("POP EBX")

class Identifier(Node): #ok
    def Evaluate(self):
        variavel = SymbolTable.getter(self.value)
        ASM.write("MOV EBX, [EBP" + str(variavel[2]) + "]")
        return(variavel[0],variavel[1])

class Strval(Node): #ok
    def Evaluate(self):
        return(self.value, "str")

class Vardec(Node):
    def Evaluate(self):
        _value = self.value
        for ident in self.children:
            SymbolTable.create(ident.value, _value)
            ASM.write("PUSH DWORD 0")
        


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
        ReservedWords = ["printf", "scanf", "if", "while", "else", "int", "str"]
        
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
        ASM.dump()

        
else:
    sys.stderr.write("Must be a .c file !")
    raise ValueError

