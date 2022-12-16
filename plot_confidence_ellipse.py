from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from math import sqrt, pi


def confidence_ellipse(covariance_matrix, average, ax, n_std=1.96, **kwargs):
    """
    Эллипс стандартных отклонений создано на основе статей:

    See how and why this works: https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html

    This function has made it into the matplotlib examples collection:
    https://matplotlib.org/devdocs/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py

    Or, once matplotlib 3.1 has been released:
    https://matplotlib.org/gallery/index.html#statistics

    kwargs : `~matplotlib.patches.Patch` properties
    :param n_std: множитель для стандартного отклонения по осям
    :param ax: область рисования, объект matplotlib
    :param average: средние арефметические значения по координатным осям
    :param covariance_matrix: матрица ковариации
      Returns
    -------
    matplotlib.patches.Ellipse
    Other parameters
    ----------------
    """

    pearson = covariance_matrix.iloc[0, 1] / sqrt(covariance_matrix.iloc[0, 0] * covariance_matrix.iloc[1, 1])

    ell_radius_x = sqrt(1 + pearson)
    ell_radius_y = sqrt(1 - pearson)

    scale_x = sqrt(covariance_matrix.iloc[0, 0]) * n_std
    mean_x = average['averageX (мм)']

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
    # render plot with "plt.show()"
