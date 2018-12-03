import os
import ftplib
import json

import pandas as pd

import biomap.utils as utils
from biomap.core.insert import MapInserter

__LOCAL_PATH__ = utils.local_path('download/hgnc')

################################################################################
# HGNC
################################################################################

class HGNC(object):

    class FtpPaths(object):
        def __init__(self):
            self.root = 'pub/databases'

            self.items = {'non_alt_loci_set': 'genenames/new',
                          'hgnc_complete_set': 'genenames/new'}

        def __call__(self, item, file_format):
            file_name = item + '.' + file_format
            if file_format == 'txt':
                file_format = 'tsv'
            return '/'.join([self.root, self.items[item], file_format, file_name])

    class LocalPaths(object):
        def __init__(self, root):
            self.root = root

        def __call__(self, item, file_format):
            return os.path.join(self.root, item + '.' + file_format)


    def __init__(self, ftp_server = 'ftp.ebi.ac.uk',
                       local_path = __LOCAL_PATH__,
                       verbose = True):
        self.ftp_server = ftp_server
        self.ftp_path = self.FtpPaths()
        self.local_path = self.LocalPaths(local_path)
        self.verbose = verbose

    def download(self, item, file_format = 'txt'):

        def RETR(path):
            return 'RETR ' + path

        ftp_file = self.ftp_path(item, file_format)
        local_file = self.local_path(item, file_format)

        if self.verbose:
            print('\nDownloading {} from {}\n\n'.format(item, ftp_file))

        try:
            ftp = ftplib.FTP(self.ftp_server)
            ftp.login()
            ftp.retrbinary(RETR(ftp_file), open(local_file, 'wb').write)
        except:
            print('FTP ERROR.')

    def get_as_dataframe(self, item):
        local_file = self.local_path(item, file_format = 'txt')
        if not os.path.isfile(local_file):
            self.download(item, file_format = 'txt')
        return pd.read_table(local_file, low_memory = False)

    def get_as_json(self, item):
        local_file = self.local_path(item, file_format = 'json')
        if not os.path.isfile(local_file):
            self.download(item, file_format = 'json')
        with open(local_file, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)

    def get(self, item, how = 'dataframe'):
        if how == 'dataframe':
            return self.get_as_dataframe(item)
        elif how == 'json':
            return self.get_as_json(item)

############## HGNC complete ###################################################

class HGNCInserter(MapInserter):

    def __init__(self, **kwargs):
        self.hgnc = HGNC(**kwargs)
        self.docs = self.hgnc.get('hgnc_complete_set', 'json')['response']['docs']
        self.supported_keys = {
            key for doc in self.docs for key in doc.keys()
        }
        self.supported_keys = (self.supported_keys - {'pseudogene.org'}) | {'pseudogene_org'}
        self.list_valued_keys = {
            key for doc in self.docs
                for key in doc.keys()
                if isinstance(doc[key], list)
        }

    def mapper_data(self):
        '''
        Specific mapper_data documentation ...
        '''
        for doc in self.docs:
            if 'pseudogene.org' in doc.keys():
                # mongoDB does not tolerate dots in keys
                # TODO?: handle this generically in MapInserter.insert_mapper_data?
                doc['pseudogene_org'] = doc['pseudogene.org']
                del doc['pseudogene.org']
            if 'pubmed_id' in doc.keys():
                doc['pubmed_id'] = [str(ID) for ID in doc['pubmed_id']]
            if 'gene_family_id' in doc.keys():
                doc['gene_family_id'] = [str(ID) for ID in doc['gene_family_id']]
            if 'orphanet' in doc.keys():
                doc['orphanet'] = str(doc['orphanet'])
            if 'iuphar' in doc.keys():
                doc['iuphar'] = doc['iuphar'].strip(':')[1]
        return self.docs

    def mapper_definition(self):
        '''
        docs must be here.
        '''
        key_synonyms = {
                          'ensembl' : 'ensembl_gene_id',
                          'entrez'  : 'entrez_id',
                          'imgt_gene' : 'imgt'
                        }
        disjoint = ['uniprot_ids', 'refseq_accession']

        miriam_mapping = {
                           'hgnc_symbol' : 'symbol',
                           'hgnc' : 'hgnc_id',
                           'hgnc_genefamily': 'gene_family_id',
                           'omim' : 'omim_id',
                           'orphanet' : 'orphanet',
                           'ncbigene' : 'entrez_id',
                           'ensembl' : 'ensembl_gene_id',
                           'pubmed' : 'pubmed_id',
                           'cosmic' : 'cosmic',
                           'uniprot' : 'uniprot_ids',
                           'refseq' : 'refseq_accession',
                           'mgi' : 'mgd_id',
                           'rgd' : 'rgd',
                           'ccds' : 'ccds_id',
                           'ena_embl' : 'ena',
                           'merops' : 'merops',
                           'ec-code' : 'enzyme_id',
                           'iuphar_receptor' : 'iuphar',
                           'mirbase' : 'mirbase'
                         }

        return {
                 'name': 'hgnc',
                 'mapper_data' : 'hgnc',
                 'supported_keys': list(self.supported_keys),
                 'main_key' : 'symbol',
                 'key_synonyms' : key_synonyms,
                 'miriam_mapping' : miriam_mapping,
                 'list_valued_keys': list(self.list_valued_keys),
                 'disjoint' : disjoint
               }
