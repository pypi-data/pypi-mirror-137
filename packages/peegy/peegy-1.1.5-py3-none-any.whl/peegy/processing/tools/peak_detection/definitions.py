from peegy.definitions.channel_definitions import Domain
from peegy.tools.units.unit_tools import set_default_unit
import pandas as pd
import astropy.units as u


class EegPeak(object):
    def __init__(self,
                 channel: str = None,
                 x: float = None,
                 rn: float = None,
                 amp: float = None,
                 amp_snr: float = None,
                 significant: bool = False,
                 peak_label: str = None,
                 show_label: bool = True,
                 show_peak: bool = True,
                 positive: bool = True,
                 domain: Domain = Domain.time,
                 spectral_phase: float = None):
        self.channel = channel
        self.x = x
        self.rn = rn
        self.amp = amp
        self.amp_snr = amp_snr
        self.significant = significant
        self.peak_label = peak_label
        self.show_label = show_label
        self.show_peak = show_peak
        self.positive = positive
        self.domain = domain
        self.spectral_phase = spectral_phase


class TimePeakWindow(object):
    def __init__(self,
                 label: str = None,
                 ini_time: u.quantity.Quantity = None,
                 end_time: u.quantity.Quantity = None,
                 ini_ref: str = None,
                 end_ref: str = None,
                 require_ini_ref: bool = False,
                 require_end_ref: bool = False,
                 global_ref: str = None,
                 require_global_ref: bool = False,
                 ini_global_ref: str = None,
                 end_global_ref: str = None,
                 minimum_scanning_window: float = 1.0e-3,
                 positive_peak: bool = False,
                 show_label: bool = True,
                 show_peak: bool = True,
                 force_search: bool = True,
                 channel: str = None,
                 target_channels: [str] = None,
                 exclude_channels: [str] = None):
        self._label = label
        self._ini_time = set_default_unit(ini_time, u.s)
        self._end_time = set_default_unit(end_time, u.s)
        self.ini_ref = ini_ref
        self.end_ref = end_ref
        self.require_ini_ref = require_ini_ref
        self.require_end_ref = require_end_ref
        self.global_ref = global_ref
        self.require_global_ref = require_global_ref
        self.ini_global_ref = ini_global_ref
        self.end_global_ref = end_global_ref
        self.minimum_scanning_window = set_default_unit(minimum_scanning_window, u.s)
        self.positive_peak = positive_peak
        self.show_label = show_label
        self.show_peak = show_peak
        self.force_search = force_search
        self.channel = channel
        self.target_channels = target_channels
        self.exclude_channels = exclude_channels

    def get_ini_time(self):
        return self._ini_time

    def set_ini_time(self, value):
        self._ini_time = value

    ini_time = property(get_ini_time, set_ini_time)

    def get_end_time(self):
        _end_time = self._end_time
        if self._end_time is None:
            _end_time = self._ini_time
        return _end_time

    def set_end_time(self, value):
        self._end_time = value
    end_time = property(get_end_time, set_end_time)

    def set_label(self, value):
        self._label = value

    def get_label(self):
        _label = self._label
        if self._label is None:
            _label = '{:.2e}'.format(self.ini_time)
        return _label
    label = property(get_label, set_label)


class PeaksContainer:
    def __init__(self, channel_label: str = None):
        self.channel_label = channel_label
        self._peaks = []

    def get_peaks(self):
        return self._peaks

    def append(self, value: EegPeak = None):
        self._peaks.append(value)

    peaks = property(get_peaks)

    def to_pandas(self):
        _data_pd = pd.DataFrame([_peak.__dict__ for _peak in self._peaks])
        return _data_pd


class PeakToPeakMeasure(object):
    def __init__(self, ini_peak='', end_peak=''):
        self.ini_peak = ini_peak
        self.end_peak = end_peak


class PeakToPeakQuantity(object):
    def __init__(self, **kwargs):
        self.channel = kwargs.get('channel', None)
        self.ini_time = kwargs.get('ini_time', None)
        self.max_time = kwargs.get('max_time', None)
        self.min_time = kwargs.get('min_time', None)
        self.amp = kwargs.get('amp', None)
        self.rn = kwargs.get('rn', None)
        self.amp_snr = kwargs.get('amp_snr', None)
        self.amp_label = kwargs.get('amp_label', None)


class PeakToPeakAmplitudeContainer:
    def __init__(self, channel_label: str = None):
        self.channel_label = channel_label
        self._peaks = []

    def get_peaks(self):
        return self._peaks

    def append(self, value: PeakToPeakQuantity = None):
        self._peaks.append(value)

    peaks = property(get_peaks)

    def to_pandas(self):
        _data_pd = pd.DataFrame([_peak.__dict__ for _peak in self._peaks])
        return _data_pd
