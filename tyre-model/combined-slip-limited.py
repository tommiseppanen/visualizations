from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def coefficient(slipValue, extremumValue, extremumSlip, asymptoteValue, asymptoteSlip):
    coefficient = asymptoteValue;
    absoluteSlip = abs(slipValue);
    if (absoluteSlip <= extremumSlip):
        coefficient = (extremumValue / extremumSlip) * absoluteSlip;
    elif (absoluteSlip > extremumSlip and absoluteSlip < asymptoteSlip):
        coefficient = ((asymptoteValue - extremumValue) / (asymptoteSlip - extremumSlip)) \
                              * (absoluteSlip - extremumSlip) + extremumValue;
    return coefficient

def adjustedLateral(longitudinal, lateral, extremumLongitudinalValue):
    return lateral*np.sqrt(1-(longitudinal/extremumLongitudinalValue)**2)

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(0, 0.9, 0.01)
Y = np.arange(0, 90, 1)
X, Y = np.meshgrid(X, Y)
longfunc = np.vectorize(lambda t: coefficient(t, 1, 0.2, 0.75, 0.4))
lateralfunc = np.vectorize(lambda t: coefficient(t, 1.0, 20.0, 0.75, 40))
Z = np.sqrt(longfunc(X)**2 + adjustedLateral(longfunc(X), lateralfunc(Y), 1.0)**2)

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax.set_zlim(0.0, 2.0)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
