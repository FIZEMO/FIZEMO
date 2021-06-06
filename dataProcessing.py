import scipy.signal as ss


# function for signal decimation
# first argument is signal data to decimation
# second argument is frequency with which signal was sampled
# third argument is goal frequency with which signal should be sampled
def decimation_process(signalData, samplingFrequency, goalFrequency):
    ratio = int(int(samplingFrequency) / int(goalFrequency))
    decimatedSignal = ss.decimate(signalData, ratio, 8, axis=0)
    return decimatedSignal
