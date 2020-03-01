"""
add_source_data.py
"""
# -*- coding: utf-8 -*-

import csv

from tqdm import tqdm


class CsvDataObject(list):
    def __init__(self, path_file_name, delimiter=None):
        # initialize
        super().__init__()
        self.__file_name = path_file_name
        self.__delimiter = delimiter
        self.__read_csv_file()

    def __read_csv_file(self):
        with open(self.__file_name, 'r', encoding='utf-8') as in_file:
            sp_char = self.__delimiter if self.__delimiter else ','
            reader = csv.reader(in_file, delimiter=sp_char)

            for each_line in reader:
                self.append(each_line)

    def print_csv_file(self, path_file_name, target_index=None):
        with open(path_file_name, 'w', encoding='utf-8') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for line in tqdm(self):
                try:
                    writer.writerow([line[index] for index in target_index])
                except IndexError as error:
                    print(line)


path_in_file = '/Users/ask4git/Desktop/HUMANproteinSEQUENCE.csv'
target_db_name = 'Proteins'
source_db_name = '03_PDB_seq'
path_out_file = '/Users/ask4git/Desktop/{}_{}.csv'.format(target_db_name, source_db_name)


obj = CsvDataObject(path_in_file)
obj.print_csv_file(path_out_file, [0, 1, 5])
