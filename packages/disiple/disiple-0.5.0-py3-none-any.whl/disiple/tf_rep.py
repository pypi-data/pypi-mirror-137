from math import floor, ceil
import numpy as np


def overlapping_triangular_filterbank(center_freqs, fft_size, samplerate, normalize=True):
    delta_freq = samplerate / fft_size
    center_indices = np.rint(center_freqs / delta_freq).astype(int)
    filterbank = np.zeros((len(center_freqs), fft_size//2+1))
    middle_start_indices = np.floor(center_freqs[:-2] / delta_freq).astype(int)
    start_indices = np.concatenate(([middle_start_indices[0]+1], middle_start_indices, [floor(center_freqs[-2] / delta_freq)]))
    center_indices = np.rint(center_freqs / delta_freq).astype(int)
    middle_end_indices = np.ceil(center_freqs[2:] / delta_freq).astype(int)
    end_indices = np.concatenate(([ceil(center_freqs[1] / delta_freq)], middle_end_indices, [middle_end_indices[-1]-1]))
    for filt, start, center, end in zip(filterbank, start_indices, center_indices, end_indices):
        filt[start:center+1] = np.linspace(0, 1, center-start+1, True)
        filt[center:end+1] = np.linspace(1, 0, end-center+1, True)
    if normalize:
        norm = filterbank.sum(axis=1, keepdims=True) * delta_freq
        norm[0] *= 2
        norm[-1] *= 2
        filterbank /= norm
    return filterbank


def mel_filterbank(samplerate, fft_size, num_filters, min_freq=0, max_freq=None, normalize=True):
    min_freq, max_freq = _sanitize_freq_extrema(samplerate, min_freq, max_freq)
    center_mels, center_freqs = mel_frequencies(num_filters, min_freq, max_freq)
    mel_filterbank = overlapping_triangular_filterbank(center_freqs, fft_size, samplerate, normalize)
    return center_mels, center_freqs, mel_filterbank


def twelve_tet_filterbank(samplerate, fft_size, bins_per_semitone, min_freq=20, max_freq=None, normalize=True, a4=440):
    nyquist_freq = samplerate / 2
    if not max_freq:
        max_freq = nyquist_freq
    if min_freq <= 0:
        raise ValueError('The minimum frequency needs to be strictly positive')
    min_freq = _nearest_12tet_freq(min_freq, lower=20, a4=a4)
    max_freq = _nearest_12tet_freq(max_freq, upper=nyquist_freq, a4=a4)
    if min_freq >= max_freq:
        raise ValueError('The minimum frequency needs to be smaller than the maximum frequency')
    center_midis, center_freqs = twelve_tet_frequencies(bins_per_semitone, min_freq, max_freq, a4)
    twelve_tet_filterbank = overlapping_triangular_filterbank(center_freqs, fft_size, samplerate, normalize)
    return center_midis, center_freqs, twelve_tet_filterbank


def mel_frequencies(num_filters, min_freq, max_freq):
    max_mel = _freq2mel(max_freq)
    min_mel = _freq2mel(min_freq)
    center_mels = np.linspace(min_mel, max_mel, num_filters+2)
    center_freqs = _mel2freq(center_mels)
    return center_mels, center_freqs


def twelve_tet_frequencies(bins_per_semitone, min_freq, max_freq, a4=440):
    min_midi = _freq2midi(min_freq, a4)
    max_midi = _freq2midi(max_freq, a4)
    if not (min_midi * bins_per_semitone).is_integer():
        raise ValueError('The minimum frequency {} Hz does not belong to the {}12-TET scale with reference {} Hz'.format(min_freq, f'1/{bins_per_semitone}-fractional ' if bins_per_semitone > 1 else '', a4))
    if not (max_midi * bins_per_semitone).is_integer():
        raise ValueError('The maximum frequency {} Hz does not belong to the {}12-TET scale with reference {} Hz'.format(min_freq, f'1/{bins_per_semitone}-fractional ' if bins_per_semitone > 1 else '', a4))
    center_midis = np.linspace(min_midi, max_midi, round((max_midi-min_midi)*bins_per_semitone)+1)
    center_freqs = _midi2freq(center_midis, a4)
    return center_midis, center_freqs


def _sanitize_freq_extrema(samplerate, min_freq, max_freq):
    nyquist_freq = samplerate / 2
    if not max_freq or max_freq > nyquist_freq:
        max_freq = nyquist_freq
    if min_freq >= max_freq or min_freq < 0:
        raise ValueError('The minimum frequency needs to be positive and smaller than the maximum frequency')
    return min_freq, max_freq


def _delta_freq_mel(num_bins, min_freq, max_freq):
    max_mel = _freq2mel(max_freq)
    min_mel = _freq2mel(min_freq)
    return _mel2freq(min_mel + (max_mel - min_mel) / (num_bins + 1))


def _delta_freq_12tet(freq, bins_per_semitone):
    return freq * (2 ** (1 / bins_per_semitone / 12) - 1)


def _delta_y_for_spacing(spacing, num_bins, min_freq, max_freq, samplerate):
    if spacing == 'mel':
        max_mel = _freq2mel(max_freq)
        min_mel = _freq2mel(min_freq)
        return (max_mel - min_mel) / (num_bins + 1)
    if spacing == 'log':
        return 1 / num_bins
    if spacing == 'linear':
        return samplerate / num_bins


def _fft_size_for_spacing(spacing, num_bins, samplerate, min_freq, max_freq):
    if spacing == 'mel':
        return ceil(samplerate / _delta_freq_mel(num_bins/2, min_freq, max_freq))
    if spacing == 'log':
        return ceil(samplerate / _delta_freq_12tet(min_freq, num_bins / 2))
    return num_bins


def _nextpow2(value):
    return np.ceil(np.log2(np.abs(value))).astype(int)


def _freq2mel(f):
    return 1000 * np.log(1 + f / 700) / np.log(1 + 1000 / 700)


def _mel2freq(m):
    return 700 * (np.exp(m * np.log(1 + 1000 / 700) / 1000) - 1)


def _freq2midi(f, a4=440):
    return 69 + 12 * np.log2(f / a4)


def _midi2freq(m, a4=440):
    return a4 * 2 ** ((m - 69) / 12)


def _nearest_12tet_freq(freq, lower=None, upper=None, a4=440):
    freq_12tet = _midi2freq(np.round(_freq2midi(freq, a4)), a4)
    if lower is not None:
        lower_12tet = _midi2freq(np.ceil(_freq2midi(lower, a4)), a4)
        freq_12tet = np.where(freq_12tet < lower_12tet, lower_12tet, freq_12tet)
    if upper is not None:
        upper_12tet = _midi2freq(np.floor(_freq2midi(upper, a4)), a4)
        freq_12tet = np.where(freq_12tet > upper_12tet, upper_12tet, freq_12tet)
    return freq_12tet
