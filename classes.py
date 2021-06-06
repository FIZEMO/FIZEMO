# Class for main signal
# signal - two-dimensions list with signal [[timestamps, values]]
# signalValues - list with only values of the signal [values]
class Signal:
    signalSamples = list()
    signalValues = list()

    # This function updates vector with values of the signal
    # It only takes values of the signal, that why there is number 1 in this fragment `signal[iterator][1]`
    # If we would like to have only time stamps we would have to make it like this `signal[iterator][0]`
    # Firstly we clear the list because it could change it's length due to processing i.e decimation
    def update_values(self):
        self.signalValues.clear()
        for iterator in range(len(self.signalSamples)):
            self.signalValues.append(self.signalSamples[iterator][1])


