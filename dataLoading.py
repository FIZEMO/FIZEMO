import pandas as pd

from matplotlib import pyplot as plt


# function to load signal from a .csv file
# - first argument is a name of the file with signal
# - second argument is a name of the object where sampled signal will be assigned to
def load_signal(fileName):
    path = './signals/' + fileName + '.csv'
    pandasDataFramedSignal = pd.read_csv(r'' + path)
    signal = pandasDataFramedSignal.to_numpy()
    return signal


# function to draw plot from given data
# - first argument is data to draw
# - second argument is a name of the window
# - third argument is a title of the plot
# - fourth argument is a name of X axis
# - fifth argument is a name of Y axis
def draw_plot(points, windowName, titleName, xName, yName):
    x_axis, y_axis = zip(*points)
    plt.figure(windowName)
    plt.title(titleName)
    plt.xlabel(xName)
    plt.plot(x_axis, y_axis)
    plt.show()



