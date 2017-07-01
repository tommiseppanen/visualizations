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

def adhesion(longSlipValue, latSlipValue, extremumValue, asymptoteValue, extremumSlipLong, asymptoteSlipLong, extremumSlipLat, asymptoteSlipLat):
    combinedSlip = np.sqrt(latSlipValue**2+longSlipValue**2)

    if (combinedSlip == 0):
        return 0;
	
    slippingValueAtExtremumLong = (asymptoteValue / asymptoteSlipLong) * extremumSlipLong
    AdhessionValueAtExtremumLong = extremumValue - slippingValueAtExtremumLong

    slippingValueAtExtremumLat = (asymptoteValue / asymptoteSlipLat) * extremumSlipLat
    AdhessionValueAtExtremumLat = extremumValue - slippingValueAtExtremumLat

    if (longSlipValue > 0):
        k = latSlipValue / longSlipValue
        limitx = (extremumSlipLong * extremumSlipLat) / np.sqrt(extremumSlipLat**2 + extremumSlipLong ** 2 * k ** 2) 

        limity = k * limitx
        limitTotal = np.sqrt(limitx**2+limity**2)

        limitAsymptoteX = (asymptoteSlipLong * asymptoteSlipLat) / np.sqrt(asymptoteSlipLat**2 + asymptoteSlipLong ** 2 * k ** 2)
        limitAsymptoteY = k * limitAsymptoteX
        limitAsymptoteTotal = np.sqrt(limitAsymptoteX**2+limitAsymptoteY**2)

        if (combinedSlip <= limitTotal):
            return (combinedSlip / limitTotal) * AdhessionValueAtExtremumLong
        elif (combinedSlip > limitTotal and combinedSlip < limitAsymptoteTotal):
            return (( - AdhessionValueAtExtremumLong) / (limitAsymptoteTotal - limitTotal)) \
            * (combinedSlip - limitTotal) + AdhessionValueAtExtremumLong
        return 0.0

    if (latSlipValue <= extremumSlipLat):
        return (latSlipValue / extremumSlipLat) * AdhessionValueAtExtremumLat
    elif (latSlipValue > extremumSlipLat and latSlipValue < asymptoteSlipLat):
        return (( - AdhessionValueAtExtremumLat) / (asymptoteSlipLat - extremumSlipLat)) \
        * (latSlipValue - extremumSlipLat) + AdhessionValueAtExtremumLat;
    return 0.0    

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
        slidingValue = slidingCoefficient(X[x], Y[y], 0.75, 0.4, 40)
        adhesionValue = adhesion(X[x], Y[y], 1.0, 0.75, 0.2, 0.4, 20, 40)
        zs[x*len(Y)+y] = slidingValue+adhesionValue
        c[x*len(Y)+y] = 'b' if slidingValue+adhesionValue <= 0.75 else 'r'

ax.scatter(xs, ys, zs, s = 1, c = c)
plt.show()
