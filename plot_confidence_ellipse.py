
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from math import sqrt, pi


def confidence_ellipse(covariance_matrix, average, ax, n_std=1.96, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`

    See how and why this works: https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html

    This function has made it into the matplotlib examples collection:
    https://matplotlib.org/devdocs/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py

    Or, once matplotlib 3.1 has been released:
    https://matplotlib.org/gallery/index.html#statistics

    I update this gist according to the version there, because thanks to the matplotlib community
    the code has improved quite a bit.
    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.
    ax : matplotlib.axes.Axes
        The axe
    n_std : floats object to draw the ellipse into.
        The number of standard deviations to determine the ellipse's radiuses.
    Returns
    -------
    matplotlib.patches.Ellipse
    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    # if x.size != y.size:
        # raise ValueError("x and y must be the same size")

    # cov = cov(x, y)
    pearson = covariance_matrix.iloc[0, 1] / sqrt(covariance_matrix.iloc[0, 0] * covariance_matrix.iloc[1, 1])

    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.

    ell_radius_x = sqrt(1 + pearson)
    ell_radius_y = sqrt(1 - pearson)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = sqrt(covariance_matrix.iloc[0, 0]) * n_std
    mean_x = average['averageX (мм)']

    # calculating the stdandard deviation of y ...
    scale_y = sqrt(covariance_matrix.iloc[1, 1]) * n_std
    mean_y = average['averageY (мм)']

    R = ell_radius_x / sqrt(2) * scale_x
    r = ell_radius_y / sqrt(2) * scale_y
    ellipse_square = r * R * pi

    ellipse = Ellipse((0, 0),
                      width=ell_radius_x * 2,
                      height=ell_radius_y * 2,
                      facecolor=(1, 0.1, 0.1, 0.04),
                      edgecolor=(1, 0.1, 0.1, 0.7),
                      linewidth=3,
                      **kwargs)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)

    return {'plot': ax.add_patch(ellipse), 'square': ellipse_square}
    # render plot with "plt.show()".