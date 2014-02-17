import numpy as np


class SVD():
    def __init__(self, data, user_count, item_count, rank, learning_rate, reg):
        """data is a tuple of tuples (user, item, rating)"""
        self.data = data
        self.rank = rank #factors
        self.user_count = user_count
        self.item_count = item_count
        self.learning_rate = learning_rate
        self.reg = reg
        self.minimprove = .0001
        #create average rating for initial values
        average = np.average([line[2] for line in data])
        init = np.sqrt(average/rank)
        noise = .005
        
        self.U = np.random.RandomState.uniform(-noise, noise, item_count*rank)\
                .reshape(item_count,rank) + init
        self.V = np.random.RandomState.uniform(-noise,noise, user_count*rank)\
                .reshape(user_count, rank) + init
                
    def predict(self, userid, itemid):
        """rating of user i and item j is simply the dot product"""
        prediction = 0
        for i in range(self.rank):
            prediction += self.U[userid][i] * self.V[itemid][i]
        return prediction
        
    def train_model(self, data, epochs):
        oldtrain = 0
        for epoch in range(epochs):
            train = self.train()
            
            if abs(oldtrain - train) < self.minimprove:
                break
            oldtrain = train
            
        
    def train(self, k):
        """iterate through the data. For each rating, update the user and item factors."""
        SSqerror = 0
        for userid, item, rating in self.data:
            itemid = item-1
            
            error = rating - self.predict(userid, itemid)
            SSqerror += error ** 2
            
            uTemp = self.U[userid][k]
            vTemp = self.V[itemid][k]
            
            self.U[userid][k] += self.learning_rate * (error * vTemp - self.reg * uTemp)
            self.V[itemid][k] += self.learning_rate * (error * uTemp - self.reg * vTemp)
            
        return SSqerror/self.data.count
            