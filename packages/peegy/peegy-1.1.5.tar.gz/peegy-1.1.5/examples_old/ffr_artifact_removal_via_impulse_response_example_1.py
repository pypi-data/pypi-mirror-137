from peegy.processing.pipe.pype_line_definitions import *
from peegy.processing.pipe.definitions import GenerateInputData
from peegy.io.storage.data_storage_tools import *
import os
import peegy.processing.tools.filters.eegFiltering as eegf
from peegy.processing.tools.template_generator.auditory_waveforms import artifact_and_brain_envelope


def my_pipe():
    # first we generate a test signal
    fs = 16384.0
    epoch_length = 4.0
    epoch_length = np.ceil(epoch_length * fs) / fs  # fit to fs rate
    alternating_polarity = False  # stimulus has fix polarity in every presentation

    # first we generate a test signal
    fs = 16384.0
    burst_duration = 1  # seconds
    stim_delay = 0.001  # neural delay in secs
    brain_delay = 0.113  # brain response delay

    template_waveform, stimulus_waveform, leaked_stimulus = artifact_and_brain_envelope(
        fs=fs,
        stimulus_delay=stim_delay,
        brain_delay=brain_delay,
        duration=burst_duration,
        seed=0)
    n_channels = 32
    event_times = np.arange(0, 300, epoch_length)
    reader = GenerateInputData(template_waveform=template_waveform,
                               stimulus_waveform=leaked_stimulus,
                               alternating_polarity=alternating_polarity,
                               fs=fs,
                               n_channels=n_channels,
                               snr=1,
                               layout_file_name='biosemi32.lay',
                               event_times=event_times,
                               event_code=1.0,
                               figures_subset_folder='artifact_subtraction_ir_1',
                               noise_seed=10,
                               line_noise_amplitude=0
                               )
    reader.run()
    # define new sampling rate to make processing easier
    new_fs = fs//1.0
    pipe_line = PipePool()
    pipe_line.append(ReferenceData(reader, reference_channels=['Cz'], invert_polarity=False),
                     name='referenced')

    pipe_line.append(AutoRemoveBadChannels(reader),
                     name='channel_cleaned')

    pipe_line.append(ReSampling(pipe_line.get_process('channel_cleaned'),
                                new_sampling_rate=new_fs),
                     name='down_sampled')

    # down-sample stimuli to match EEG data
    rs_leak_stimulus, _ = eegf.eeg_resampling(x=reader.simulated_artifact,
                                              factor=new_fs / fs)
    rs_template_waveform, _ = eegf.eeg_resampling(x=template_waveform,
                                                  factor=new_fs / fs)
    rs_simulated_neural_response, _ = eegf.eeg_resampling(x=reader.simulated_neural_response,
                                                          factor=new_fs / fs)

    pipe_line.append(RegressOutArtifactIR(pipe_line.get_process('down_sampled'),
                                          stimulus_waveform=rs_leak_stimulus,
                                          ir_length=0.01),
                     name='artifact_free')

    pipe_line.append(FilterData(pipe_line.get_process('artifact_free'), high_pass=2.0, low_pass=60.0),
                     name='filtered_data')

    pipe_line.append(EpochData(pipe_line.get_process('filtered_data'),
                               event_code=1.0,
                               base_line_correction=False,
                               post_stimulus_interval=2.0),
                     name='time_epochs')

    pipe_line.append(CreateAndApplySpatialFilter(pipe_line.get_process('time_epochs'),
                                                 sf_join_frequencies=None),
                     name='dss_time_epochs')

    pipe_line.append(AverageEpochs(pipe_line.get_process('dss_time_epochs')),
                     name='time_domain_ave')

    # compute epochs using without dss
    pipe_line.append(PlotTopographicMap(pipe_line.get_process('time_domain_ave'),
                                        plot_x_lim=[0, epoch_length],
                                        user_naming_rule='time_domain_ave'))

    pipe_line.run()

    # we process data without removing the artifact on a second pipeline
    pipe_line_2 = PipePool()
    pipe_line_2.append(EpochData(pipe_line.get_process('down_sampled'),
                                 event_code=1.0,
                                 base_line_correction=False,
                                 post_stimulus_interval=2.0),
                       name='time_epochs')

    pipe_line_2.append(CreateAndApplySpatialFilter(pipe_line_2.get_process('time_epochs'),
                                                   sf_join_frequencies=None),
                       name='dss_time_epochs')

    pipe_line_2.append(AverageEpochs(pipe_line_2.get_process('dss_time_epochs')),
                       name='time_domain_ave')

    pipe_line_2.run()

    # create tables with results for data using dss
    time_data_clean = pipe_line.get_process('time_domain_ave')
    time_data_raw = pipe_line_2.get_process('time_domain_ave')

    # we plot target response vs. recovered
    plt.plot(time_data_raw.output_node.data[:, -1], label='contaminated response')
    plt.plot(time_data_clean.output_node.data[:, -1], label='recovered response')
    plt.plot(rs_simulated_neural_response[0:int(epoch_length*new_fs), -1], label='target response')
    plt.legend()
    plt.show()
    # compute correlations between brain response and contaminated response artifact
    correlations_artifact = np.empty(time_data_clean.output_node.data.shape[1])
    for _idx in range(time_data_clean.output_node.data.shape[1]):
        _size = np.minimum(time_data_raw.output_node.data.shape[0], rs_template_waveform.shape[0])
        correlations_artifact[_idx] = np.corrcoef(
            rs_template_waveform[0:_size, :].flatten(),
            time_data_raw.output_node.data[0:_size, _idx])[0, 1]
    print('obtained correlation between and leaked artifact {:}'.format(correlations_artifact))

    # compute correlations between brain response and recovered response artifact
    correlations_brain = np.empty(time_data_clean.output_node.data.shape[1])
    for _idx in range(time_data_clean.output_node.data.shape[1]):
        _size = np.minimum(time_data_clean.output_node.data.shape[0], rs_template_waveform.shape[0])
        correlations_brain[_idx] = np.corrcoef(
            rs_template_waveform[0:_size, :].flatten(),
            time_data_clean.output_node.data[0:_size, _idx])[0, 1]
    print('obtained correlation between response and simulated brain response {:}'.format(correlations_brain))

    waveform_table_dss = PandasDataTable(table_name='time_waveform',
                                         pandas_df=time_data_clean.output_node.data_to_pandas())

    # now we save our data to a database
    subject_info = SubjectInformation(subject_id='Test_Subject')
    measurement_info = MeasurementInformation(
        date='Today',
        experiment='sim')

    _parameters = {'Type': 'envelope_tracking'}
    data_base_path = reader.input_node.paths.file_directory + os.sep + 'envelope_tracking_ir_1.sqlite'
    store_data(data_base_path=data_base_path,
               subject_info=subject_info,
               measurement_info=measurement_info,
               recording_info={'recording_device': 'dummy_device'},
               stimuli_info=_parameters,
               pandas_df=[waveform_table_dss])


if __name__ == "__main__":
    """
    In this example we estimate neural activity from the envelope by removing the transducer artifact
    by means of impulse response estimation. 
    Here we estimate the impulse response from the entire signal, not from the epochs.
    """
    my_pipe()
