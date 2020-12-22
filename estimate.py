class Estimate:
    def __init__(self):
        self.theta0 = 0
        self.theta1 = 0

    def setThetas(self):
        filee = open("data.txt", "r")
        content = filee.read()
        lines = content.split('\n')
        for i in range(len(lines)):
            c = lines[i].split("=")
            if c[0] == "theta0":
                self.theta0 = float(c[1])
            if c[0] == "theta1":
                self.theta1 = float(c[1])
        filee.close()

    def getPrice(self, kil):
        price = self.theta0 + (self.theta1 * kil)
        return (price)

estimate = Estimate()
estimate.setThetas()
try:
    kil = int(input())
    price = estimate.getPrice(kil)
    print(str(price))
except ValueError:
    print("Oops!  That was no valid number.  Try again...")
