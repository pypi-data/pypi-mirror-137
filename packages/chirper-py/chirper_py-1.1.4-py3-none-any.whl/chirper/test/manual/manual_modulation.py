import numpy as np
import matplotlib.pyplot as plt

from chirper.sgn.defaults import SIN
from chirper.transforms import f1, if1
from chirper.modulation import am_modulation, fm_modulation, pm_modulation

################################################################################################################
################################################################################################################
################################################################################################################


def main(show_fig=False):
    end_time = 2
    sf = 2000
    time = np.linspace(0, end_time, end_time * sf)

    triangle_built = SIN(time, 5, 10) + SIN(time, 10, 5) + SIN(time, 15, 2.5) + \
        SIN(time, 20, 1.25) + SIN(time, 25, 0.625) + SIN(time, 30, 0.3125)

    t_am_mod = am_modulation(triangle_built, 200, 1)
    t_fm_mod = fm_modulation(triangle_built, 200, 1, 0.1)
    t_pm_mod = pm_modulation(triangle_built, 100, 10)

    orig_fourier = f1(triangle_built)
    am_fourier = f1(t_am_mod)
    fm_fourier = f1(t_fm_mod)
    pm_fourier = f1(t_pm_mod)

    orig_inv = if1(orig_fourier)
    am_inv = if1(am_fourier)
    fm_inv = if1(fm_fourier)
    pm_inv = if1(pm_fourier)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    fig.suptitle("FFT")
    ax1.plot(*abs(orig_fourier).unpack(), label="Fourier original")
    ax2.plot(*abs(am_fourier).unpack(), label="Fourier AM modulated")
    ax3.plot(*abs(fm_fourier).unpack(), label="Fourier FM modulated")
    ax4.plot(*abs(pm_fourier).unpack(), label="Fourier PM modulated")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_ylabel("Amplitude (-)")
    ax4.set_ylabel("Amplitude (-)")
    ax4.set_xlabel("Frequency (Hz)")

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    fig.suptitle("Original vs modulated")
    ax1.plot(*triangle_built.unpack(), label="Original")
    ax2.plot(*t_am_mod.unpack(), label="AM Modulated")
    ax3.plot(*t_fm_mod.unpack(), label="FM Modulated")
    ax4.plot(*t_pm_mod.unpack(), label="PM Modulated")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_ylabel("Amplitude (-)")
    ax4.set_ylabel("Amplitude (-)")
    ax4.set_xlabel("Time (s)")

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    fig.suptitle("Reconstructed signals")
    ax1.plot(*orig_inv.real_part().unpack(),
             label="Original reconstructed (Re)")
    ax1.plot(*orig_inv.imag_part().unpack(),
             label="Original reconstructed (Im)")
    ax2.plot(*am_inv.real_part().unpack(),
             label="AM Modulated reconstructed (Re)")
    ax2.plot(*am_inv.imag_part().unpack(),
             label="AM Modulated reconstructed (Im)")
    ax3.plot(*fm_inv.real_part().unpack(),
             label="FM Modulated reconstructed (Re)")
    ax3.plot(*fm_inv.imag_part().unpack(),
             label="FM Modulated reconstructed (Im)")
    ax4.plot(*pm_inv.real_part().unpack(),
             label="PM Modulated reconstructed (Re)")
    ax4.plot(*pm_inv.imag_part().unpack(),
             label="PM Modulated reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax3.set_ylabel("Amplitude (-)")
    ax4.set_ylabel("Amplitude (-)")
    ax4.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    fig.suptitle("Reconstructed vs originals")
    ax1.plot(*triangle_built.unpack(), label="Original")
    ax2.plot(*orig_inv.real_part().unpack(),
             label="Original reconstructed (Re)")
    ax2.plot(*orig_inv.imag_part().unpack(),
             label="Original reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    fig.suptitle("Reconstructed vs originals")
    ax1.plot(*t_am_mod.unpack(), label="AM Modulated")
    ax2.plot(*am_inv.real_part().unpack(),
             label="AM Modulated reconstructed (Re)")
    ax2.plot(*am_inv.imag_part().unpack(),
             label="AM Modulated reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    fig.suptitle("Reconstructed vs originals")
    ax1.plot(*t_fm_mod.unpack(), label="FM Modulated")
    ax2.plot(*fm_inv.real_part().unpack(),
             label="FM Modulated reconstructed (Re)")
    ax2.plot(*fm_inv.imag_part().unpack(),
             label="FM Modulated reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    fig.suptitle("Reconstructed vs originals")
    ax1.plot(*t_pm_mod.unpack(), label="PM Modulated")
    ax2.plot(*pm_inv.real_part().unpack(),
             label="PM Modulated reconstructed (Re)")
    ax2.plot(*pm_inv.imag_part().unpack(),
             label="PM Modulated reconstructed (Im)")
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    ax1.set_ylabel("Amplitude (-)")
    ax2.set_ylabel("Amplitude (-)")
    ax2.set_xlabel("Time (s)")

    if show_fig:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(True)
