import matplotlib.pyplot as plt
import numpy as np
from signal_processing import proposed_expression

def plot_measured_signals(x, I, Dms):
    plt.figure(figsize=(12,8))
    for i in range(I.shape[1]):
        plt.plot(x[:,i], I[:,i], label=r"$\Delta m = {}$".format(Dms[i]))
    plt.xlabel(r"$x (m)$", fontsize = 14)
    plt.ylabel(r"$ I / I_{max} $", fontsize = 14)
    plt.title('Measured interference patterns for different Δm', fontsize = 16)
    plt.legend(fontsize = 12)
    plt.grid()
    plt.show()

def plot_fft(ks, spectrums, Dms):
    for k, spectrum, Dm in zip(ks, spectrums, Dms):
        plt.plot(k, spectrum, 'o', label=r"$\Delta m = {}$".format(Dm))
    plt.xlabel(r"$k (rad/m)$", fontsize = 14)
    plt.xlim(-1800, 1800)
    plt.ylabel("Magnitude of the FFT (u.a.)", fontsize = 14)
    plt.title('Wavenumber spectrum of the measured patterns', fontsize = 16)
    plt.text(200, 67, r"$k_m$: envelope", fontsize = 12)
    plt.text(900, 30, r"$k_c$: carrier", fontsize = 12)
    plt.grid()
    plt.legend(fontsize = 12)
    plt.show()

def plot_filtered_vs_fitted(x, signal_filtered, popt, Dm):
    plt.figure(figsize=(12,8))
    B_fit, C_fit, D_fit, km_fit, kc_fit = popt
    g_sup = B_fit * np.exp(-(km_fit * x)**2 / 2) 
    g_inf = C_fit * np.exp(-(D_fit * x)**2 / 2)
    plt.plot(x, signal_filtered, 'b-', label="Filtered signal")
    plt.plot(x, proposed_expression(x, *popt), 'r-', label="Fitted signal by NLLS")
    plt.plot(x, g_sup, color='grey', linestyle = '--', label = "Upper Gaussian")
    plt.plot(x, g_inf, color='grey', linestyle = '--', label = "Lower Gaussian")
    plt.legend(fontsize = 12)
    plt.xlabel(r"$x (m)$", fontsize = 14)
    plt.ylabel(r"$ I / I_{max} $", fontsize = 14)
    plt.title(r"Fitting of the filtered $\Delta m = 200$  signal", fontsize = 16)
    plt.legend(fontsize = 12)
    plt.text(0.015, 0.7, r"$ \frac{I}{I_{max}} = e^{-\frac{(k_m x)^2}{2}} $", fontsize = 15)
    plt.text(-0.023, 0.25, r"$ \frac{I}{I_{max}} = 0,44·e^{-\frac{(0,7·k_m x)^2}{2}} $", fontsize = 15)
    plt.grid()
    plt.show()

def plot_parameter_trends(Dm, Dm_err, m1, m2,
                          kc, kc_err, mc1, dmc1, mc2, dmc2,
                          kc_lin1, kc_lin2,
                          km, km_err, mm1, dmm1, mm2, dmm2,
                          km_lin1, km_lin2):
    

    text_kc1 = rf"$ k_c \propto ({mc1} \pm {dmc1} \, rad·m^{{-1}}) \Delta m  $"
    text_kc2 = rf"$ k_c \propto ({mc2} \pm {dmc2} \, rad·m^{{-1}}) \Delta m $"
    text_km1 = rf"$ k_m \propto ({mm1} \pm {dmm1} \, rad·m^{{-1}}) \Delta m  $"
    text_km2 = rf"$ k_m \propto ({mm2} \pm {dmm2} \, rad·m^{{-1}}) \Delta m  $"

    fig, ax = plt.subplots(1,2)
            
    ax[0].errorbar(Dm, kc, xerr=Dm_err, yerr=kc_err, color = 'blue', fmt='.', linestyle='None', ecolor = 'black', label=r"$k_c$, interference of the pattern")
    ax[0].plot(m1, kc_lin1, 'b', linestyle='--', label = r"Linear estimation for minors $\Delta m$")
    ax[0].plot(m2, kc_lin2, 'b', linestyle=':', label = r"Linear estimation for largers $\Delta m$")
    ax[0].text(6, 1400, text_kc1, fontsize = 12)
    ax[0].text(40, 950, text_kc2, fontsize = 12)
    ax[0].set_ylabel(r"$k_c (rad/m)$", fontsize = 16)
    ax[0].set_xlabel(r"$\Delta m $", fontsize = 16)
    ax[0].set_title(r"Representation: $k_c$ vs $\Delta m$", fontsize = 18)
    ax[0].tick_params(axis='both', labelsize=12)
    ax[0].grid()
    ax[0].legend(loc = 'lower right', fontsize = 12)

    ax[1].errorbar(Dm, km, xerr=Dm_err, yerr=km_err, color = 'red', fmt='.', linestyle='None', ecolor = 'black', label=r"$k_m$, angular width of the pattern")
    ax[1].plot(m1, km_lin1, 'r', linestyle='--', label = r"Linear estimation for minors $\Delta m$")
    ax[1].plot(m2, km_lin2, 'r', linestyle=':', label = r"Linear estimation for largers $\Delta m$")
    ax[1].text(5, 40, text_km1, fontsize = 12)
    ax[1].text(90, 55, text_km2, fontsize = 12)
    ax[1].set_ylabel(r"$k_m (rad/m)$", fontsize = 16)
    ax[1].set_xlabel(r"$\Delta m $", fontsize = 16)
    ax[1].set_title(r"Representation: $k_m$ vs $\Delta m$", fontsize = 18)
    ax[1].tick_params(axis='both', labelsize=12)
    ax[1].grid()
    ax[1].legend(loc = 'lower right', fontsize = 12)

    plt.show()

 

