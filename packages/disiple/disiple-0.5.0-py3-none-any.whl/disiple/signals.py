from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from math import sqrt, ceil
import warnings
import numpy as np
from scipy import fft, signal
from IPython.display import display
from miniaudio import get_file_info, decode_file, SampleFormat, DecodeError
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.ranges import DataRange1d
from bokeh.models.tools import PanTool, BoxZoomTool, WheelZoomTool, ZoomInTool, ZoomOutTool, SaveTool, ResetTool, HoverTool, InspectTool
from bokeh.palettes import Viridis256
from bokeh.io import output_notebook
from .util import Audio, _read_aiff_file, _resample
from .tf_rep import mel_filterbank, twelve_tet_filterbank, _fft_size_for_spacing


try:
    ipyname = get_ipython().__class__.__name__
    ipymodule = get_ipython().__class__.__module__
    if ipyname == 'ZMQInteractiveShell' or ipymodule == 'google.colab._shell':
        output_notebook()
except NameError:
    pass


def get_samples_and_rate(input_signal, samplerate):
    if isinstance(input_signal, TimeSignal):
        if samplerate is not None:
            print('Explicitly defined samplerate gets ignored when input is a TimeSignal', samplerate)
        samples = input_signal.samples
        samplerate = input_signal.samplerate
    elif np.ndim(input_signal) > 0:
        if samplerate is None:
            raise ValueError('The samplerate needs to be defined explicitly when input is an array or other iterable')
        samples = np.asarray(input_signal)
    else:
        raise TypeError('Only TimeSignals, Numpy arrays or other iterables are supported as input, not {}'.format(type(input_signal)))
    return samples, samplerate


def get_samples(input_signal):
    if isinstance(input_signal, TimeSignal):
        return input_signal.samples
    elif np.ndim(input_signal) > 0:
        return np.asarray(input_signal)
    else:
        raise TypeError('Only TimeSignals, Numpy arrays or other iterables are supported as input, not {}'.format(type(input_signal)))


def _get_compatible_samples(ref_signal, other):
    if isinstance(other, TimeSignal):
        if ref_signal.samplerate != other.samplerate:
            raise ValueError('Signals need to have the same sample rates')
        other_samples = other.samples
    else:
        other_samples = np.asarray(other)
    if np.issubdtype(other_samples.dtype, np.number):
        return other_samples
    raise TypeError('Only TimeSignals or numeric iterables are supported as operands, not {}'.format(type(other)))


def _get_compatible_size_samples(ref_signal, other):
    other_samples = _get_compatible_samples(ref_signal, other)
    if other_samples.size != ref_signal.samples.size:
        raise ValueError('Signals need to have the same size')
    return other_samples


def get_both_samples_and_rate(input_signal1, input_signal2, samplerate=None):
    samples1, samplerate1 = get_samples_and_rate(input_signal1, samplerate)
    samples2, samplerate2 = get_samples_and_rate(input_signal2, samplerate)
    if samplerate1 != samplerate2:
        raise ValueError('Both signals need to have the same samplerate')
    return samples1, samples2, samplerate1


def get_both_samples(input_signal1, input_signal2):
    samples1 = get_samples(input_signal1)
    samples2 = get_samples(input_signal2)
    if isinstance(input_signal1, TimeSignal) and isinstance(input_signal2, TimeSignal) and input_signal1.samplerate != input_signal2.samplerate:
        raise ValueError('Both signals need to have the same samplerate')
    return samples1, samples2


def same_type_as(output_samples, input_signal):
    if isinstance(input_signal, TimeSignal):
        return type(input_signal)(output_samples, input_signal.samplerate)
    else:
        return output_samples


class Signal(ABC):
    """Abstract base class defining a generic signal.
    """
    @abstractmethod
    def plot(self, **fig_args):
        pass


    def _repr_html_(self):
        return show(self.plot())


    def display(self, **fig_args):
        show(self.plot(**fig_args))


