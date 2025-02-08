import math
from decimal import Decimal
from matplotlib import pyplot as plt

class Wave:
    def __init__(self, a: float, l: float, u2: float, t: float, u1=1.0) -> None:
        self.k = Decimal('2.0')*Decimal(str(math.pi))/Decimal(str(l))
        self.phi = self.k*Decimal(str(t))*(Decimal(str(u2)) / Decimal(str(u1)))
        self.val = lambda x: Decimal(str(a)) * Decimal(str(math.sin(self.k*Decimal(str(x)) + self.phi)))


class IPolLig:
    def __init__(self, l: float, u1: float, u2: float, t=100.0, u=1.0, p=5000) -> None:
        if l <= 0 or u1 > u2 or t <= 0 or u1 <= 0 or u2 <= 0 or u <= 0 or p <= 0:
            print("Invalid argument: l > 0 / u1 < u2 / t > 0 / u, u1, u2 > 0 / p > 0\n")
        self.ord = Wave(Decimal('2') ** Decimal('-0.5'), l, u1, t, u)
        self.exord = Wave(Decimal('2') ** Decimal('-0.5'), l, u2, t, u)
        self.l = float(l)
        self.p = int(p)
        self.u1 = float(u1)
        self.u2 = float(u2)
        self.val = lambda x: (self.ord.val(x), self.exord.val(x))
        self.idata = self._interference()

    def _interference(self) -> tuple:
        l1 = Decimal(str(self.l)) / self.p
        lis1 = list()
        lis2 = list()
        lis3 = list()
        ang = list()
        for i in range(self.p + 1):
            a1 = self.val(i*l1)
            lis3.append(float(i*l1))
            lis1.append(float(a1[0]))
            lis2.append(float(a1[1]))
            ang.append(a1[0]/ a1[1])
        return lis1, lis2, lis3, ang

    def plotintrf(self, pr=1) -> None:
        pr = Decimal(str(math.tan(Decimal(str(pr)) * Decimal(str(math.pi)) / 360)))
        plt.subplot(2, 1, 1)
        plt.plot(self.idata[0], self.idata[1])
        plt.title("Interference wave")
        plt.xlabel("Low RI: " + str(self.u1))
        plt.ylabel("High RI: " + str(self.u2))
        plt.subplot(2, 1, 2)
        x = list()
        for i in enumerate(self.idata[3]):
            i1 = i[1] + 1
            if i1 <= pr and i1 >= -pr:
                x.append((i[0], i[1]))
        if len(x) == 0:
            for i in range(len(self.idata[0])):
                if round(self.idata[0][i], 6) != round(self.idata[1][i], 6):
                    print("Change pr: " + str(pr) + " or increase number of points: " + str(self.p))
                    exit()
            x = 0.0
        else:
            x = max([float((Decimal(str(self.idata[0][i[0]])) ** 2  + Decimal(str(self.idata[1][i[0]])) ** 2) ** Decimal('0.5')) for i in x])
        plt.plot(["Maximum", "Maximum", "Analyzer: " + str(x), "Analyzer: " + str(x)], [0.0, 1.0, x, 0.0])
        plt.show()
        
    def plotintrfwave(self) -> None:
        fig = plt.figure()
        p = plt.axes(projection='3d')
        p.scatter3D(self.idata[0], self.idata[1], self.idata[2])
        p.set_xlabel("Low RI: " + str(self.u1))
        p.set_ylabel("High RI: " + str(self.u2))
        p.set_zlabel("Direction of Propagation")
        plt.show()

