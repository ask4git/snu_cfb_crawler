"""
main.py
"""
# -*- coding: utf-8 -*-

from kegg_crawler import gene_url_crawler
from kegg_crawler import multi_threading_crawling


trigger_urls = {
    'hsa04080: Neuroactive ligand-receptor interaction': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa04080+H02106',
    'hsa04714: Thermogenesis': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa04714+H02106',
    'hsa04024: cAMP signaling pathway': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa04923+H02106',
    'hsa03320: PPAR signaling pathway': 'https://www.kegg.jp/kegg-bin/show_pathway?hsa03320+H02106'
}


def main():
    # Get gene urls
    target_urls = []
    for trigger_url in trigger_urls:
        target_urls += gene_url_crawler(trigger_url)

    # Deduplication urls
    target_urls = list(set(target_urls))

    # Use multi threading
    multi_threading_crawling(processes=6, urls=target_urls)


main()
