import sys

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
        
        valid_tokens = [" ", "+" "-", ""]
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
            
            if(self.position == len(self.origin) - 1):
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
            
            if (i in numbers) or (i  in valid_tokens):
                self.position +=1 
                
                
            else:
                sys.stderr.write("Invalid Token")
                
                
        
        self.actual = Token("EOF", "")
        
        return self.actual
        

class Parser:


    @staticmethod
    def parseExpression(token):       
        
        result = ""
        token.selectNext()
                    
        
        
        if token.actual.type == "int":
            result = int(token.actual.value)           
            
            token.selectNext()
                      

            while(token.actual.type == "plus" or token.actual.type == "minus"):
                
                if(token.actual.type == "plus"):                    
                    token.selectNext()                    

                    if(token.actual.type == "int"):                        
                        result += int(token.actual.value)
                        

                    else:
                        sys.stderr.write("Invalid Sequence #1")
                    
                if(token.actual.type == "minus"):
                    token.selectNext()
                    if(token.actual.type == "int"):
                        result -= int(token.actual.value)
                    else:
                        sys.stderr.write("Invalid Sequence #2")

                token.selectNext()

                if(token.actual.type == "EOF"):
                    print(result)                   
                    return result

        else:
            sys.stderr.write("Invalid Sequence")


    @staticmethod
    def run(codigo_base):
        token = Tokenizer(codigo_base)
        return Parser.parseExpression(token)

Parser.run(sys.argv[1])










