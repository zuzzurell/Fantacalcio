#!/usr/bin/env python
# coding: utf-8

# In[10]:


import requests
import re
import glob
import pandas as pd
import os
import wget


'''Estrarre I data frame delle stagioni calcistiche'''

class Fantacalcio():
    '''Scaricare le statistiche dei calciatori e le quotazioni da Fantacalcio.it'''

    def __init__(self, numero_stagioni: int):

        self.numero_stagioni: list = numero_stagioni
            
            
    def anno_stagione(self):
        '''
        Prende il numero di stagioni e convertile in anni e prima e
        seconda parte della stagione
        '''
        parte_1 = []
        parte_2 = []
    
        for i in range(1,self.numero_stagioni):
            parte_1.append(int(pd.to_datetime('now').strftime('%Y')) - i)
            parte_2.append(int(pd.to_datetime('now').strftime('%Y')) +1 - i)

        return parte_1,parte_2
    
    def valore_stagione(self,parte_1,parte_2):
        '''Crea l argomento stagione nel formato 2021-22'''
        
        fine_stag = [fin - 2000 for fin in parte_2]
        stagioni = [str(anno_1)+"-"+str(anno_2) for anno_1,anno_2 in zip(parte_1,fine_stag)]

        return stagioni


    def sito_fanta(self,stagioni):
        '''Accedere alla pagina con le statistiche e con le quotazioni'''

        urls = []
        for s in stagioni:
            url = 'https://www.fantacalcio.it/statistiche-serie-a/'+str(s)+'/fantacalcio/medie'
            urls.append(url)

        quota = 'https://www.fantacalcio.it/quotazioni-fantacalcio'
        urls.append(quota)

        return urls         


    def stats_e_quota_excel(self,urls):
        '''
        Url del excel dove le stats o le quotazioni per le stagioni indicate
        sono salvate
        '''

        excel_url = []
        for url in urls: 
            req=requests.get(url).text
            excel_location = re.search('location.href = (.+?)"', req)
            excel_url.append(excel_location.group(1).replace('"',''))


        return excel_url


    def scaricare_frame(self,path,excel_url):

        '''
        Scaricare i file excel nel path selezionato, cancella file
        se duplicato
        '''
        for f in glob.glob(path+"/*.xlsx"):
            os.remove(f)

        [wget.download(req, out = path)for req in excel_url]


