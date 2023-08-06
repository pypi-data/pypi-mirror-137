class Sampletestlohit:
    def __init__(self,a=1,b=1):
        self.a=a;
        self.b=b;

    def addition(self):
        return self.a+self.b

    def sub(self):
        if(self.a > self.b):
            return self.a - self.b
        else:
            return self.b-self.a

    def mul(self):
        return self.a * self.b

    def div(self):
        return self.a / self.b

    def setValue(self,a,b):
        self.a= a
        self.b= b