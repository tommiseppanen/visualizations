from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def slidingCoefficient(longSlipValue, latSlipValue, asymptoteValue, asymptoteSlipLong, asymptoteLatSlip):
    combinedSlip = np.sqrt(latSlipValue**2+longSlipValue**2)

    if (combinedSlip == 0):
        return 0;

    if (longSlipValue > 0):
        k = latSlipValue / longSlipValue
        limitx = (asymptoteSlipLong * asymptoteLatSlip) / np.sqrt(asymptoteLatSlip**2 + asymptoteSlipLong ** 2 * k ** 2) 

        limity = k * limitx
        limitTotal = np.sqrt(limitx**2+limity**2)

        if (combinedSlip < limitTotal):
            return (combinedSlip / limitTotal) * asymptoteValue       
        return asymptoteValue
    else:
        if (latSlipValue < asymptoteLatSlip):
            return (latSlipValue / asymptoteLatSlip) * asymptoteValue       
        return asymptoteValue

def adhesion(slipValue, extremumValue, extremumSlip, asymptoteValue, asymptoteSlip):
    if (slipValue > asymptoteSlip):
        return 0.0

    slippingValueAtExtremum = (asymptoteValue / asymptoteSlip) * extremumSlip
    AdhessionValueAtExtremum = extremumValue - slippingValueAtExtremum
        
    if (slipValue < extremumSlip):
        return (AdhessionValueAtExtremum / extremumSlip) * slipValue

    return (( - AdhessionValueAtExtremum) / (asymptoteSlip - extremumSlip)) \
                              * (slipValue - extremumSlip) + AdhessionValueAtExtremum;
    
    

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(0.0, 0.9, 0.01)
Y = np.arange(0.0, 90, 1)

xs = np.zeros(len(X)*len(Y))
ys = np.zeros(len(X)*len(Y))
zs = np.zeros(len(X)*len(Y))
c = ["" for x in range(len(X)*len(Y))]
Z = np.zeros((len(X),len(Y)))
for x in range(len(X)):
    for y in range(len(Y)):
        xs[x*len(Y)+y] = X[x]
        ys[x*len(Y)+y] = Y[y]
        adhesionlong = adhesion(X[x], 1.0, 0.2, 0.75, 0.4)
        adhesionlat = adhesion(Y[y], 1.0, 20, 0.75, 40)
        value = slidingCoefficient(X[x], Y[y], 0.75, 0.4, 40) + np.sqrt(adhesionlong**2+adhesionlat**2)
        zs[x*len(Y)+y] = value
        c[x*len(Y)+y] = 'b' if value < 0.75 else 'r'

ax.scatter(xs, ys, zs, s = 1, c = c)
plt.show()