class TimeSignal(Signal):
    """A class representing a sampled time-signal.
    """
    def __init__(self, in_data, samplerate=None):
        if isinstance(in_data, Spectrogram):
            if in_data.spacing != 'linear':
                raise ValueError('Inversion of non-linear spectrograms is not supported')
            if not signal.check_NOLA(in_data.window, in_data._frame_size, in_data._overlap_size):
                raise ValueError('A spectrogram created with this combination of parameters cannot be inverted')
            if not signal.check_COLA(in_data.window, in_data._frame_size, in_data._overlap_size):
                warnings.warn('A spectrogram created with this combination of parameters cannot be perfectly inverted')
            self.times, self.samples = signal.istft(
                in_data.complex, in_data._input_samplerate, in_data.window,
                in_data._frame_size, in_data._overlap_size, in_data._fft_size,
            )
            self.samples = np.clip(self.samples, -1, 1)
            self.samplerate = in_data._input_samplerate
        else:
            if isinstance(in_data, Spectrum):
                self.samples = fft.irfft(in_data.complex, in_data._fft_size, norm='forward')
                self.samplerate = in_data._input_samplerate
            else:
                if samplerate is None:
                    raise ValueError('Specify sample rate when creating TimeSignal from samples')
                self.samples = in_data
                self.samplerate = samplerate
            self.times = np.arange(len(self.samples)) / self.samplerate


    def plot(self, **fig_args):
        default_args = {
            'width': 900, 'height': 300,
            'x_axis_label': 'time [s]', 'y_axis_label': 'amplitude',
            'tools': 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,save,reset',
            'active_drag': 'pan',
            'toolbar_location': 'above',
        }
        fig = figure(**{**default_args, **fig_args})
        fig.line(self.times, self.samples, line_width=2)
        return fig


    def __len__(self):
        return len(self.times)


    def __add__(self, other):
        if np.isscalar(other):
            return same_type_as(self.samples + other, self)
        other_samples = _get_compatible_size_samples(self, other)
        return same_type_as(self.samples + other_samples, self)


    def __mul__(self, other):
        if np.isscalar(other):
            return same_type_as(self.samples * other, self)
        other_samples = _get_compatible_size_samples(self, other)
        return same_type_as(self.samples * other_samples, self)


    def __and__(self, other):
        if np.isscalar(other):
            return same_type_as(np.tile(self.samples, other), self)
        other_samples = _get_compatible_samples(self, other)
        return same_type_as(np.concatenate((self.samples, other_samples)), self)


    def rms(self):
        return sqrt(self.power(dB=False))


    def power(self, dB=True):
        power = np.mean(self.samples ** 2)
        return 10*np.log10(power) if dB else power


    def filter(self, coefficients):
        if isinstance(coefficients, tuple):
            if len(coefficients) == 1:
                numerator, = coefficients
                denominator = 1
            else:
                numerator, denominator = coefficients
                filtered_samples = signal.lfilter(numerator, denominator, self.samples)
        else:
            filtered_samples = signal.lfilter(coefficients, 1, self.samples)
        return same_type_as(filtered_samples, self)


    def resample(self, samplerate):
        resampled_signal = deepcopy(self)
        if samplerate != self.samplerate:
            resampled_signal.samplerate = samplerate
            resampled_signal.samples = _resample(self.samples, self.samplerate, samplerate)
            resampled_signal.times = np.arange(len(resampled_signal.samples)) / samplerate
        return resampled_signal


    def frames(self, frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None):
        return [same_type_as(frame_samples, self) for frame_samples in self.frame_data(
            frame_duration, frame_size, step_duration, step_size, step_ratio).T]


    def frame_data(self, frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None):
        frame_size, overlap_size = _parse_frame_params(frame_duration, frame_size, step_duration, step_size, step_ratio,
                                                       self.samplerate, 'linear', None)
        step_size = frame_size - overlap_size
        samples = np.pad(self.samples, (frame_size//2, 0), 'constant')
        num_frames = ((len(samples)-frame_size//2) // step_size) + 1
        num_fill_samples = (num_frames-1)*step_size+frame_size-len(samples)
        if num_fill_samples > 0:
            samples = np.pad(samples, (0, num_fill_samples), 'constant')
        return np.array([samples[i:i+frame_size] for i in range(0, len(samples)-frame_size+1, step_size)]).T


class AudioSignal(TimeSignal):
    """A class representing an audio signal with sample values between -1 and 1.
    
    Has playback functionality through the play() method.
    """
    def __init__(self, in_data, samplerate=None):
        if isinstance(in_data, (str, Path)):
            try:
                if samplerate is None:
                    file_info = get_file_info(in_data)
                    samplerate = file_info.sample_rate
                decoded_file = decode_file(filename=in_data, output_format=SampleFormat.FLOAT32,
                                           nchannels=1, sample_rate=samplerate)
                samples = np.asarray(decoded_file.samples)
            except DecodeError as decode_error:
                try:
                    samples, file_samplerate = _read_aiff_file(in_data, mix_to_mono=True)
                    if samplerate is None:
                        samplerate = file_samplerate
                    elif samplerate != file_samplerate:
                        samples = _resample(samples, file_samplerate, samplerate)
                except:
                    raise decode_error
            super().__init__(samples, samplerate)
        else:
            super().__init__(in_data, samplerate)


    def play(self, normalize=False):
        return display(Audio(self.samples, rate=self.samplerate, normalize=normalize))


    def plot(self, **fig_args):
        default_args = {
            'width': 900, 'height': 300,
            'x_axis_label': 'time [s]', 'y_axis_label': 'amplitude',
            'y_range': (-1.09, 1.09),
            'tools': [
                PanTool(dimensions='width'),
                BoxZoomTool(),
                WheelZoomTool(dimensions='width'),
                ZoomInTool(dimensions='width'),
                ZoomOutTool(dimensions='width'),
                SaveTool(),
                ResetTool(),
            ],
            'active_drag': 'auto',
            'active_inspect': 'auto',
            'active_scroll': 'auto',
            'toolbar_location': 'above',
            'tooltips': [('time [s]', '@x{0.000}'), ('amplitude', '@y{0.000}')],
        }
        kwargs = {**default_args, **fig_args}
        if kwargs['tooltips'] is not None:
            kwargs['tools'].append(HoverTool(mode='vline'))
        fig = figure(**kwargs)
        fig.line(self.times, self.samples, line_width=2)
        return fig


class Spectrum(Signal):
    """ A class representing a complex spectrum.
    """
    def __init__(
        self, in_data, *,
        dB=True, min_freq=None, max_freq=None, num_bins=None,
        norm_single_side_band=False, spacing='linear', window=None, exponent=1,
        samplerate=None,
    ):
        samples, samplerate = get_samples_and_rate(in_data, samplerate)

        self._input_samplerate = samplerate
        self.spacing = spacing
        self.window = window
        self.exponent = exponent
        self._norm_single_side_band = norm_single_side_band
        self.dB = dB

        if max_freq is None:
            max_freq = samplerate / 2
        if min_freq is not None and min_freq < 1 / len(samples):
            raise ValueError('The given minimum frequency is too small for a signal of this length')
        if spacing == 'log':
            if num_bins is None:
                raise ValueError(f'The number of bins per semitone needs to be given as "num_bins" when requesting {spacing}-spaced frequencies')
            if min_freq is None or min_freq <= 0 or min_freq >= max_freq:
                raise ValueError(f'A minimum frequency above 0 and below the maximum frequency needs to be given when requesting {spacing}-spaced frequencies')
        elif spacing == 'linear':
            if num_bins is None:
                num_bins = len(samples)
        else:
            raise ValueError('The frequency spacing needs to be one of "linear", "log" or "mel"')

        self._fft_size = max(len(samples), _fft_size_for_spacing(spacing, num_bins, samplerate, min_freq, max_freq))
        if window is not None:
            samples = samples * signal.get_window(window, len(samples), True) # do not multiply in place, otherwise in_data gets overwritten
        spectrum = fft.rfft(samples, self._fft_size, norm='forward')
        filtered_spectrum, self.frequencies, self._bin_values = _spacing_filter(spectrum, spacing, samplerate, min_freq, max_freq, self._fft_size, num_bins)
        self.magnitude = np.abs(filtered_spectrum)
        self.phase = np.angle(filtered_spectrum)

        if norm_single_side_band:
            if self._fft_size % 2 == 0:
                self.magnitude[1:-1] *= sqrt(2)
            else:
                self.magnitude[1:] *= sqrt(2)
        if dB:
            self.magnitude = 20 * np.log10(np.clip(self.magnitude, 1e-6, None))
        else:
            self.magnitude **= exponent


    def plot(self, **fig_args):
        freq_label = _freq_label(self.spacing)
        default_args = {
            'width': 900, 'height': 300,
            'x_axis_label': freq_label, 'y_axis_label': 'magnitude',
            'tools': [
                PanTool(),
                BoxZoomTool(),
                WheelZoomTool(),
                ZoomInTool(),
                ZoomOutTool(),
                SaveTool(),
                ResetTool(),
            ],
            'active_drag': 'auto',
            'active_inspect': 'auto',
            'active_scroll': 'auto',
            'toolbar_location': 'above',
            'tooltips': [('frequency [Hz]', '@frequency{0.000}'), ['magnitude', '@magnitude{0.000}']],
        }
        if self.spacing in ('mel', 'log'):
            default_args['tooltips'].insert(0, (freq_label, '@bins{0.0}'))
        if self.exponent == 2 or self.dB:
            default_args['y_axis_label'] = 'power'
            default_args['tooltips'][-1][0] = 'power'
        if self.dB:
            default_args['y_axis_label'] += ' [dB]'
            default_args['tooltips'][-1][0] += ' [dB]'
        kwargs = {**default_args, **fig_args}
        if kwargs['tooltips'] is not None:
            kwargs['tools'].append(HoverTool(mode='vline'))
        fig = figure(**kwargs)
        if isinstance(fig.x_range, DataRange1d):
            fig.x_range.range_padding = 0
        if isinstance(fig.y_range, DataRange1d):
            fig.y_range.range_padding = 0
        data_source = ColumnDataSource({'magnitude': self.magnitude, 'frequency': self.frequencies, 'bins': self._bin_values})
        fig.line(x='bins', y='magnitude', line_width=2, source=data_source)
        return fig


    def __len__(self):
        return len(self.frequencies)


    def rms(self):
        return sqrt(self.power(dB=False))


    def power(self, dB=True):
        if self.dB:
            power_per_freq = 10 ** (self.magnitude / 10)
        else:
            power_per_freq = self.magnitude ** (2/self.exponent)
        if self._norm_single_side_band:
            power = np.sum(power_per_freq)
        elif self._fft_size % 2 == 0:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:-1]) + power_per_freq[-1]
        else:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:])
        return 10*np.log10(power) if dB else power


    def set_magnitude(self, value, start=None, end=None):
        start_idx = np.argmin(np.abs(self.frequencies - start)) if start is not None else 0
        end_idx = np.argmin(np.abs(self.frequencies - end)) if end is not None else len(self.frequencies)-1
        modified_spectrum = deepcopy(self)
        modified_spectrum.magnitude[start_idx:end_idx+1] = value
        return modified_spectrum


    def modify_magnitude(self, amount, start=None, end=None):
        start_idx = np.argmin(np.abs(self.frequencies - start)) if start is not None else 0
        end_idx = np.argmin(np.abs(self.frequencies - end)) if end is not None else len(self.frequencies)-1
        modified_spectrum = deepcopy(self)
        if self.dB:
            modified_spectrum.magnitude[start_idx:end_idx+1] = np.clip(modified_spectrum.magnitude[start_idx:end_idx+1] + amount, -120, None)

        else:
            modified_spectrum.magnitude[start_idx:end_idx+1] *= amount
        return modified_spectrum


    @property
    def complex(self):
        if self.dB:
            magnitude = 10 ** (self.magnitude / 20)
        else:
            magnitude = self.magnitude ** (1/self.exponent)
        if self._norm_single_side_band:
            if self._fft_size % 2 == 0:
                magnitude[1:-1] /= sqrt(2)
            else:
                magnitude[1:] /= sqrt(2)
        return magnitude * np.exp(1j*self.phase)


