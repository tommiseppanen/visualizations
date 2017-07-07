from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import math

def coefficient(longSlipValue, latSlipValue, extremumValueLong, asymptoteValueLong, extremumValueLat, asymptoteValueLat, extremumSlipLong, asymptoteSlipLong, extremumSlipLat, asymptoteSlipLat):
    combinedSlip = np.sqrt(latSlipValue**2+longSlipValue**2)

    if (combinedSlip == 0):
        return 0;

    angleExtremum = math.atan2(latSlipValue, (extremumSlipLat / extremumSlipLong)* longSlipValue)
    angleAsymptote = math.atan2(latSlipValue, (asymptoteSlipLat / asymptoteSlipLong)* longSlipValue)
    asymptoteValue = asymptoteValueLong + ((asymptoteValueLat-asymptoteValueLong) / (math.pi/2) ) * angleAsymptote
    extremumValue = extremumValueLong + ((extremumValueLat-extremumValueLong) / (math.pi/2) ) * angleExtremum

    if (longSlipValue > 0):       
        k = latSlipValue / longSlipValue
		
        limitExtremumX = (extremumSlipLong * extremumSlipLat) / np.sqrt(extremumSlipLat**2 + extremumSlipLong ** 2 * k ** 2) 
        limitExtremumY = k * limitExtremumX
        limitExtremumTotal = np.sqrt(limitExtremumX**2+limitExtremumY**2)

        limitAsymptoteX = (asymptoteSlipLong * asymptoteSlipLat) / np.sqrt(asymptoteSlipLat**2 + asymptoteSlipLong ** 2 * k ** 2)
        limitAsymptoteY = k * limitAsymptoteX
        limitAsymptoteTotal = np.sqrt(limitAsymptoteX**2+limitAsymptoteY**2)

        if (combinedSlip <= limitExtremumTotal):
            return (combinedSlip / limitExtremumTotal) * extremumValue
        elif (combinedSlip > limitExtremumTotal and combinedSlip < limitAsymptoteTotal):
            return (( asymptoteValue - extremumValue) / (limitAsymptoteTotal - limitExtremumTotal)) \
            * (combinedSlip - limitExtremumTotal) + extremumValue
        return asymptoteValue

    if (latSlipValue <= extremumSlipLat):
        return (latSlipValue / extremumSlipLat) * extremumValue
    elif (latSlipValue > extremumSlipLat and latSlipValue < asymptoteSlipLat):
        return (( asymptoteValue - extremumValue) / (asymptoteSlipLat - extremumSlipLat)) \
        * (latSlipValue - extremumSlipLat) + extremumValue;
    return asymptoteValue   

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
        value = coefficient(X[x], Y[y], 2*1.0, 2*0.75, 1.0, 0.75, 2*0.2, 2*0.4, 20, 40) 
        zs[x*len(Y)+y] = value
        c[x*len(Y)+y] = 'b' if value <= 0.75 else 'r'

ax.scatter(xs, ys, zs, s = 1, c = c)
plt.show()
