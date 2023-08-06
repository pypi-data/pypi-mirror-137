class RobustScaler():
    def transform(self, X):
        import numpy as np
        self.X = None
        self.X = np.copy(X)
        for i in range(len(self.X[0][:])):
           q1 = np.quantile(self.X[:,i], 0.25)
           median = np.quantile(self.X[:,i], 0.5)
           q3 = np.quantile(self.X[:,i], 0.75)
           for k in range(len(self.X[:][:])):
               self.X[k,i] = (self.X[k,i] - median) / (q3 - q1)
        return self.X

class MinMaxScaler():
    def transform(self, X):
        import numpy as np
        self.X = None
        self.X = np.copy(X)
        for i in range(len(self.X[0][:])):
           minimum = np.amin(self.X[:,i])
           maximum = np.amax(self.X[:,i])
           for k in range(len(self.X[:][:])):
               self.X[k,i] = (self.X[k,i] - minimum) / (maximum - minimum)
        return self.X

class StandardScaler():
    def transform(self, X):
        import numpy as np
        self.X = None
        self.X = np.copy(X)
        for i in range(len(self.X[0][:])):
           std = np.std(self.X[:,i])
           mean = np.mean(self.X[:,i])
           for k in range(len(self.X[:][:])):
               self.X[k,i] = (self.X[k,i] - mean) / (std)
        return self.X

class OneHotEncoder():
    def __init__(self):
        self.fit = False
        self.y = None
        self.L1 = []
        self.L2 = []
        self.L3 = []
        self.L4 = []
    
    def transform(self, y):
        import numpy as np
        self.y = y
        self.L4 = []
        if self.fit == False:
            self.L1 = []
            for e in y:
                if [e] not in self.L1:
                    self.L1.append([e])
            self.L2 = list(self.L1)
            for i in range(len(self.L2)):
                self.L2[i] = [0]*len(self.L2)
                self.L2[i][i] = 1
            self.L3 = np.concatenate((np.array(self.L2).reshape(-1,len(self.L2[0])), np.array(self.L1).reshape(-1,1)), axis=1)
            self.L4 = []
        for i in range(len(y)):
            for j in range(len(self.L3)):
                if y[i] == self.L3[j][-1]:
                    self.L4.append(list(self.L3[j][:-1]))
        self.fit = True
        return np.array(self.L4)