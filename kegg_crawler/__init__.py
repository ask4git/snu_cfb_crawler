"""
kegg_crawler.__init__.py
"""
# -*- coding: utf-8 -*-

import re
import requests

import logging
import traceback
import multiprocessing

from bs4 import BeautifulSoup
from os.path import join as pjoin

from kegg_crawler.kegg_gene_model import Gene


def gene_url_crawler(url):
    # todo make UrlNotFound exception
    res = []
    home_url = 'https://www.kegg.jp'

    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    shapes = html.find_all('area', {'shape': 'rect'})

    for shape in shapes:
        genes_url = pjoin(home_url, shape.get('href'))
        for gene_url in gene_url_spliter(genes_url):
            res.append(gene_url.strip())

    return res


def gene_url_spliter(url):
    res = []
    base_url = 'https://www.genome.jp/dbget-bin/www_bget'
    gene_id_list = url.split('?')[1]

    for gene_id in gene_id_list.split('+'):
        if gene_id.startswith('hsa:'):
            res.append('{}?{}'.format(base_url, gene_id))

    return res


def gene_crawler(url):
    try:
        res = requests.get(url)
        html = BeautifulSoup(res.content, 'html.parser')
        serialized_data = Gene(url, html).serialize()
        print(url, serialized_data)
        with open('result_data/kegg_gene_result.tsv', 'a') as out_file:
            print(serialized_data, file=out_file)

    except Exception as error:
        print(error)
        logging.error(traceback.format_exc())  # logging


def multi_threading_gene_crawling(processes, urls):
    pool = multiprocessing.Pool(processes=processes)
    pool.map(gene_crawler, urls)
    pool.close()
    pool.join()
