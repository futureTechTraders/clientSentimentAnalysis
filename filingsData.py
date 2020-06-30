import nltk
import numpy as np
import pandas as pd 
import pickle
import pprint
import project_helper
from bs4 import BeautifulSoup
from tqdm import tqdm

cik_lookup = {
    'AMZN': '0001018724',
    #'BMY': '0000014272',   
    #'CNP': '0001130310',
    #'CVX': '0000093410',
    #'FL': '0000850209',
    #'FRT': '0000034903',
    #'HON': '0000773840'
}


sec_api = project_helper.SecAPI()

def get_sec_data(cik, doc_type, start = 0, count = 60):
    rss_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany' \
        '&CIK={}&type={}&start={}&count={}&owner=exclude&output=atom' \
        .format(cik, doc_type, start, count)
    sec_data = sec_api.get(rss_url)
    feed = BeautifulSoup(sec_data.encode('ascii'), 'xml').feed 
    entries = [
        (
        entry.content.find('filing-href').getText(),
        entry.content.find('filing-type').getText(),
        entry.content.find('filing-date').getText())
        for entry in feed.find_all('entry', recursive = False)]

    return entries

test_ticker = 'AMZN'
sec_data = {}
for ticker, cik in cik_lookup.items():
    sec_data[ticker] = get_sec_data(cik, '10-k')

#pprint.pprint(sec_data[test_ticker][:5]) 



raw_filings_by_ticker = {}

for ticker, data in sec_data.items():
    raw_filings_by_ticker[ticker] = {}
    for index_url, file_type, file_date in tqdm (data, desc= 'Downloading {} Filings'.format(ticker), unit = 'filling'):
        if(file_type == '10-K'):
            file_url = index_url.replace('-index.htm', '.txt').replace('txtl', '.txt')
            raw_filings_by_ticker[ticker][file_date] = sec_api.get(file_url)


print('Example Document: \n\n{}...'.format(next(iter(raw_filings_by_ticker[test_ticker].values()))[:1000]))














