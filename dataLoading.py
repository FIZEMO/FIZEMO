import pandas as pd


# function to load signal from a .csv file
# - first argument is a name of the file with signal
# - second argument is a name of the object where sampled signal will be assigned to
def load_signal(fileName, signal):
    path = './signals/' + fileName + '.csv'
    df = pd.read_csv(r'' + path)
    signal.sampledSignal = df.to_numpy()



