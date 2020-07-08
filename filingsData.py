import nltk
import numpy as np
import pandas as pd 
import pickle
import pprint
import project_helper
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from nltk.corpus import wordnet, stopwords
from nltk.stem import  WordNetLemmatizer
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import CountVectorizer

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


#print('Example Document: \n\n{}...'.format(next(iter(raw_filings_by_ticker[test_ticker].values()))[:1000]))


def get_documents(text):
    extracted_docs = []
    doc_start_pattern = re.compile(r"<DOCUMENT>")
    doc_end_pattern = re.compile(r"</DOCUMENT>")
    
    doc_start_is = [m.end() for m in doc_start_pattern.finditer(text)]
    doc_end_is  = [m.start() for m in doc_end_pattern.finditer(text)]

    for doc_start_i, doc_end_i in zip(doc_start_is, doc_end_is):
        extracted_docs.append(text[doc_start_i:doc_end_i])

    return extracted_docs

filling_documents_by_ticker = {}
for ticker,raw_fillings in raw_filings_by_ticker.items():
    filling_documents_by_ticker[ticker] = {}
    for file_date, filling in tqdm(raw_fillings.items(), desc = 'Getting documents from {} Filings'.format(ticker), unit = 'filling'):
        filling_documents_by_ticker[ticker][file_date] = get_documents(filling)

#print('\n\n'.join(['Document {} Filed on {}: \n{}...'.format(doc_i,file_date,doc[:200])
      #for file_date, docs in filling_documents_by_ticker[test_ticker].items()
      #for doc_i, doc in enumerate(docs)][:3]))


def get_document_type(doc):
    type_pattern = re.compile(r'<TYPE>[^\n]+')
    doc_type = type_pattern.findall(doc)[0][len('<TYPE>'):]

    return doc_type.lower()

ten_ks_by_ticker = {}
for ticker, filling_documents in filling_documents_by_ticker.items():
    ten_ks_by_ticker[ticker] = []
    for file_date, documents in filling_documents.items():
        for document in documents:
            if get_document_type(document) == '10-k':
                ten_ks_by_ticker[ticker].append({
                    'cik': cik_lookup[ticker],
                    'file': document,
                    'file_date': file_date
                })

#project_helper.print_ten_k_data(ten_ks_by_ticker[test_ticker][:5], ['cik','file','file_date'])

def remove_html_tags(text):
    text = BeautifulSoup(text, 'html.parser').get_text()
    return text

def clean_text(text):
    text = text.lower()
    text = remove_html_tags(text)
    return text


for ticker, ten_ks in ten_ks_by_ticker.items():
    for ten_k in tqdm(ten_ks,desc="Cleaning {} 10-Ks".format(ticker), unit="10-K"):
        ten_k['file clean'] = clean_text(ten_k['file'])

#project_helper.print_ten_k_data(ten_ks_by_ticker[test_ticker][:5], ['file clean'])

def lemmatize_words(words):
    lemmatized_words = [WordNetLemmatizer().lemmatize(word,'v') for word in words]
    return lemmatized_words

word_pattern = re.compile(r'\w+')

for ticker, ten_ks in ten_ks_by_ticker.items():
    for ten_k in tqdm(ten_ks, desc="Lemmatize {} 10-ks".format(ticker), unit='10-K'):
        ten_k['file_lemma'] = lemmatize_words(word_pattern.findall(ten_k['file clean']))

#project_helper.print_ten_k_data(ten_ks_by_ticker[test_ticker][:5],['file_lemma'])

lemma_english_stopwords =  lemmatize_words(stopwords.words('english'))
for ticker, ten_ks in ten_ks_by_ticker.items():
    for ten_k in tqdm(ten_ks,desc='Remove Stop Words for {} 10-Ks'.format(ticker), unit='10-K'):
        ten_k['file_lemma'] = [word for word in ten_k['file_lemma'] if word not in lemma_english_stopwords]

print('Stopwords removed')

#Loughran-McDonald sentiment word lists for analysis

sentiments = ['positive','negative','uncertainty','litigious','constraining','interesting']
sentiment_df = pd.read_csv('LoughranMcDonald_MasterDictionary_2018.csv')
sentiment_df.columns = [column.lower() for column in sentiment_df.columns]

#Removing unused information

sentiment_df = sentiment_df[sentiments + ['word']]
sentiment_df[sentiments] = sentiment_df[sentiments].astype(bool)
sentiment_df = sentiment_df[(sentiment_df[sentiments].any(1))]#check













