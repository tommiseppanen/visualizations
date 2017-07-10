from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
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

    absolute_long_slip_value = abs(long_slip_value)
    absolute_lat_slip_value = abs(lat_slip_value)

    if combined_slip == 0:
        return 0

    asymptote_value, extremum_value = \
        interpolate_combined_values(absolute_long_slip_value, absolute_lat_slip_value, longitudinal_curve, lateral_curve)

    if absolute_long_slip_value > 0:
        gradient = absolute_lat_slip_value / absolute_long_slip_value

        limit_extremum = calculate_limit(gradient, longitudinal_curve.extremum_slip, lateral_curve.extremum_slip)
        limit_asymptote = calculate_limit(gradient, longitudinal_curve.asymptote_slip, lateral_curve.asymptote_slip)

        if combined_slip <= limit_extremum:
            return (combined_slip / limit_extremum) * extremum_value
        elif limit_extremum < combined_slip < limit_asymptote:
            return ((asymptote_value - extremum_value) / (limit_asymptote - limit_extremum)) \
                   * (combined_slip - limit_extremum) + extremum_value
        return asymptote_value

    if absolute_lat_slip_value <= lateral_curve.extremum_slip:
        return (absolute_lat_slip_value / lateral_curve.extremum_slip) * extremum_value
    elif lateral_curve.extremum_slip < absolute_lat_slip_value < lateral_curve.asymptote_slip:
        return ((asymptote_value - extremum_value) / (lateral_curve.asymptote_slip - lateral_curve.extremum_slip)) \
               * (absolute_lat_slip_value - lateral_curve.extremum_slip) + extremum_value
    return asymptote_value


def interpolate_combined_values(long_slip_value, lat_slip_value, longitudinal_curve, lateral_curve):
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
    return asymptote_value,extremum_value


def calculate_limit(gradient, longitudinal_slip, lateral_slip):
    limit_x = (longitudinal_slip * lateral_slip) / np.sqrt(lateral_slip ** 2 + longitudinal_slip ** 2 * gradient ** 2)
    limit_y = gradient * limit_x
    return np.sqrt(limit_x ** 2 + limit_y ** 2)

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(-0.9, 0.9, 0.01)
Y = np.arange(-90, 90, 1)

xs = np.zeros(len(X) * len(Y))
ys = np.zeros(len(X) * len(Y))
zs = np.zeros(len(X) * len(Y))
c = ["" for x in range(len(X) * len(Y))]
Z = np.zeros((len(X), len(Y)))
for x in range(len(X)):
    for y in range(len(Y)):
        xs[x * len(Y) + y] = X[x]
        ys[x * len(Y) + y] = Y[y]
        value = coefficient(X[x], Y[y], FrictionCurve(1 * 1.0, 1 * 0.75, 0.4, 0.8), FrictionCurve(1.0, 0.75, 20, 40))
        zs[x * len(Y) + y] = value
        c[x * len(Y) + y] = 'b' if value <= 0.75 else 'r'

ax.scatter(xs, ys, zs, s=1, c=c)
plt.show()
