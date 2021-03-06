import numpy as np

from bq3d.image_filters import filter_manager
from bq3d.image_filters.filter import FilterBase
from scipy.ndimage.filters import maximum_filter

from bq3d._version import __version__
__author__     = 'Ricardo Azevedo, Jack Zeitoun'
__copyright__  = "Copyright 2019, Gandhi Lab"
__license__    = 'BY-NC-SA 4.0'
__version__    = __version__
__maintainer__ = 'Ricardo Azevedo'
__email__      = 'ricardo-re-azevedo@gmail.com'
__status__     = "Development"


class Max(FilterBase):
    """Calculates local maxima of an image.

    See `scipy.ndimage.maximum_filter`

    Call using :meth:`filter_image` with 'Max' as filter.

    Attributes:
        input (array): Image to pass through filter.
        output (array): Filter result.

        size (float or tuple): Size of sliding window to look for max. If
            float, will apply same window to all axes. Default: 3.
    """

    def __init__(self):
        self.size = 3
        super().__init__()

    def _generate_output(self):
        img = self.input

        orig_shape = img.shape
        if len(orig_shape) < 3:
            img = img[np.newaxis, ...]

        res = maximum_filter(img, size=self.size)

        res.shape = orig_shape

        return res

filter_manager.add_filter(Max())

