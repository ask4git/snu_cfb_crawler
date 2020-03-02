"""
kegg_gene_model.py
"""
# -*- coding: utf-8 -*-

import re


def remove_tag(content):
    html_tag = re.compile('<.*?>')
    modified_text = re.sub(html_tag, '', str(content))
    return modified_text


class Gene:
    def __init__(self, url, html):
        self.__initialize(url, html)
        self.__set_entry()
        self.__crawling_body()

    # Initialize
    def __initialize(self, url, html):
        self.__url = url
        self.__html = html
        self.entry = ''
        self.gene_name = ''
        self.gene_sub_names = []
        self.pathway = []
        self.structure = []
        self.sequence = ''

    # Entry
    def __set_entry(self):
        try:
            font_title = self.__html.find('font', {'class': 'title1'})

            if not font_title:
                raise EntryNotFoundError('Can\'t find entry data.')
            self.entry = font_title.string.split(':')[1].strip()

        except EntryNotFoundError as error:
            print(self.__url)
            print(error)

    # Gene name
    def __set_gene_name(self, tr_tag):
        genes = remove_tag(tr_tag.find('div')).split(',')
        for gene_index, gene in enumerate(genes):
            self.gene_name = gene.strip() if gene_index == 0 \
                else self.gene_sub_names.append(gene.strip())

    # Pathway
    def __set_pathway(self, tr_tag):
        pathways = tr_tag.find_all('tr')
        for pathway in pathways:
            pathway_id = pathway.find('a').string
            pathway_name = pathway.find_all('td')[1].string
            self.pathway.append(':'.join([pathway_id, pathway_name]))

    # Structure
    def __set_structure(self, tr_tag):
        pdb = tr_tag.find_all('a')
        for p in pdb:
            if p.string:
                self.structure.append(p.string.strip())

    # Sequence
    def __set_sequence(self, tr_tag):
        context = remove_tag(tr_tag.find('td')).strip().split('\n')
        sequence = ''.join(context[1:])
        self.sequence = sequence

    def __crawling_body(self):
        # Gene 페이지마다 class 명칭이 다른 경우가 종종 있음
        try:
            tbody_class_names = ['fr1', 'fr3']
            tbody = self.__html.find('td', {"class": tbody_class_names[0]})
            if tbody:
                tr_tags = tbody.find_all_next('tr')
            else:
                raise TBodyNotFound('Can\'t find entry data.')
        except TBodyNotFound as error:
            print(self.__url)
            print(error)
            return None

        for tr_tag in tr_tags:
            title = remove_tag(str(tr_tag.find('nobr')))

            if title == 'Gene name':
                self.__set_gene_name(tr_tag)
            elif title == 'Pathway':
                self.__set_pathway(tr_tag)
            elif title == 'Structure':
                self.__set_structure(tr_tag)
            elif title == 'AA seq':
                self.__set_sequence(tr_tag)

    def serialize(self):
        _entry = self.entry or '_'
        _gene_name = self.gene_name or '_'
        _gene_sub_name = '::'.join(self.gene_sub_names) or '_'
        _pathway = '::'.join(self.pathway) or '_'
        _structure = '::'.join(self.structure) or '_'
        _sequence = self.sequence or '_'
        return '\t'.join([_entry, _gene_name, _gene_sub_name, _pathway, _structure, _sequence])


class EntryNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'[{self.__class__.__name__}'


class TBodyNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'{self.__class__.__name__}'
