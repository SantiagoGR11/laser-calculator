import numpy as np
from scipy.interpolate import interp1d

def normalize_and_interpolate(x, I, num_points=500, width_limit=0.04):
    # Centering of the data
    x -= x[np.argmax(I)]

    # Discard irrelevant data
    x, I = x[np.abs(x) <= width_limit], I[np.abs(x) <= width_limit]

    # Normalize
    I = I / np.max(I)

    # Linear + cubic interpolation
    interp_lin = interp1d(x, I, 'linear')
    x_new = np.linspace(min(x), max(x), num_points)
    I_lin = interp_lin(x_new)
    interp_cub = interp1d(x_new, I_lin, 'cubic')
    I_new = interp_cub(x_new)
    
    return x_new, I_new