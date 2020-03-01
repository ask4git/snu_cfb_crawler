"""
kegg_crawler.__init__.py
"""
# -*- coding: utf-8 -*-

import re
import requests
import multiprocessing
import logging
import traceback

from bs4 import BeautifulSoup
from os.path import join as pjoin

from kegg_crawler.kegg_gene_model import Gene


def kegg_gene_url_spliter(url):
    res = []
    base_url = 'https://www.genome.jp/dbget-bin/www_bget'
    gene_id_list = url.split('?')[1]
    for gene_id in gene_id_list.split('+'):
        if gene_id.startswith('hsa'):
            res.append('{}?{}'.format(base_url, gene_id))
    return res


def kegg_gene_base_crawler(url, out_file):
    print(url)
    try:
        res = requests.get(url)
        html = BeautifulSoup(res.content, 'html.parser')
        serialized_data = Gene(html).serialize()
        print(serialized_data)
        print(serialized_data, file=out_file)

    except Exception as error:
        print(error)
        logging.error(traceback.format_exc())   # logging


def kegg_gene_crawler(url):
    path_output_tsv_file = 'result_data/kegg_gene_result.tsv'
    with open(path_output_tsv_file, 'a') as out_file:
        for sub_url in kegg_gene_url_spliter(url):
            kegg_gene_base_crawler(sub_url, out_file)


def kegg_node_url(url):
    # todo
    res = []
    home_url = 'https://www.kegg.jp'
    try:
        response = requests.get(url)
        html = BeautifulSoup(response.content, 'html.parser')
        shapes = html.find_all('area', {'shape': 'rect'})
        for shape in shapes:
            genes_url = pjoin(home_url, shape.get('href'))
            res.append(genes_url)

    except Exception as error:
        print(error)
        logging.error(traceback.format_exc())   # logging

    return res


def multi_threading_kegg_gene_crawler(url):
    nodes_url = kegg_node_url(url)
    for url in nodes_url:
        kegg_gene_crawler(url)
    pool = multiprocessing.Pool(processes=6)
    pool.map(kegg_gene_crawler, nodes_url)
    pool.close()
    pool.join()


start_urls = [
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa04080+H02106',
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa04714+H02106',
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa04923+H02106',
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa03320+H02106'
]


for start_url in start_urls:
    multi_threading_kegg_gene_crawler(start_url)
