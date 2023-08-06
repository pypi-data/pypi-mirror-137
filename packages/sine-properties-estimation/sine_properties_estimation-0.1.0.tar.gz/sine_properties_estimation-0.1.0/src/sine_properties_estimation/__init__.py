from sine_properties_estimation.estimation import SineProperties


def calc_sine_properties(raw_data_1d, total_seconds):
    return SineProperties(raw_data_1d, total_seconds)


if __name__ == "__main__":
    import numpy as np

    # sine with random noise
    samples = 1000
    seconds = 10
    amp_mv = 340
    phase_rad = 2.2
    offset_mv = 60
    freq_ghz = 1.834

    t = np.linspace(0, seconds, samples)
    signal = amp_mv * np.sin(2 * np.pi * freq_ghz * t + phase_rad) + offset_mv + np.random.normal(0, 50, samples)

    estimation = calc_sine_properties(signal, seconds)
    print(f'estimate freq is {estimation.est_freq} Hz')
    print(f'estimated sine amp is {estimation.est_sine_amp}')
    estimation.print_estimation()