class PowerSpectrum(Spectrum):
    """A class representing a complex power spectrum.
    """
    def __init__(self, in_data, **kwargs):
        exponent = kwargs.pop('exponent', None)
        if exponent is not None and exponent != 2:
            warnings.warn('Magnitude exponent is automatically set to 2 for a PowerSpectrum')
        super().__init__(in_data, exponent=2, **kwargs)


class Spectrogram(Signal):
    """A class representing a complex spectrogram.
    """
    def __init__(
        self, input_signal, *,
        frame_duration=None, frame_size=None, step_duration=None, step_size=None, step_ratio=None,
        dB=True, min_freq=None, max_freq=None, num_bins=None, norm_single_side_band=False,
        spacing='linear', window='hann', exponent=1, samplerate=None,
    ):
        samples, samplerate = get_samples_and_rate(input_signal, samplerate)

        self._num_bins = num_bins
        self._norm_single_side_band = norm_single_side_band
        self.spacing = spacing
        self.window = window
        self.exponent = exponent
        self.dB = dB
        self._input_samplerate = samplerate

        self._frame_size, self._overlap_size = _parse_frame_params(frame_duration, frame_size,
            step_duration,step_size, step_ratio, samplerate, spacing, min_freq)
        self.samplerate = samplerate / (self._frame_size - self._overlap_size)

        if max_freq is None:
            max_freq = samplerate / 2
        if min_freq is not None and min_freq < 1 / self._frame_size:
            raise ValueError('The given minimum frequency is too small for the given frame width')
        if spacing == 'log':
            if num_bins is None:
                raise ValueError(f'The number of bins per semitone needs to be given as "num_bins" when requesting {spacing}-spaced frequencies')
            if min_freq is None or min_freq <= 0 or min_freq >= max_freq:
                raise ValueError(f'A minimum frequency above 0 and below the maximum frequency needs to be given when requesting {spacing}-spaced frequencies')
        elif spacing == 'linear':
            if num_bins is None:
                num_bins = self._frame_size
        else:
            raise ValueError('The frequency spacing needs to be one of "linear", "log" or "mel"')

        self._fft_size = max(self._frame_size, _fft_size_for_spacing(spacing, num_bins, samplerate, min_freq, max_freq))
        _, self.times, spectrogram = signal.stft(samples, fs=samplerate, window=window, nperseg=self._frame_size,
                                                 noverlap=self._overlap_size, nfft=self._fft_size, padded=False)
        filtered_spectrogram, self.frequencies, self._bin_values = _spacing_filter(
            spectrogram, spacing, samplerate, min_freq, max_freq, self._fft_size, num_bins)
        self.magnitude = np.abs(filtered_spectrogram)
        self.phase = np.angle(filtered_spectrogram)

        if norm_single_side_band:
            if self._fft_size % 2 == 0:
                self.magnitude[1:-1] *= sqrt(2)
            else:
                self.magnitude[1:] *= sqrt(2)
        if dB:
            self.magnitude = 20 * np.log10(np.clip(self.magnitude, 1e-6, None))
        else:
            self.magnitude **= exponent


    def plot(self, lowest_value=None, highest_value=None, palette=None, **fig_args):
        if not palette:
            palette = Viridis256
        if not lowest_value:
            lowest_value = np.min(self.magnitude)
        if not highest_value:
            highest_value = np.max(self.magnitude)

        freq_label = _freq_label(self.spacing)
        default_args = {
            'width': 900, 'height': 400,
            'x_axis_label': 'time [s]', 'y_axis_label': freq_label,
            'tools': 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,save,reset',
            'active_drag': 'pan',
            'active_inspect': 'auto',
            'active_scroll': 'auto',
            'toolbar_location': 'above',
            'tooltips': [('time [s]', '@time{0.000}'), ('frequency [Hz]', '@frequency{0.000}'), ['magnitude', '@magnitude{0.000}']],
        }
        if self.spacing in ('mel', 'log'):
            default_args['tooltips'].insert(1, (freq_label, '@bins{0.0}'))

        if self.exponent == 2 or self.dB:
            default_args['tooltips'][-1][0] = 'power'
        if self.dB:
            default_args['tooltips'][-1][0] += ' [dB]'
        if fig_args.get('tooltips') is not None and self.magnitude.size > 2000000:
            fig_args['tooltips'] = None
            warnings.warn('Tooltips are automatically disabled when plotting large spectrograms for performance reasons. '
                          'Pass "tooltips=None" to silence this warning.')

        fig = figure(**{**default_args, **fig_args})
        if isinstance(fig.x_range, DataRange1d):
            fig.x_range.range_padding = 0
        if isinstance(fig.y_range, DataRange1d):
            fig.y_range.range_padding = 0
        step_time = 1 / self.samplerate
        if [t for t in fig.tools if isinstance(t, InspectTool)]:
            all_times = np.broadcast_to(self.times, self.magnitude.shape)
            all_freqs = np.broadcast_to(self.frequencies.reshape(-1, 1), self.magnitude.shape)
            all_bin_values = np.broadcast_to(self._bin_values.reshape(-1, 1), self.magnitude.shape)
            delta_y = (self._bin_values[-1] - self._bin_values[0]) / (len(self._bin_values) - 1)
            data_source = ColumnDataSource({'magnitude': self.magnitude.reshape(-1, 1, 1).tolist(), 'time': all_times.ravel(), 'frequency': all_freqs.ravel(), 'bins': all_bin_values.ravel()})
            color_indices = np.rint(np.interp(self.magnitude, (lowest_value, highest_value), (0, len(palette)-1))).astype(int)
            data_source.data['color'] = [palette[i] for i in color_indices.ravel()]
            fig.rect(x='time', y='bins', width=step_time, height=delta_y, color='color', source=data_source)
        else:
            mapper = LinearColorMapper(palette=palette, low=lowest_value, high=highest_value)
            fig.image([self.magnitude], x=self.times[0]-step_time/2, y=self._bin_values[0], dw=self.times[-1]+step_time, dh=self._bin_values[-1], color_mapper=mapper)
        return fig


    def __len__(self):
        return len(self.times)


    def rms(self):
        return sqrt(self.power(dB=False))


    def power(self, dB=True):
        if self.dB:
            power_per_freq = 10 ** (self.magnitude / 10)
        else:
            power_per_freq = self.magnitude ** (2/self.exponent)
        if self._norm_single_side_band:
            power = np.sum(power_per_freq, axis=0)
        elif self._fft_size % 2 == 0:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:-1], axis=0) + power_per_freq[-1]
        else:
            power = power_per_freq[0] + 2*np.sum(power_per_freq[1:], axis=0)
        return 10*np.log10(power) if dB else power


    @property
    def complex(self):
        if self.dB:
            magnitude = 10 ** (self.magnitude / 20)
        else:
            magnitude = self.magnitude ** (1/self.exponent)
        if self._norm_single_side_band:
            if self._fft_size % 2 == 0:
                magnitude[1:-1] /= sqrt(2)
            else:
                magnitude[1:] /= sqrt(2)
        return magnitude * np.exp(1j*self.phase)


    def spectrum_at(self, *, time=None, index=None):
        if (time is None and index is None) or (time is not None and index is not None):
            raise ValueError('Specify either the time or the index of the requested spectrum')
        if time is not None:
            index = np.argmin(np.abs(self.times - time))
        if self.spacing == 'linear':
            min_freq, max_freq = None, None
        else:
            min_freq, max_freq = self.frequencies[0], self.frequencies[-1]
        spectrum = Spectrum(np.zeros(self._frame_size), dB=self.dB, min_freq=min_freq, max_freq=max_freq, 
            num_bins=self._num_bins, norm_single_side_band=self._norm_single_side_band, spacing=self.spacing,
            window=self.window, exponent=self.exponent, samplerate=self._input_samplerate)
        spectrum._fft_size = self._fft_size
        spectrum.magnitude = self.magnitude[:, index]
        spectrum.phase = self.phase[:, index]
        spectrum.frequencies = self.frequencies
        return spectrum


