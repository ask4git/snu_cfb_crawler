"""
main.py
"""
# -*- coding: utf-8 -*-

import multiprocessing

from kegg_crawler import kegg_gene_crawler as crawler


start_urls = [
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa04080+H02106',
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa04714+H02106',
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa04923+H02106',
    'https://www.kegg.jp/kegg-bin/show_pathway?hsa03320+H02106'
]


def main():

    # Use multi threading
    pool = multiprocessing.Pool(processes=4)
    pool.map(crawler, start_urls)
    pool.close()
    pool.join()


main()
