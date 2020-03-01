"""
kegg.py
"""
# -*- coding: utf-8 -*-

import re
import time
import requests
import traceback
import logging
import multiprocessing

from bs4 import BeautifulSoup

from kegg_code_list import target_kegg_list


pathway_url_form = 'https://www.genome.jp/dbget-bin/www_bget?hsa{}'


def remove_tag(content):
    html_tag = re.compile('<.*?>')
    modified_text = re.sub(html_tag, '', content)
    return modified_text


def kegg_urls():
    urls = []
    for kegg_id in target_kegg_list.keys():
        urls.append(pathway_url_form.format(kegg_id))
    return urls


def crawling_disease_name(tag):
    res = []
    disease_names_file = open('disease.tsv', 'a', encoding='utf-8')

    tables = tag.find('div').find_all('table')
    for table in tables:
        disease_id = table.find('a').string
        disease_name = table.find_all('td')[1].string
        disease = '\t'.join([disease_id, disease_name])
        res.append(disease_id)
        print(disease, file=disease_names_file)
    return res


def crawling_related_pathway(tag):
    res = []
    pathway_names_file = open('pathway.tsv', 'a', encoding='utf-8')

    related_pathways = tag.find_all('tr')
    for pwy in related_pathways:
        pathway_id = pwy.find('a').string
        pathway_name = pwy.find_all('td')[1].string
        pathway = '\t'.join([pathway_id, pathway_name])
        res.append(pathway_id)
        print(pathway, file=pathway_names_file)
    return res


def crawling_gene_name(tag):
    res = []
    gene_names_file = open('gene.tsv', 'a', encoding='utf-8')

    tables = tag.find('td')
    for table in tables:
        gene_id = table.find('nobr').find('a').string
        gene_name = remove_tag(str(table.find_all('td')[1]).split(';')[0])
        gene = '\t'.join([gene_id, gene_name])
        res.append(gene_id)
        print(gene, file=gene_names_file)
    return res


def crawling_datas(html):
    kegg_name = html.find('font', {"class": "title3"}).string.split(": ")[1].strip()
    tbody = html.find('td', {"class": "fr3"})
    tr_tags = tbody.find_all_next('tr')
    disease, pathway, gene = [], [], []

    for tr_tag in tr_tags:
        title = remove_tag(str(tr_tag.find('nobr')))
        if title == 'Disease':
            disease = crawling_disease_name(tr_tag)
        elif title == 'Relatedpathway':
            pathway = crawling_related_pathway(tr_tag)
        elif title == 'Gene':
            gene = crawling_gene_name(tr_tag)

    kegg_file = open('kegg.tsv', 'a', encoding='utf-8')
    print(kegg_name)
    print('\t'.join([kegg_name, ';'.join(disease), ';'.join(pathway), ';'.join(gene)]), file=kegg_file)


def kegg_crawling(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        crawling_datas(soup)
    except Exception as error:
        error_file = open('error_log.tsv', 'a', encoding='utf-8')
        print(url, file=error_file)
        print(error)
        logging.error(traceback.format_exc())   # logging


def main():
    start_time = time.time()
    urls = kegg_urls()
    pool = multiprocessing.Pool(processes=6)
    pool.map(kegg_crawling, urls)
    pool.close()
    pool.join()
    print("========== Process finished {}s ==========".format(time.time() - start_time))


main()
