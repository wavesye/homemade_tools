import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

'''
该程序模拟了较复杂反应中串联反应的浓度随时间变化的情况
'''
fig, ax = plt.subplots()
plt.subplots_adjust(bottom = 0.25)
t = np.arange(0.0,100.0,1.0)
cA0 = 1.0
k1 = 0.04
cB0 = 0.0
k2 = 0.05
cC0 = 0.0
#k3 = 0.04
cA = cA0 * np.exp(-k1 * t)
cB = k1*cA0/(k2-k1) * (np.exp(-k1*t)-np.exp(-k2*t))
cC = cA0 * (1 + (k1*np.exp(-k2*t)-k2*np.exp(-k1*t))/(k2-k1))

lA, = plt.plot(t,cA,lw=2,label='$c_A$')
print(plt.gca().lines)
lB, = plt.plot(t,cB,lw=2,label='$c_B$')
print(plt.gca().lines)
lC, = plt.plot(t,cC,lw=2,label='$c_C$')
print(plt.gca().lines)
plt.legend()
ax.margins(x=0)
plt.title('Dominal Reaction')
axcolor = 'lightgoldenrodyellow'
axk1 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor) #[left,bottom,width,hight]
axk2 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

sk1 = Slider(axk1,'k1', 0.01, 0.5, valinit=k1)
sk2 = Slider(axk2,'k2', 0.01, 0.5, valinit=k2)

def update(val):
    new_k1 = sk1.val
    new_k2 = sk2.val

    lA.set_ydata(cA0 * np.exp(-new_k1 * t))
    lB.set_ydata(new_k1*cA0/(new_k2-new_k1) * (np.exp(-new_k1*t)-np.exp(-new_k2*t)))
    lC.set_ydata(cA0 * (1 + (new_k1*np.exp(-new_k2*t)-new_k2*np.exp(-new_k1*t))/(new_k2-new_k1)))
    fig.canvas.draw_idle()

sk1.on_changed(update)
sk2.on_changed(update)


resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sk1.reset()
    sk2.reset()

button.on_clicked(reset)

plt.show()