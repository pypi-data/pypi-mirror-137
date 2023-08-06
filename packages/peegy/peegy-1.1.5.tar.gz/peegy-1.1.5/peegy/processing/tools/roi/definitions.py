import numpy as np
import astropy.units as u
from peegy.tools.units.unit_tools import set_default_unit


class TimeROI(object):
    """
    Object used to define the timepoints in a region of interest (ROI), for time-window based analysis. The required
    parameters  are the beginning (initial) and ending timepoints in seconds. To distinguish different ROI windows,
    each objects can  be linked to a measure (string), a label (string), a condition (string), an (EEG) channel (str),
    or a value (float). This class will return a  numpy array. The TimeROI object is used by classes like AverageEpochs
    or HotellingT2Test.
    Example to define a ROI window for SNR estimation starting at 150 ms and ending at 350 ms:
    roi_windows = np.array([TimeROI(ini_time=150.0e-3, end_time=350.0e-3, measure="snr", label="itd_snr")])
    """
    def __init__(self,
                 ini_time: u.quantity.Quantity = None,
                 end_time: u.quantity.Quantity = None,
                 measure: str = None,
                 label: str = None,
                 condition: str = None,
                 value: u.quantity.Quantity = None,
                 show_window: bool = True,
                 show_label: bool = False,
                 ):
        """

        :param ini_time: initial time of the window (in seconds)
        :param end_time: end time of the window (in seconds)
        :param measure: str measure to be performed e.g. "snr", "rms" (this key value can be used to trigger a given
        action within a function requiring a ROI window
        :param label: str defining a desired label for this ROI
        :param condition: str defining a desired condition
        :param value: output value to store the output  of a given measure
        :param show_window: boolean use when plotting data. If true, time interval will be shown in plots
        :param show_label: boolean use when plotting data. If true, label will be shown in plots
        """
        self.ini_time = set_default_unit(ini_time, u.s)
        self.end_time = set_default_unit(end_time, u.s)
        self.measure = measure
        self.label = label
        self.condition = condition
        self.value = value
        self.show_window = show_window
        self.show_label = show_label

    def get_samples_interval(self, fs: u.quantity.Quantity = None):
        out = np.array([self.ini_time.to(u.s).value,
                        self.end_time.to(u.s).value]) * u.s * fs
        return out.astype(np.int)


class Marker(object):
    def __init__(self,
                 x_ini: u.Quantity = 0,
                 x_end: u.Quantity = 0,
                 y_ini: u.Quantity = 0,
                 y_end: u.Quantity = 0,
                 label='',
                 channel=''):
        self.x_ini = x_ini
        self.x_end = x_end
        self.y_ini = y_ini
        self.y_end = y_end
        self.channel = channel
        self.label = label
