import pyxem as pxm
import numpy as np
import hyperspy.api as hs
from skimage import filters

def do_background_removal_2xxx(self, min_sigma=2, max_sigma=3, sigma=0.7, min=0.0002):
    """Return a SPED dataset after done standard background removal. This was just
    made for myself to learn python packaging. Use with care I guess...

    Parameters
    ----------
    min_sigma : minimum sigma for background subtraction

    max_sigma : maximum sigma for background subtraction

    sigma : sigma for smoothing the DP through mapping

    min : min intensity to keep in DP data. If lower than this its removed


    Returns
    -------
    s : Diffraction2D or LazyDiffraction2D signal

    """
    s = self.subtract_diffraction_background(method="difference of gaussians",
                                        min_sigma=min_sigma,
                                        max_sigma=max_sigma)

    # smooth out the output
    s = s.map(filters.gaussian, sigma=sigma, inplace=False)

    # Set values lower than a specific value to 0 in the image
    def crop_minimum(image, minimum=0.0005):
        copied = image.copy()
        copied[copied <= minimum] = 0.
        return copied

    # remove low intensities
    s = s.map(crop_minimum, minimum = 0.0002, inplace=False)

    return experimental_data