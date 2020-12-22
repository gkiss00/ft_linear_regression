from sklearn import preprocessing
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Trainer:
    def __init__(self):
        self.kil = []
        self.kil_normalized = []
        self.price = []
        self.price_normalized = []
        self.price_predict = []
        self.price_predict_denormalized = []
        self.index = []
        self.errors = []
        self.theta0 = 0
        self.theta1 = 0
        self.theta0_denormalized = 0
        self.theta1_denormalized = 0
        self.learning_ratio = 1
        self.nb_iteration = 100
        self.size = 0

    def getData(self):
        data = pd.read_csv("data.csv")
        self.kil = np.array(data["km"])
        self.price = np.array(data["price"])
        self.size = len(self.price)
        self.normalize()

    def estimatePrice(self, kilometres):
        estimate_price = self.theta0 + (self.theta1 * kilometres)
        return estimate_price

    def train(self):
        self.theta1 = 1
        for i in range(self.nb_iteration):
            er = 0
            tmp_theta0 = 0
            tmp_theta1 = 0
            for k in range(self.size):
                tmp_theta0 += self.estimatePrice(self.kil_normalized[k]) - self.price_normalized[k]
                tmp_theta1 += (self.estimatePrice(self.kil_normalized[k]) - self.price_normalized[k]) * self.kil_normalized[k]
                er += (self.estimatePrice(self.kil_normalized[k]) - self.price_normalized[k]) ** 2
            tmp_theta0 = self.learning_ratio * (tmp_theta0 / self.size)
            tmp_theta1 = self.learning_ratio * (tmp_theta1 / self.size)
            self.errors.append(er)
            self.index.append(i)
            self.theta0 -= tmp_theta0
            self.theta1 -= tmp_theta1
            
            
        self.pricePredict()
        self.denormalize()

    def pricePredict(self):
        for i in range(self.size):
            self.price_predict.append(self.theta0 + (self.theta1 * self.kil_normalized[i]))

    def normalize(self):
        for i in range(self.size):
            self.kil_normalized.append((self.kil[i] - self.kil.min()) / (self.kil.max() -self.kil.min()))
            self.price_normalized.append((self.price[i] - self.price.min()) / (self.price.max() -self.price.min()))

    def denormalize(self):
        for i in range(self.size):
            self.price_predict_denormalized.append((self.price_predict[i] * (self.price.max() - self.price.min())) + self.price.min())
        self.theta1_denormalized = (self.price_predict_denormalized[1] - self.price_predict_denormalized[0]) / (self.kil[1] - self.kil[0])
        self.theta0_denormalized = self.price_predict_denormalized[0] - (self.kil[0] * self.theta1_denormalized)
        print(self.theta1_denormalized)
        print(self.theta0_denormalized)

    def graph(self):
        plt.plot(self.kil, self.price_predict_denormalized)
        plt.plot(self.kil, self.price, "ro")
        plt.ylabel("price")
        plt.show()

    def graph_normalized(self):
        plt.plot(self.kil_normalized, self.price_predict)
        plt.plot(self.kil_normalized, self.price_normalized, "ro")
        plt.ylabel("price")
        plt.show()

    def graph_error(self):
        #plt.plot(np.arange(1, len(self.errors) + 1), self.errors, color='red', linewidth=5)
        plt.plot(self.index, self.errors, "ro")
        plt.ylabel("error")
        plt.show()

    def save(self):
        f = open("data.txt", "w")
        f.write("theta1=")
        f.write(str(self.theta1_denormalized))
        f.write("\ntheta0=")
        f.write(str(self.theta0_denormalized))
        f.close()

trainer = Trainer()
trainer.getData()
trainer.train()
trainer.graph()
trainer.graph_normalized()
trainer.graph_error()
trainer.save()