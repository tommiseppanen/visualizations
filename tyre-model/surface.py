from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math


class FrictionCurvePoint:
    def __init__(self, value, slip):
        self.value = value
        self.slip = slip


class FrictionCurve:
    def __init__(self, extremum_value, asymptote_value, extremum_slip, asymptote_slip):
        self.extremum = FrictionCurvePoint(extremum_value, extremum_slip)
        self.asymptote = FrictionCurvePoint(asymptote_value, asymptote_slip)

    def calculate_coefficient(self, value):
        absolute_value = abs(value)
        if absolute_value <= self.extremum.slip:
            return (absolute_value / self.extremum.slip) * self.extremum.value
        elif self.extremum.slip < absolute_value < self.asymptote.slip:
            return ((self.asymptote.value - self.extremum.value) / (self.asymptote.slip - self.extremum.slip)) \
                   * (absolute_value - self.extremum.slip) + self.extremum.value
        return self.asymptote.value


def coefficient(long_slip_value, lat_slip_value, longitudinal_curve, lateral_curve):
    combined_slip = np.sqrt(lat_slip_value ** 2 + long_slip_value ** 2)

    if combined_slip == 0:
        return 0

    if long_slip_value != 0:
        combined_slip_curve = create_combined_curve(long_slip_value, lat_slip_value, longitudinal_curve, lateral_curve)
        return combined_slip_curve.calculate_coefficient(combined_slip)

    return lateral_curve.calculate_coefficient(lat_slip_value)


def create_combined_curve(long_slip_value, lat_slip_value, longitudinal_curve, lateral_curve):
    absolute_long_slip_value = abs(long_slip_value)
    absolute_lat_slip_value = abs(lat_slip_value)

    gradient = absolute_lat_slip_value / absolute_long_slip_value

    slip_values = (absolute_long_slip_value, absolute_lat_slip_value)
    extremum_value, asymptote_value = interpolate_combined_values(slip_values, longitudinal_curve, lateral_curve)
    limit_extremum = calculate_limit(gradient, longitudinal_curve.extremum.slip, lateral_curve.extremum.slip)
    limit_asymptote = calculate_limit(gradient, longitudinal_curve.asymptote.slip, lateral_curve.asymptote.slip)

    return FrictionCurve(extremum_value, asymptote_value, limit_extremum, limit_asymptote)


def interpolate_combined_values(slip_values, longitudinal_curve, lateral_curve):
    return interpolate_by_angle(slip_values, longitudinal_curve.extremum, lateral_curve.extremum), \
           interpolate_by_angle(slip_values, longitudinal_curve.asymptote, lateral_curve.asymptote)


def interpolate_by_angle(slip_values, longitudinal_curve_point, lateral_curve_point):
    long_slip_value, lat_slip_value = slip_values
    angle = math.atan2(lat_slip_value,
                       (lateral_curve_point.slip / longitudinal_curve_point.slip) * long_slip_value)
    return longitudinal_curve_point.value + \
        ((lateral_curve_point.value - longitudinal_curve_point.value) / (
               math.pi / 2)) * angle


def calculate_limit(gradient, longitudinal_slip, lateral_slip):
    limit_x = (longitudinal_slip * lateral_slip) / np.sqrt(lateral_slip ** 2 + longitudinal_slip ** 2 * gradient ** 2)
    limit_y = gradient * limit_x
    return np.sqrt(limit_x ** 2 + limit_y ** 2)


fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(0.00, 0.9, 0.005)
Y = np.arange(0, 90, 0.5)
XX, YY = np.meshgrid(X, Y, indexing='ij')
ZZ = np.zeros((len(X), len(Y)))
for i in range(len(X)):
    for j in range(len(Y)):
        ZZ[i, j] = coefficient(XX[i, j], YY[i, j], FrictionCurve(2 * 1.0, 2 * 0.75, 0.4, 0.8), FrictionCurve(1.0, 0.75, 20, 40))
ax.plot_surface(XX, YY, ZZ, cmap=plt.get_cmap('GnBu'),alpha=0.9,linewidth=0.25, edgecolors='black')
plt.show()
