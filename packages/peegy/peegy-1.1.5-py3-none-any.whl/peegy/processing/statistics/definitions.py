

class HotellingTSquareFrequencyTest(object):
    def __init__(self,
                 test_name='HT2',
                 frequency_tested=None,
                 df_1=None,
                 df_2=None,
                 t_square=None,
                 f=None,
                 p_value=None,
                 n_epochs=None,
                 spectral_magnitude=None,
                 spectral_phase=None,
                 rn=None,
                 snr=None,
                 snr_db=None,
                 f_critic=None,
                 channel=None):
        self.test_name = test_name
        self.frequency_tested = frequency_tested
        self.df_1 = df_1
        self.df_2 = df_2
        self.t_square = t_square
        self.f = f
        self.p_value = p_value
        self.spectral_magnitude = spectral_magnitude
        self.spectral_phase = spectral_phase
        self.rn = rn
        self.n_epochs = n_epochs
        self.snr = snr
        self.snr_db = snr_db
        self.f_critic = f_critic
        self.channel = channel


class HotellingTSquareTest(object):
    def __init__(self,
                 test_name='HT2',
                 df_1=None,
                 df_2=None,
                 t_square=None,
                 f=None,
                 f_critic=None,
                 p_value=None,
                 mean_amplitude=None,
                 mean_phase=None,
                 rn=None,
                 n_epochs=None,
                 snr=None,
                 snr_db=None,
                 snr_critic_db=None,
                 snr_critic=None,
                 channel=None,
                 frequency_tested=None,
                 **kwargs
                 ):
        self.test_name = test_name
        self.df_1 = df_1
        self.df_2 = df_2
        self.t_square = t_square
        self.f = f
        self.f_critic = f_critic
        self.p_value = p_value
        self.mean_amplitude = mean_amplitude
        self.mean_phase = mean_phase
        self.rn = rn
        self.n_epochs = n_epochs
        self.snr = snr
        self.snr_db = snr_db
        self.snr_critic_db = snr_critic_db
        self.snr_critic = snr_critic
        self.channel = channel
        self.frequency_tested = frequency_tested
        for _item, _value in kwargs.items():
            setattr(self, _item, _value)


class FrequencyFTest(object):
    def __init__(self,
                 test_name='F-test',
                 frequency_tested=None,
                 df_1=None,
                 df_2=None,
                 f=None,
                 p_value=None,
                 spectral_magnitude=None,
                 spectral_phase=None,
                 rn=None,
                 snr=None,
                 snr_db=None,
                 f_critic=None,
                 channel=None):
        self.test_name = test_name
        self.frequency_tested = frequency_tested
        self.df_1 = df_1
        self.df_2 = df_2
        self.f = f
        self.p_value = p_value
        self.spectral_magnitude = spectral_magnitude
        self.spectral_phase = spectral_phase
        self.rn = rn
        self.snr = snr
        self.snr_db = snr_db
        self.f_critic = f_critic
        self.channel = channel


class PhaseLockingValueTest(object):
    def __init__(self,
                 test_name='PLV',
                 plv=None,
                 df_1=None,
                 z_value=None,
                 z_critic=None,
                 p_value=None,
                 mean_phase=None,
                 channel=None,
                 frequency_tested=None,
                 rn=None):
        self.test_name = test_name
        self.plv = plv
        self.df_1 = df_1
        self.z_value = z_value
        self.z_critic = z_critic
        self.p_value = p_value
        self.mean_phase = mean_phase
        self.channel = channel
        self.frequency_tested = frequency_tested
        self.rn = rn


class FpmTest(object):
    def __init__(self,
                 test_name='Fmp',
                 df_1=None,
                 df_2=None,
                 f=None,
                 f_critic=None,
                 p_value=None,
                 rn=None,
                 snr=None,
                 time_ini=None,
                 time_end=None,
                 n_epochs=None,
                 channel=None):
        self.test_name = test_name
        self.df_1 = df_1
        self.df_2 = df_2
        self.f = f
        self.f_critic = f_critic
        self.p_value = p_value
        self.rn = rn
        self.snr = snr
        self.time_ini = time_ini
        self.time_end = time_end
        self.n_epochs = n_epochs
        self.channel = channel
