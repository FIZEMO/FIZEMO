import scipy.signal as ss


# function for signal decimation
# first argument is signal data to decimation
# second argument is frequency with which signal was sampled
# third argument is modifier for how less samples we need for example value 10 means we want 10x less samples
def decimation_process(signalData, samplingFrequency, decimationFrequency):
    ratio = int(int(samplingFrequency) / int(decimationFrequency))
    decimatedSignal = ss.decimate(signalData, ratio, 8, axis=0)
    return decimatedSignal