import numpy as np
import math


def rms(signal):
    return np.mean(signal ** 2.0, axis=0) ** 0.5


def lcm(num1, num2):
    return num1 * num2 / math.gcd(num1, num2)


def next_power_2(x: int):
    value = 1
    while value <= x:
        value = value << 1
    return value


def fit_spectrum(time_signal, time_shape_constrain, target_spectrum):
    n = time_signal.shape[0]

    if np.mod(n, 2) == 0:
        n_uniq_freq = int((n / 2 + 1))
    else:
        n_uniq_freq = int((n + 1) / 2)

    error = np.inf
    tol = 1e-10
    delta_error = np.inf
    _fft = np.fft.rfft(time_signal, axis=0)
    n_iter = 1
    fitted_signal = None
    while (delta_error > tol) and (n_iter < 1000):
        _phase = np.angle(_fft)
        # reconstruct full fft
        full_spectrum = target_spectrum * np.exp(1j * _phase)
        fitted_signal = np.fft.irfft(full_spectrum, n, axis=0) * time_shape_constrain
        _fft = np.fft.rfft(fitted_signal, axis=0)
        current_error = np.std(np.abs(_fft[range(n_uniq_freq)] - target_spectrum))
        delta_error = abs(error - current_error)
        error = current_error
        n_iter = n_iter + 1
        print('error: {:.6f}'.format(error))

    print('n_iter: {:}'.format(n_iter))
    return fitted_signal


def generate_modulated_noise(fs: float = 44100.0,
                             duration: float = 1.0,  # duration in seconds
                             n_channels=1,  # number of channels to be generated
                             n_repetitions: int = 1,  # sampling frequency
                             amplitude: float = 1.0,  # between -1 and 1
                             f_noise_low: float = 300.0,  # phase in rad
                             f_noise_high: float = 700.0,  # phase in rad
                             attenuation: float = 0.0,  # in dB, 3 for pink noise
                             modulation_frequency: float = 0.0,  # frequency in Hz
                             modulation_phase: float = 0.0,  # frequency in Hz
                             modulation_index: float = 0.0,  # frequency in Hz
                             round_next_power_2: bool = False,
                             reference_rms: bool = None,
                             noise_seed=None):
    if noise_seed is not None:
        np.random.seed(noise_seed)
    time = np.expand_dims(np.arange(0, np.round(fs * duration)) / fs, axis=1)
    n = time.size
    if np.mod(n, 2) == 0:
        n_uniq_freq = int((n / 2 + 1))
    else:
        n_uniq_freq = int((n + 1) / 2)

    freq = np.arange(0, n_uniq_freq) * fs / n
    p = -attenuation / (20 * np.log10(0.5))
    amp_noise = np.zeros((n_uniq_freq, 1))

    # defining spectral magnitude
    for _i in np.arange(1, n_uniq_freq):
        f = freq[_i]
        if (f >= f_noise_low) and (f <= f_noise_high):
            amp_noise[_i] = 1 / (f ** p)
        else:
            amp_noise[_i] = 0

    # Phase generation
    phase_noise = 2 * np.pi * np.random.rand(n_uniq_freq, n_channels)
    spectrum_noise = amp_noise * np.exp(1j * phase_noise)

    # synthesized noise
    noise = np.fft.irfft(spectrum_noise, n, axis=0)
    # modulated noise
    mod_amp = (1 - modulation_index * np.cos(2 * np.pi * modulation_frequency * time + modulation_phase)) / \
              (1 + modulation_index)
    _amplitude = amplitude * mod_amp
    noise = noise / np.max(np.abs(noise), axis=0)
    noise = _amplitude * noise
    if reference_rms:
        noise = reference_rms / rms(noise) * noise  # normalize noise to have required rms
    value = np.tile(noise, n_repetitions)
    return value
