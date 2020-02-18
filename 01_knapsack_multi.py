"""
01_knapsack.py
"""
# -*- coding: utf-8 -*-

import re
import json
import requests
import traceback
import logging

from bs4 import BeautifulSoup

path_out_file = '/Users/ask4git/Desktop/test_knapsack_crawling_result.json'
test_url = 'http://www.knapsackfamily.com/knapsack_core/information.php?sname=C_ID&word=C00000001'
url_form = 'http://www.knapsackfamily.com/knapsack_core/information.php?sname=C_ID&word=C{}'
num_of_url = 52044


def target_urls(form, num_url):
    for i in range(1, num_url + 1):
        yield form.format(str(i).zfill(8))


def get_tag_text(tag, key):
    return tag.find(key).string if tag.find(key) else None


def crawling_tag(context, tag, tag_name):
    if get_tag_text(tag, 'th') == tag_name:
        context.update({tag_name: get_tag_text(tag, 'td')})


def metabolite_information(soup, result):
    table = soup.find('table', class_='d3')
    all_tr_tags = table.find_all_next('tr')

    for tr_tag in all_tr_tags:
        crawling_tag(result, tr_tag, 'Name')  # Name
        crawling_tag(result, tr_tag, 'SMILES')  # SMILES


def organism_information(soup, result):
    organism_info = []
    table = soup.find('table', class_='org')
    all_tr_tags = table.find_all('tr')

    for tr_tag in all_tr_tags:
        th_tags = tr_tag.find_next('td')
        print(th_tags)
        family = get_tag_text(th_tags, 'td')
        print(family)
    #
    #     family = th_tags[0].find('td').string
    #     species = th_tags[1].find('td').string
    #     organism_info.append((family, species))
    #
    # result.update({'Organism': organism_info})


def knapsack_crawling(target_url):
    crawling_result = {}

    try:
        res = requests.get(target_url)
        soup = BeautifulSoup(res.content, 'html.parser')

        # remove <br> tag
        origin_text = str(soup)
        modified_text = re.sub('<br/>', '  ', origin_text)
        soup = BeautifulSoup(modified_text, 'html.parser')

        # crawling
        metabolite_information(soup, crawling_result)
        # organism_information(soup, crawling_result)

    except Exception as error:
        logging.error(traceback.format_exc())   # logging

    print(crawling_result)


def test():
    cnt = 10
    for url in target_urls(url_form, num_of_url):
        knapsack_crawling(url) if cnt != 0 else exit(0)
        cnt -= 1


def main():
    for url in target_urls(url_form, num_of_url):
        knapsack_crawling(url)


# test
test()


# # main
# main()
