import os
import main
import csv

if __name__ == '__main__':
    signal_files = os.listdir('signals')

    for index, file in enumerate(signal_files):
        print(index, file)
        os.chdir('./signals')
        os.rename(file, 'current.csv')
        os.chdir('../')
        main.main("./configuration/config_gsr.json")
        os.chdir('./signals')
        os.rename('current.csv', file)
        os.chdir('../')

    feature_files = os.listdir('results\\features')

    with open("./results/merge/ECG_features.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        empty_destination_file = csv.reader(csv_file).line_num == 0
        for file in feature_files:
            with open("./results/features/"+file, 'r') as merge_file:
                csv_reader = csv.reader(merge_file)
                if file.__contains__('ECG') and empty_destination_file:
                    empty_destination_file = False
                    for index, row in enumerate(csv_reader):
                        if index >= 6:
                            csv_writer.writerow(row)
                elif file.__contains__('ECG'):
                    for index, row in enumerate(csv_reader):
                        if index >= 7:
                            csv_writer.writerow(row)

    with open("./results/merge/GSR_features.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        empty_destination_file = csv.reader(csv_file).line_num == 0
        for file in feature_files:
            with open("./results/features/"+file, 'r') as merge_file:
                csv_reader = csv.reader(merge_file)
                if file.__contains__('GSR') and empty_destination_file:
                    empty_destination_file = False
                    for index, row in enumerate(csv_reader):
                        if index >= 6:
                            csv_writer.writerow(row)
                elif file.__contains__('GSR'):
                    for index, row in enumerate(csv_reader):
                        if index >= 7:
                            csv_writer.writerow(row)

