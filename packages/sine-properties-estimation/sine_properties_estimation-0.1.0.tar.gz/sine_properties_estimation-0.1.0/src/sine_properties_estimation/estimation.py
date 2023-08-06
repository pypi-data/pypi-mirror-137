import numpy as np
import pandas as pd
import scipy.signal
from dict_aligned_print import print_dict


def freq_by_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    https://gist.github.com/endolith/255291
    https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html
    """

    def parabolic(f, x):
        """Quadratic interpolation for estimating the true position of an
        inter-sample maximum when nearby samples are known.

        f is a vector of amplitudes and i is an index for max value at that vector.

        Returns (vx, vy), the coordinates of the vertex of a parabola that goes
        through point i and its two neighbors.

        Example:
        Defining a vector f with a local maximum at index 3 (= 6), find local
        maximum if points 2, 3, and 4 actually defined a parabola.

        In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]

        In [4]: parabolic(f, argmax(f))
        Out[4]: (3.2142857142857144, 6.1607142857142856)

        """
        # Requires real division.  Insert float() somewhere to force it?
        xv = 1 / 2 * (f[x - 1] - f[x + 1]) / (f[x - 1] - 2 * f[x] + f[x + 1]) + x
        yv = f[x] - 1 / 4 * (f[x - 1] - f[x + 1]) * (xv - x)
        return xv, yv

    # Compute Fourier transform of windowed signal
    sig = sig.copy()
    sig -= np.mean(sig)
    windowed = sig * scipy.signal.blackmanharris(len(sig))
    f = np.fft.rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = np.argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = parabolic(np.log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)


def find_amp_phase_by_ls(values, time, freq):
    def _phase_from_A_B(A, B, C):
        """
            C*sin(w*t+phase)=C*sin(w*t)*cos(phase)+C*cos(w*t)*sin(phase)
            C*sin(w*t+phase)=A*sin(w*t)           +B*cos(w*t)
            A=C*cos(phase) -> can only tell if left (minus) or right (plus)
            B=C*sin(phase) -> can only tell if down (minus) or up    (plus)
        """
        if B == 0:  # we have only sin(wt) so phase is 0
            return 0
        if A == 0:  # we have only cos(wt) so phase is pi/2
            return np.pi / 2

        cos_ang = np.arccos(A / C)
        sin_ang = np.arcsin(B / C)
        quarter = dict(up_right=[1, cos_ang],
                       up_left=[2, cos_ang],
                       down_left=[3, 2 * np.pi - cos_ang],
                       down_right=[4, 2 * np.pi - cos_ang])

        vertical = 'up' if sin_ang > 0 else 'down'
        horizontal = 'right' if cos_ang < (np.pi / 2) else 'left'

        return quarter['%s_%s' % (vertical, horizontal)][1]

    def _amp_from_A_B(A, B):
        return float(np.sqrt(A ** 2 + B ** 2))

    def _estimate_A_B_for_sine(values, time, freq):
        df = pd.DataFrame()
        df['value'] = values
        df['time'] = time

        df['internal'] = 2 * np.pi * freq * df.time
        df['sin'] = np.sin(df.internal)
        df['cos'] = np.cos(df.internal)
        df['ones'] = 1

        y = np.mat(df.value.values).T
        x = np.mat(df[['sin', 'cos', 'ones']].values)
        try:
            h = x.I * y  # pseudo inverse which is (x.T * x).I * x.T * y
        except:
            '''happened to me when estimated frequency is 0. you should remove DC before FFT'''
            print("{:*^150}".format('singular matrix (probably estimated freq is 0), cannot resolve this case. returning dummy values for amp and phase!!!'))
            return 0, 0, 0

        A, B, offset = h.A1.astype(float)
        return A, B, offset

    A, B, offset = _estimate_A_B_for_sine(values, time, freq)
    # estimating offset by average is wrong, for example if you have 2.5 cycles, the half cycle will change the average!
    amp = _amp_from_A_B(A, B)
    phase = _phase_from_A_B(A, B, amp)
    return amp, phase, offset


class SineProperties:
    def __init__(self, raw_data_1d, total_seconds):
        self.raw_data_1d = np.array(raw_data_1d)
        self.total_seconds = total_seconds
        self.samples = len(raw_data_1d)
        self.seconds_between_adjacent_samples = total_seconds / self.samples

        t = np.linspace(0, total_seconds, self.samples)
        self.est_freq = freq_by_fft(raw_data_1d, fs=1 / self.seconds_between_adjacent_samples)
        self.est_sine_amp, self.est_phase_rad, self.est_offset = find_amp_phase_by_ls(raw_data_1d, t, self.est_freq)

    def __str__(self):
        d = dict(samples=self.samples,
                 total_seocnds=self.total_seconds,
                 freq=self.est_freq,
                 sine_amp=self.est_sine_amp,
                 phase_rad=self.est_phase_rad,
                 offset=self.est_offset)
        return print_dict(d, return_instead_of_print=True)

    def __repr__(self):
        return self.__str__()

    def print_estimation(self):
        print(self.__str__())
