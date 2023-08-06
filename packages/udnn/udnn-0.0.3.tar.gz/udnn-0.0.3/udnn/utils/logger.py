class Logger(object):
    def __init__(self, filename, mode):
        super(Logger, self).__init__()
        if (len(filename.split('.'))==1):
            self.name = filename + '.csv'
        else:
            self.name = filename
        self.mode = mode
        if (self.mode == 'r') or (self.mode == 'a'):
            self.file=open(self.name,'r')
            lines=self.file.readlines()
            elements=[]
            for i in range(0,len(lines)):
                elements.append(lines[i].split('\t'))
            for i in range(0,len(elements)):
                for j in range(0,len(elements[i])):
                    elements[i][j]=elements[i][j].split('\n')[0]
            self.nsymbols = len(elements[0])
            self.names = elements[0]
            self.symbols = []
            self.idx = dict()
            for i in range(0,self.nsymbols):
                self.symbols.append([])
                self.idx[self.names[i]]=i
            for i in range(0,self.nsymbols):
                for j in range(1,len(lines)-1):
                    if elements[j][i].replace('.','',1).isdigit() == True:
                        self.symbols[i].append(elements[j][i])
                    else:
                        self.symbols[i].append(float(elements[j][i]))
            self.file.close()
            self.empty = False
        else:
            self.names = []
            self.nsymbols = []
            self.symbols = []
            self.idx = dict()
            self.empty = True

    def setNames(self, names):
        if (self.mode != 'w') and (self.mode != 'a'):
            print('Error log is Read Only')
        elif self.mode == 'a':
            print('Error log is in Append Mode')
        else:
            self.file=open(self.name, self.mode)
            self.names = names
            self.nsymbols = len(names)
            self.empty = False
            for k in range(0,len(names)):
                self.file.write(names[k] + '\t')
                self.symbols.append([])
                self.idx[names[k]]=k
            self.file.write('\n')
            self.file.close()

    def add(self, symbols):
        if (self.mode != 'w') and (self.mode != 'a'):
            print('Error log is Read Only')
        else:
            self.file=open(self.name,'a')
            for i in range(0,len(symbols)-1):
                if type(symbols[i]) == str:
                    self.file.write(symbols[i] + '\t')
                else:
                    self.file.write(('%s' % repr(symbols[i])) + '\t')
                self.symbols[i].append(symbols[i])
            if type(symbols[len(symbols)-1]) == str:
                self.file.write(symbols[len(symbols)-1])
            else:
                self.file.write(('%s' % repr(symbols[len(symbols)-1])))
            self.symbols[i].append(symbols[len(symbols)-1])
            self.file.write('\n')
            self.file.close()
