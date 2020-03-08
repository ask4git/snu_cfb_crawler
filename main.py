"""
main.py
"""
# -*- coding: utf-8 -*-

from kegg_crawler import gene_crawler
from kegg_crawler import gene_url_crawler
from kegg_crawler import multi_threading_gene_crawling

from kegg_crawler.genetic_obesity_extractor import extractor


kegg_gene_base_url = 'https://www.kegg.jp/kegg-bin/get_htext?br08402_gene.keg'

# https://www.kegg.jp/kegg-bin/get_htext?br08402_gene.keg
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
    for pathway_name, trigger_url in trigger_urls.items():
        gene_urls = gene_url_crawler(trigger_url)
        for url in gene_urls:
            print('\t'.join([pathway_name, url.split('?')[1]]))
        target_urls += gene_urls

    # Deduplication urls
    target_urls = list(set(target_urls))

    # Use multi threading
    multi_threading_gene_crawling(processes=6, urls=target_urls)


main()

path_in_file = '/Users/ask4git/Desktop/kegg_gene_result.tsv'
path_out_file = '/Users/ask4git/Desktop/kegg_gene_result_postprocessed.tsv'


extractor(path_in_file, path_out_file)
#
# urls = [
#     'https://www.kegg.jp/dbget-bin/www_bget?hsa:84984',
#     'https://www.kegg.jp/dbget-bin/www_bget?hsa:9149',
#     'https://www.kegg.jp/dbget-bin/www_bget?hsa:63036'
# ]
#
# for url in urls:
#     gene_crawler(url)