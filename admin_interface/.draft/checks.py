class Filtro:
    def __init__(self):
        pass
    
    def CheckRule(self, clean):
        self.clean = clean
        #self.isalphanum = self.clean.isalnum()
        try:
            #if no numeric input will throw an error
            int(self.clean)
            if any(c in self.clean for c in "\"/'\;.,=%#$*()[]?¿¡@{}:!|&<>¨~°^ "):
                self.aproved = 'NO'
            elif len(self.clean) <= 10:
                self.aproved = 'YES'
            else:
                self.aproved = 'NO'
        except:
            self.aproved = 'NO'
        return self.aproved
    
    def CheckRuleName(self, clean):
        self.clean = clean
        try:
            #if no numeric input will throw an error
            if any(c in str(self.clean) for c in "\"/'\;,=%#$*()[]?¿¡@{}:!|&<>¨~°^"):
                self.aproved = 'NO'
            else:
                self.aproved = 'YES'
        except:
            self.aproved = 'NO'
        return self.aproved
    
    def CheckStr(self, clean):
        self.clean = clean
        self.isalphanum = self.clean.isalnum()
        if len(self.clean) == 40 and self.isalphanum == True:
            self.aproved = 'YES'

        else:
            self.aproved = 'NO'

        return self.aproved
    
    def CheckStr35(self, clean):
        self.clean = clean
        self.isalphanum = self.clean.isalnum()
        if self.isalphanum == True and (len(self.clean) == 35 or len(self.clean) == 36):
            self.aproved = 'YES'

        else:
            self.aproved = 'NO'

        return self.aproved


    
    def CheckPorts(self, ports):
        self.ports = ports
        if any(c in self.ports for c in "\"/';,%#$*=()[]{}:?¿¡!|&<>¨~°^ ."):
            self.aproved = 'NO'
        if re.search('[a-zA-Z]', self.ports):
            self.aproved = 'NO'
        if len(self.ports) < 2:
            self.aproved = 'NO'
        else:
            self.aproved = 'YES'
            
        
        return self.aproved
    
    def CheckName(self, name):
        self.name = name
        if any(c in self.name for c in "\"\\';,%$*=[]{}?¿¡!|<>¨~°^"):
            self.aproved = 'NO'
        else:
            self.aproved = 'YES'

        return self.aproved

    def CheckPath(self, path):
        self.path = path
        if any(c in self.path for c in "\"\\';,%$*[]{}:|<>¨~°^ "):
            self.aproved = 'NO'
        else:
            self.aproved = 'YES'

        return self.aproved
