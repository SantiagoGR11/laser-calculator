import numpy as np
from scipy import odr


# -------------------------------
# 1. Rounding algorithm
# -------------------------------
def round_result(m, dm):
    # Make sure that dm!=0 to avoid errors in log10
    if np.all(dm == 0):
        return m, dm
    
    # Determine the precision based on the error
    precision = -np.floor(np.log10(np.abs(dm))).astype(int)
    
    # Round the values
    dm_rounded = np.round(dm, precision)
    m_rounded = np.round(m, precision)
    
    return m_rounded, dm_rounded

# -------------------------------
# 1. Linear estimations
# -------------------------------

def linear_estimation(Dm, Dmerr, ks, kerr):
    def lineal(p, x):
        m, b = p
        return m * x + b

    model = odr.Model(lineal)

    data = odr.RealData(Dm, ks, sx=Dmerr, sy=kerr)

    linear_fit = odr.ODR(data, model, beta0=[1.0, 0.0])
    
    exit = linear_fit.run()
    
    m, b = exit.beta  
    dm, db = exit.sd_beta   


    m_rounded, dm_rounded = round_result(m, dm)
    b_rounded, db_rounded = round_result(b, db) 
    return m_rounded, dm_rounded, b_rounded, db_rounded, m, b