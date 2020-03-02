"""
main.py
"""
# -*- coding: utf-8 -*-

from kegg_crawler import gene_url_crawler
from kegg_crawler import multi_threading_gene_crawling


kegg_gene_base_url = 'https://www.kegg.jp/kegg-bin/get_htext?br08402_gene.keg'

trigger_urls = {
    # H02106 Genetic obesity
    'hsa04080: Neuroactive ligand-receptor interaction': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa04080',
    'hsa04714: Thermogenesis': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa04714',
    'hsa04923: Regulation of lipolysis': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa04923',
    'hsa03320: PPAR signaling pathway': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa03320'
}


def main():
    # Get gene urls
    target_urls = []
    for __, trigger_url in trigger_urls.items():
        target_urls += gene_url_crawler(trigger_url)

    # Deduplication urls
    target_urls = list(set(target_urls))

    # Use multi threading
    multi_threading_gene_crawling(processes=6, urls=target_urls)


main()
