import numpy as np
from pyeeg.processing.pipe.definitions import DataNode


class SpatialFilter(object):
    def __init__(self):
        self.z = np.array([])  # components matrix
        self.cov = np.array([])  # covariance matrix
        self.pwr0 = np.array([])
        self.pwr1 = np.array([])
        self.components_ave = DataNode()  # class containing averaged components
        self.component_indexes = np.array([])  # components used to clean data
