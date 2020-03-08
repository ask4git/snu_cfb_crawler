"""
genetic_obesity_extractor.py
"""
# -*- coding: utf-8 -*-


import csv

index_of_disease = 4
genetic_obesity = 'H02106:Genetic obesity'


def extractor(path_in, path_out):
    with open(path_in) as in_file, \
            open(path_out, 'w') as out_file:

        reader = csv.reader(in_file, delimiter='\t')
        writer = csv.writer(out_file, delimiter='\t')

        for row in reader:
            diseases = row[index_of_disease]

            for disease in diseases.split('::'):
                if disease == genetic_obesity:
                    writer.writerow(row)
