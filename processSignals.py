import os
import main

if __name__ == '__main__':
    signal_files = os.listdir('D:\Projects\FIZEMO\signals')

    for index, file in enumerate(signal_files):
        os.chdir('D:\Projects\FIZEMO\signals')
        os.rename(file, 'current.csv')
        os.chdir('D:\Projects\FIZEMO')
        main.main("./configuration/config.json")
        os.chdir('D:\Projects\FIZEMO\signals')
        os.rename('current.csv', file)
