from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

from chirper.config import CONVOLUTION_METHOD, CROSS_CORRELATION_METHOD, KERNEL_OOB
from chirper.exceptions import DimensionError
if TYPE_CHECKING:
    from chirper.sgn import Signal1, Signal2

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def convolution(s1_x: Signal1, s1_y: Signal1,
                method=CONVOLUTION_METHOD) -> Signal1:
    """Calculates the convolution of two one-dimensional signals.

    There are different methods to calculate the convolution of two
    signals. The ones currently implemented are:
     - "fft": Uses the property that convolution in the time domain
        translates into multiplication in the frequency domain.
        That way, one can use the FFT to calculate the Fourier
        transforms of both signals (which is done really quickly),
        multiplies the spectra and then applies the inverse.

     - "direct" : Uses the formula of convolution to calculate it via
        brute-force. Very inneficient, as it is O(N*M).

    Parameters
    ----------
    s1_x : Signal1
        First one-dimensional signal to convolute.
    s1_y : Signal1
        Second one-dimensional signal to convolute.
    method : {"fft", "direct"}, optional
        Method used for the convolution, by default CONVOLUTION_METHOD.

    Returns
    -------
    Signal1
        Convoluted signal.
    """
    conv_methods = {
        "fft": conv_fft,
        "direct": conv_direct,
    }
    return conv_methods[method](s1_x, s1_y)


def conv_fft(s1_x: Signal1, s1_y: Signal1) -> Signal1:
    """Convolutes using the FFT."""
    from chirper.transforms import f1, if1
    x_fourier = f1(s1_x)
    y_fourier = f1(s1_y)
    return if1(x_fourier * y_fourier)


def conv_direct(s1_x: Signal1, s1_y: Signal1) -> Signal1:
    """Convolutes via brute-force."""
    x_copy = s1_x.clone()
    y_copy = s1_y.clone()
    if not np.array_equal(x_copy.axis, y_copy.axis):
        raise DimensionError("Dimensions of signals do not match.")
    vals = []
    for n, _ in enumerate(x_copy.values):
        sum = 0
        for m, _ in enumerate(y_copy.values):
            sum += x_copy.values[m] * y_copy.values[n - m]
        vals.append(sum)
    output = s1_x.clone()
    output.values = np.array(vals)
    return output


def cross_correlation(s1_x: Signal1, s1_y: Signal1,
                      method=CROSS_CORRELATION_METHOD) -> Signal1:
    """Calculates the cross correlation of two signals.

    Parameters
    ----------
    s1_x : Signal1
        First signal.
    s1_y : Signal1
        Second signal
    method : {"fft", "direct"}, optional
        Desired method to calculate the cross correlation, by default
        CROSS_CORRELATION_METHOD.

    Returns
    -------
    Signal1
        Cross correlated signal
    """
    cc_methods = {
        "fft": cc_fft,
        "direct": cc_direct,
    }
    return cc_methods[method](s1_x, s1_y)


def cc_direct(s1_x: Signal1, s1_y: Signal1) -> Signal1:
    x_copy = s1_x.clone()
    y_copy = s1_y.clone()
    if not np.array_equal(x_copy.axis, y_copy.axis):
        raise DimensionError("Dimensions of signals do not match.")
    vals = []
    for n, _ in enumerate(x_copy.values):
        sum = 0
        for m, _ in enumerate(y_copy.values):
            sum += np.conjugate(x_copy.values[m]) * \
                y_copy.values[(m + n) % len(x_copy)]
        vals.append(sum)
    output = s1_x.clone()
    output.values = np.array(vals)
    return output


def cc_fft(s1_x: Signal1, s1_y: Signal1) -> Signal1:
    from chirper.transforms import f1, if1
    x_copy = s1_x.clone()
    y_copy = s1_y.clone()
    x_fourier = f1(x_copy)
    y_fourier = f1(y_copy)
    return if1(x_fourier.conjugate() * y_fourier)

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Signal2 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def apply_kernel(signal2: Signal2, kernel: np.ndarray, flip=False,
                 oob=KERNEL_OOB) -> Signal2:
    """Applies a given kernel to the two dimensional signal.

    This operation can be often found in the literature as image
    convolution.

    Predefined kernels can be found within `chirper.kernel`, but a
    custom one can be given without a problem.

    Parameters
    ----------
    signal2 : Signal2
        Signal to apply the kernel to.
    kernel : np.ndarray
        Kernel used for the operation.
    flip : bool, optional
        Whether to flip the kernel or not, by default False.
    oob : {"zero"}, optional
        Determines how to handle the values out of the signal. For
        example, when `oob` is `"zero"` then, when trying to get
        the 6th element of a 5x5 signal you will just get a 0. By
        default KERNEL_OOB.

    Returns
    -------
    Signal2
        Signal with the kernel applied to it.
    """
    copy = signal2.clone()
    signal_shape = copy.shape()
    result = np.empty((signal_shape))
    ker_copy = kernel.copy().T if flip else kernel.copy()
    ker_shape = np.shape(ker_copy)
    for i in range(signal_shape[0]):
        for j in range(signal_shape[1]):
            sum = 0
            for row, col, ker_row, ker_col in _generate_indices(ker_shape, i, j):
                sum += _get(copy, row, col, oob) * ker_copy[ker_row, ker_col]
            result[i, j] = sum
    copy.values = result
    return copy


def _get(signal2: Signal2, row, col, oob=KERNEL_OOB):
    methods = {
        "zero": _get_zero,
    }
    copy = signal2.clone()
    row_total, col_total = copy.shape()
    if (0 <= row < row_total) and (0 <= col < col_total):
        return signal2[row, col]
    else:
        return methods[oob](signal2, row, col)


def _get_zero(signal2: Signal2, row, col):
    return 0


def _generate_indices(ker_shape, row, col):
    ker_rows, ker_cols = ker_shape
    center = ((ker_rows - 1) // 2, (ker_cols - 1) // 2)
    return [
        (row + i, col + j, center[0] + i, center[1] + j)
        for i in range(-center[0], center[0] + 1)
        for j in range(-center[1], center[1] + 1)
    ]

########################################################################################################################
# ||||||||||||||||||||||||||||||||||||||||||||||||| Others ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################