def _parse_frame_params(
    frame_duration, frame_size, step_duration, step_size, step_ratio, samplerate, spacing, min_freq
):
    frame_specs = sum([frame_duration is not None, frame_size is not None])
    if frame_specs != 1:
        if spacing == 'linear':
            raise ValueError('Specify a frame width either as duration in seconds or size in samples')
        if min_freq is None:
            raise ValueError('Specify either a minimum frequency or a frame width in seconds or in samples')
    if frame_duration is not None:
        frame_size = round(frame_duration * samplerate)
    elif frame_size is None and min_freq is not None and spacing != 'linear':
        frame_size = ceil(samplerate / min_freq)

    if sum([step_duration is not None, step_size is not None, step_ratio is not None]) > 1:
        raise ValueError('Specify a frame step either as duration in seconds, size in samples or ratio')
    if step_duration is not None:
        overlap_size = round((frame_duration-step_duration) * samplerate)
    elif step_size is not None:
        overlap_size = frame_size - step_size
    elif step_ratio is not None:
        overlap_size = round((1-step_ratio) * frame_size)
    else:
        overlap_size = frame_size // 2
    return frame_size, overlap_size


def _spacing_filter(spectral_values, spacing, samplerate, min_freq, max_freq, fft_size, num_bins):
    if spacing == 'linear':
        lin_frequencies = np.arange(len(spectral_values)) * samplerate / fft_size
        if min_freq is not None:
            min_idx = np.argmin(np.abs(np.where(lin_frequencies < min_freq, np.inf, lin_frequencies) - min_freq))
        if max_freq is not None:
            max_idx = np.argmin(np.abs(np.where(lin_frequencies > max_freq, np.inf, lin_frequencies) - max_freq))
        return spectral_values, lin_frequencies, lin_frequencies
    if spacing == 'mel':
        bin_values, spaced_frequencies, filterbank = mel_filterbank(samplerate, fft_size, num_bins, min_freq, max_freq, normalize=False)
    elif spacing == 'log':
        bin_values, spaced_frequencies, filterbank = twelve_tet_filterbank(samplerate, fft_size, num_bins, min_freq, max_freq, normalize=False, a4=440)
    return np.matmul(filterbank, spectral_values), spaced_frequencies, bin_values


def _freq_label(spacing):
    if spacing == 'linear':
        return 'frequency [Hz]'
    if spacing == 'mel':
        return 'mel'
    if spacing == 'log':
        return 'MIDI number'
