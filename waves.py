import math
from decimal import Decimal
from matplotlib import pyplot as plt
from tkinter import *
from tkinter.font import Font, BOLD

class Wave:
    def __init__(self, a: float, l: float, u2: float, t: float, u1=1.0) -> None:
        self.k = Decimal('2.0')*Decimal(str(math.pi))/Decimal(str(l))
        self.phi = self.k*Decimal(str(t))*(Decimal(str(u2)) / Decimal(str(u1)))
        self.val = lambda x: Decimal(str(a)) * Decimal(str(math.sin(self.k*Decimal(str(x)) + self.phi)))


class IPolLig:
    def __init__(self, l: float, u1: float, u2: float, t=100.0, u=1.0, p=5000) -> None:
        if (l:=float(l)) <= 0 or float(u1) > float(u2) or (t:=float(t)) <= 0 or (u1:=float(u1)) <= 0 or (u2:=float(u2)) <= 0 or (u:=float(u)) <= 0 or (p:=int(p)) <= 0:
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


root = Tk()
root.geometry("480x480")
root.title("Polarized light visualization")

var_l = StringVar(root, value="447");
var_u1 = StringVar(root, value="1.3");
var_u2 = StringVar(root, value="1.4");
var_t = StringVar(root, value="100.0");
var_u = StringVar(root, value="1.0");
var_p = StringVar(root, value="5000");

frame = Frame(root, pady=20)
font = Font(root, size=16, weight=BOLD)
font_normal = Font(frame, size=16)

label_l = Label(frame, text="wavelength (nm)", padx=5, pady=2.5, font=font)
label_u1 = Label(frame, text="rf 1", padx=5, pady=2.5, font=font)
label_u2 = Label(frame, text="rf 2", padx=5, pady=2.5, font=font)
label_t = Label(frame, text="thickness (nm)", padx=5, pady=2.5, font=font)
label_u = Label(frame, text="rf outside", padx=5, pady=2.5, font=font)
label_p = Label(frame, text="number of points", padx=5, pady=2.5, font=font)

entry_l = Entry(frame, textvariable=var_l, font=font_normal)
entry_u1 = Entry(frame, textvariable=var_u1, font=font_normal)
entry_u2 = Entry(frame, textvariable=var_u2, font=font_normal)
entry_t = Entry(frame, textvariable=var_t, font=font_normal)
entry_u = Entry(frame, textvariable=var_u, font=font_normal)
entry_p = Entry(frame, textvariable=var_p, font=font_normal)

label_l.grid(row=0, column=0)
entry_l.grid(row=0, column=1)
label_u1.grid(row=1, column=0)
entry_u1.grid(row=1, column=1)
label_u2.grid(row=2, column=0)
entry_u2.grid(row=2, column=1)
label_t.grid(row=3, column=0)
entry_t.grid(row=3, column=1)
label_u.grid(row=4, column=0)
entry_u.grid(row=4, column=1)
label_p.grid(row=5, column=0)
entry_p.grid(row=5, column=1)

frame.pack()

frame_button = Frame(root, pady=20)
frame_visualize = Frame(root, pady=20)

calculated = False;
obj = None;

def calculate():
    global obj, calculated
    try:
        obj = IPolLig(var_l.get(), var_u1.get(), var_u2.get(), var_t.get(), var_u.get(), var_p.get())
        if obj is not None:
            calculated = True
        else:
            calculated = False
        change_buttons()
    except Exception as e:
        calculated = False
        change_buttons()

def change_buttons():
    global calculate, calculated, obj, frame_visualize, frame_button
    try:
        frame_button.destroy()
    except:
        pass
    try:
        frame_visualize.destroy()
    except:
        pass
    frame_button = Frame(root, pady=20)
    frame_visualize = Frame(root, pady=20)
    if calculated:
        frame_button.destroy();
        button = Button(frame_visualize, bg="blue", activebackground="blue", activeforeground="white", fg="white", text="Calculate", font=font, command=calculate)
        button.pack()
        button_plot_interference = Button(frame_visualize, bg="blue", activebackground="blue", activeforeground="white", fg="white", text="Plot graph", font=font, command=obj.plotintrf)
        button_plot_wave = Button(frame_visualize, bg="blue", activebackground="blue", activeforeground="white", fg="white", text="Plot wave", font=font, command=obj.plotintrfwave)
        button_plot_interference.pack()
        button_plot_wave.pack()
        frame_visualize.pack()
    else:
        frame_visualize.destroy()
        button = Button(frame_button, bg="blue", activebackground="blue", activeforeground="white", fg="white", text="Calculate", font=font, command=calculate)
        button.pack()
        frame_button.pack()

button = Button(frame_button, bg="blue", activebackground="blue", activeforeground="white", fg="white", text="Calculate", font=font, command=calculate)
button.pack()

frame_button.pack()

root.mainloop();