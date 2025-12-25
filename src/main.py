"""
main.py
Principal script of the LASER CALCULATOR proyect.
This file manage the data load, preprocess, FFT analysis,
pass-band filtering and NLLS fitting for the experiment of the wavenumber manipulation.
"""

# Import own modules
from preprocessing import normalize_and_interpolate
from signal_processing import process_signal
from parameter_analysis import linear_estimation
from visualization import plot_measured_signals, plot_fft, plot_filtered_vs_fitted, plot_parameter_trends

# Standar libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import fft, fftfreq

# -------------------------------
# 1. Data load and parameters of each measurement
# -------------------------------
df = pd.read_csv('data\dataset_laser.csv')

# Interference patterns measured
x1, I1 = df['x1'].dropna().to_numpy(), df['I1'].dropna().to_numpy()
x2, I2 = df['x2'].dropna().to_numpy(), df['I2'].dropna().to_numpy()
x3, I3 = df['x3'].dropna().to_numpy(), df['I3'].dropna().to_numpy()
x50, I50 = df['x50'].dropna().to_numpy(), df['I50'].dropna().to_numpy()
x100, I100 = df['x100'].dropna().to_numpy(), df['I100'].dropna().to_numpy()
x200, I200 = df['x200'].dropna().to_numpy(), df['I200'].dropna().to_numpy()

# Other significant parameters
## Δm values
Dm = [1, 2, 3, 50, 100, 200] 
## Wavelength of the He-Ne laser in meters
lambda_laser = 632.8e-9 
## Slits separation (d) and width (a) in meters
d_rend1, a_rend1, d_rend2, a_rend2 = 4e-4, 5e-5, 1.25e-3, 0.75e-4
## Inverse of the grating density in meters
dinv = 4000
## Distance between diffraction grating and double slit in meters
y, dy= np.array([0.016, 0.008, 0.005, 0.010, 0.005, 0.002]), 0.0002
## Δm error values
Dm_err1 = d_rend1 / (dinv*lambda_laser*y[:3]**2)*dy + a_rend1 / (dinv*lambda_laser*y[:3])
Dm_err2 = d_rend2 / (dinv*lambda_laser*y[3:]**2)*dy + a_rend2 / (dinv*lambda_laser*y[3:])
Dm_err = np.concatenate((Dm_err1, Dm_err2))


# -------------------------------
# 2. Preprocessing of the data
# -------------------------------
x1_new, I1_new = normalize_and_interpolate(x1, I1)
x2_new, I2_new = normalize_and_interpolate(x2, I2)
x3_new, I3_new = normalize_and_interpolate(x3, I3)
x50_new, I50_new = normalize_and_interpolate(x50, I50)
x100_new, I100_new = normalize_and_interpolate(x100, I100)
x200_new, I200_new = normalize_and_interpolate(x200, I200)

# Clustering preprocess data
x = np.column_stack((x1_new, x2_new, x3_new, x50_new, x100_new, x200_new))
I = np.column_stack((I1_new, I2_new, I3_new, I50_new, I100_new, I200_new))


# -------------------------------
# 3. Signal processing (FFT, filtering and fitting by NLLS)
# -------------------------------
km_spectrum, kc_spectrum = np.zeros(I.shape[1]), np.zeros(I.shape[1])
popt_all, perr_all = np.zeros((I.shape[1], 5)), np.zeros((I.shape[1], 5))

k_spectrum1, spectrum1, km_spectrum[0], kc_spectrum[0], signal_filtered1, popt_all[0], perr_all[0] = process_signal(x[:, 0], I[:, 0])
k_spectrum2, spectrum2, km_spectrum[1], kc_spectrum[1], signal_filtered2, popt_all[1], perr_all[1] = process_signal(x[:, 1], I[:, 1])
k_spectrum3, spectrum3, km_spectrum[2], kc_spectrum[2], signal_filtered3, popt_all[2], perr_all[2] = process_signal(x[:, 2], I[:, 2])
k_spectrum50, spectrum50, km_spectrum[3], kc_spectrum[3], signal_filtered50, popt_all[3], perr_all[3] = process_signal(x[:, 3], I[:, 3])
k_spectrum100, spectrum100, km_spectrum[4], kc_spectrum[4], signal_filtered100, popt_all[4], perr_all[4] = process_signal(x[:, 4], I[:, 4])
k_spectrum200, spectrum200, km_spectrum[5], kc_spectrum[5], signal_filtered200, popt_all[5], perr_all[5] = process_signal(x[:, 5], I[:, 5])


# -------------------------------
# 4. Behavior of the interference pattern vs Δm
# -------------------------------

# Values of km and kc including their errors
km = np.abs(popt_all[:,3])
km_err = np.abs(perr_all[:,3])
kc = np.abs(popt_all[:,4])
kc_err = np.abs(perr_all[:,4])

# Linear estimation in regime Δm = 1, 2, 3
mc1, dmc1, bc1, dbc1, mc1_est, bc1_est = linear_estimation(Dm[:3], Dm_err[:3], kc[:3], kc_err[:3] )
mm1, dmm1, bm1, dbm1, mm1_est, bm1_est = linear_estimation(Dm[:3], Dm_err[:3], km[:3], km_err[:3] )

m1 = np.linspace(0, 4, 50)
kc_lin1 = mc1_est*m1 + bc1_est
km_lin1 = mm1_est*m1 + bm1_est

# Linear estimation in regime Δm = 50, 100, 200
mc2, dmc2, bc2, dbc2, mc2_est, bc2_est = linear_estimation(Dm[3:], Dm_err[3:], kc[3:], kc_err[3:] )
mm2, dmm2, bm2, dbm2, mm2_est, bm2_est = linear_estimation(Dm[3:], Dm_err[3:], km[3:], km_err[3:] )

m2 = np.linspace(45, 205, 50)
kc_lin2 = mc2_est*m2 + bc2_est
km_lin2 = mm2_est*m2 + bm2_est


# -------------------------------
# 5. Visualization
# -------------------------------

# Plot measured signals for Δm = 50, 100, 200 
plot_measured_signals(x[:, 3:6], I[:, 3:6], Dm[3:6])

# Plot FFT of signals Δm = 50, 100, 200
plot_fft([k_spectrum50, k_spectrum100, k_spectrum200],
         [spectrum50, spectrum100, spectrum200],
         Dm[3:6])

# Plot filtered and fitted signal for Δm = 200
plot_filtered_vs_fitted(x[:-1, 5], signal_filtered200, popt_all[5], Dm[5])

# Plot trends between km, kc and Δm
plot_parameter_trends(Dm, Dm_err, m1, m2,
                      kc, kc_err, mc1, dmc1, mc2, dmc2,
                      kc_lin1, kc_lin2,
                      km, km_err, mm1, dmm1, mm2, dmm2,
                      km_lin1, km_lin2)
