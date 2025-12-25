import numpy as np
from scipy.fft import fft, fftfreq, ifft
from scipy.optimize import curve_fit

# -------------------------------
# 1. FFT | envelope and carrier wavenumbers estimation
# -------------------------------

def compute_fft(signal, dx):
    N = len(signal)
    k = 2 * np.pi * fftfreq(N, d=dx)
    spectrum = np.abs(fft(signal))
    return k, spectrum

def estimate_wavenumbers(k, spectrum, km_range=(0, 500), kc_range=(900, 1100)):
    mask_m = (k > km_range[0]) & (k < km_range[1])
    mask_c = (k > kc_range[0]) & (k < kc_range[1])
    km = k[mask_m][np.argmax(spectrum[mask_m])]
    kc = k[mask_c][np.argmax(spectrum[mask_c])]
    return km, kc

# -------------------------------
# 2. Double bandpass filtering
# -------------------------------
def double_bandpass(signal, k, km, kc, sigma_m, sigma_c):
    S = fft(signal)
    filter = (
        np.exp(-0.5*((k-km)/sigma_m)**2) +
        np.exp(-0.5*((k+km)/sigma_m)**2) +
        np.exp(-0.5*((k-kc)/sigma_c)**2) +
        np.exp(-0.5*((k+kc)/sigma_c)**2)
    )
    return np.real(ifft(S * filter))

# -------------------------------
# 3. Modeling and fitting by NLLS
# -------------------------------
def proposed_expression(x, B, C, D, km, kc):
    gauss_sup = B * np.exp(-(km * x)**2 / 2)
    gauss_inf = C * np.exp(-(D * x)**2 / 2)
    average_line = (gauss_sup + gauss_inf) / 2
    variable_amplitude = (gauss_sup - gauss_inf) / 2
    return average_line + variable_amplitude * np.cos(kc * x)

def fit_signal(x, signal, p0):
    popt, pcov = curve_fit(proposed_expression, x, signal, p0=p0)
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

# -------------------------------
# 4. Complete pipeline
# -------------------------------
def process_signal(x, I, km_range=(0, 500), kc_range=(900, 1100)):
    dx = x[1] - x[0]
    I_fft = I - np.mean(I) # Remove DC component
    k_spectrum, spectrum = compute_fft(I_fft, dx)
    km, kc = estimate_wavenumbers(k_spectrum, spectrum, km_range, kc_range)
    
    # Filtering
    signal_filtered = double_bandpass(I_fft, k_spectrum, km, kc, sigma_m=0.3*km, sigma_c=0.3*kc)
    ## Restore DC component
    signal_filtered += np.mean(I)
    ## Signal centering
    x = x - x[np.argmax(signal_filtered)]
    ## Impose symmetry
    xlim = min(abs(x[0]), abs(x[-1]))
    mask = abs(x) <= xlim
    x = x[mask]
    signal_filtered = signal_filtered[mask]
    signal_pos, signal_neg = signal_filtered[x>0], signal_filtered[x<0]
    signal_avg = (signal_pos + signal_neg[::-1])/2
    signal_filtered[x>0] = signal_avg
    signal_filtered[x<0] = signal_avg[::-1]
    ## Normalize
    signal_filtered /= np.max(signal_filtered)

    # Fitting
    p0 = [1.0, 1.0, 2*km, km, kc]
    popt, perr = fit_signal(x, signal_filtered, p0)

    return k_spectrum, spectrum, km, kc, signal_filtered, popt, perr