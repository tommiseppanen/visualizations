from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import math


class FrictionCurve:
    def __init__(self, extremum_value, asymptote_value, extremum_slip, asymptote_slip):
        self.extremum_value = extremum_value
        self.extremum_slip = extremum_slip
        self.asymptote_value = asymptote_value
        self.asymptote_slip = asymptote_slip


def coefficient(long_slip_value, lat_slip_value, longitudinal_curve, lateral_curve):
    combined_slip = np.sqrt(lat_slip_value ** 2 + long_slip_value ** 2)

    if combined_slip == 0:
        return 0

    angle_extremum = math.atan2(lat_slip_value,
                                (lateral_curve.extremum_slip / longitudinal_curve.extremum_slip) * long_slip_value)
    angle_asymptote = math.atan2(lat_slip_value,
                                 (lateral_curve.asymptote_slip / longitudinal_curve.asymptote_slip) * long_slip_value)
    asymptote_value = longitudinal_curve.asymptote_value + \
                      ((lateral_curve.asymptote_value - longitudinal_curve.asymptote_value) / (
                          math.pi / 2)) * angle_asymptote
    extremum_value = longitudinal_curve.extremum_value + \
                     ((lateral_curve.extremum_value - longitudinal_curve.extremum_value) / (
                         math.pi / 2)) * angle_extremum

    if long_slip_value > 0:
        k = lat_slip_value / long_slip_value

        limit_extremum_x = (longitudinal_curve.extremum_slip * lateral_curve.extremum_slip) / np.sqrt(
            lateral_curve.extremum_slip ** 2 + longitudinal_curve.extremum_slip ** 2 * k ** 2)
        limit_extremum_y = k * limit_extremum_x
        limit_extremum_total = np.sqrt(limit_extremum_x ** 2 + limit_extremum_y ** 2)

        limit_asymptote_x = (longitudinal_curve.asymptote_slip * lateral_curve.asymptote_slip) / np.sqrt(
            lateral_curve.asymptote_slip ** 2 + longitudinal_curve.asymptote_slip ** 2 * k ** 2)
        limit_asymptote_y = k * limit_asymptote_x
        limit_asymptote_total = np.sqrt(limit_asymptote_x ** 2 + limit_asymptote_y ** 2)

        if combined_slip <= limit_extremum_total:
            return (combined_slip / limit_extremum_total) * extremum_value
        elif limit_extremum_total < combined_slip < limit_asymptote_total:
            return ((asymptote_value - extremum_value) / (limit_asymptote_total - limit_extremum_total)) \
                   * (combined_slip - limit_extremum_total) + extremum_value
        return asymptote_value

    if lat_slip_value <= lateral_curve.extremum_slip:
        return (lat_slip_value / lateral_curve.extremum_slip) * extremum_value
    elif lateral_curve.extremum_slip < lat_slip_value < lateral_curve.asymptote_slip:
        return ((asymptote_value - extremum_value) / (lateral_curve.asymptote_slip - lateral_curve.extremum_slip)) \
               * (lat_slip_value - lateral_curve.extremum_slip) + extremum_value
    return asymptote_value


fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(0.0, 0.9, 0.01)
Y = np.arange(0.0, 90, 1)

xs = np.zeros(len(X) * len(Y))
ys = np.zeros(len(X) * len(Y))
zs = np.zeros(len(X) * len(Y))
c = ["" for x in range(len(X) * len(Y))]
Z = np.zeros((len(X), len(Y)))
for x in range(len(X)):
    for y in range(len(Y)):
        xs[x * len(Y) + y] = X[x]
        ys[x * len(Y) + y] = Y[y]
        value = coefficient(X[x], Y[y], FrictionCurve(2 * 1.0, 2 * 0.75, 0.4, 0.8), FrictionCurve(1.0, 0.75, 20, 40))
        zs[x * len(Y) + y] = value
        c[x * len(Y) + y] = 'b' if value <= 0.75 else 'r'

ax.scatter(xs, ys, zs, s=1, c=c)
plt.show()
