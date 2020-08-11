# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:36:47 2020

@author: AdamPer
"""

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re


tickers = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Valueinvesting\gpw_tickers.csv')

war_ryn_dict_of_df = {}
war_ryn_dict_of_list = {}

def get_war_ryn_info(stock):
    '''
    Getting market value info about each stock
    
    Args:
        stock (list of strings)
    Returns:
        Dataframe dictionary of dataframes for each ticker
    '''
    try:
        html_file = urllib.request.urlopen('https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/'+stock)
        soup = BeautifulSoup(html_file, 'lxml')

        rows = []
        for dat in soup.find_all('th', class_ = re.compile('thq h+')):
            #compile adds the newest value to table
            rows.append(re.search(r'\d\d\d\d/Q\d', dat.text).group(0))
  
        # columns = []
        # for tyt_tab in soup.find_all('td', class_ ='f'):
        #     columns.append(tyt_tab.text)
        columns = ['Cena / Wartość księgowa', 'Cena / Zysk']
        
        # fields = [item['data-field'] for item in soup.find_all('tr', attrs = {'data-field': True})]
        fields = ['CWKCurrent', 'CZCurrent']
        #selecting fields that we want to scrap
        row_data = []
        for field in fields:
            for war in soup.find(attrs = {f'data-field': '{}'.format(field)}).find_all('td', class_ = 'h'):
                if war.span is None:
                    row_data.append(np.nan)
                else:
                    row_data.append(float(war.span.text.replace(' ', '')))
                    #change the space to change the value to float
        for field in enumerate(fields):       
            war_ryn_dict_of_list["war_ryn_{}".format(field[1])] = np.array_split(row_data, len(fields))[field[0]].astype(np.float)
        war_ryn_dict_of_list['rows'] = np.array(rows)
        #setting names for rows 

    
        war_ryn_dict_of_df["{}".format(stock)] = pd.DataFrame.from_dict(war_ryn_dict_of_list)
        war_ryn_dict_of_df["{}".format(stock)].set_index('rows', inplace = True)
        war_ryn_dict_of_df["{}".format(stock)].columns = columns
    except Exception as e:
        print(stock, str(e))



for eachstock in tickers:
    get_war_ryn_info(eachstock)


df_war_ryn = pd.concat(war_ryn_dict_of_df)


df_war_ryn.to_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indicators\wart_rynkowa.csv', encoding = 'utf_8_sig')

# =============================================================================


# =============================================================================
# profitability

rent_dict_of_df = {}
rent_dict_of_list = {}   
def get_rento_info(stock):
    '''
    Getting revenue info about each stock

    Args:
        stock (list of strings)
    Returns:
        Dataframe dictionary of dataframes for each ticker
    '''
    try:
        html_file = urllib.request.urlopen('https://www.biznesradar.pl/wskazniki-rentownosci/'+stock)
        soup = BeautifulSoup(html_file, 'lxml')
        #wiersze
        rows = []
        for dat in soup.find_all('th', class_ = re.compile('thq h+')):
            rows.append(re.search(r'\d\d\d\d/Q\d', dat.text).group(0))
        #kolumny    
        columns = ['ROE', 'Marża zysku operacyjnego']
        # columns = []
        # for tyt_tab in soup.find_all('td', class_ ='f'):
        #     # print(tyt_tab.prettify())
        #     columns.append(tyt_tab.text)
        
        # fields = [item['data-field'] for item in soup.find_all('tr', attrs = {'data-field': True})]
        fields = ['ROE', 'OPM']
        row_data = []
        for field in fields:
            for war in soup.find(attrs = {f'data-field': '{}'.format(field)}).find_all('td', class_ = 'h'):
                if war.span is None:
                    row_data.append(np.nan)
                else:
                    row_data.append(war.span.text.replace(' ', ''))                             
        for field in enumerate(fields):       
            rent_dict_of_list["rentownosc_{}".format(field[1])] = np.array_split(row_data, len(fields))[field[0]]
        rent_dict_of_list['rows'] = np.array(rows)
    
        rent_dict_of_df["{}".format(stock)] = pd.DataFrame.from_dict(rent_dict_of_list)
        rent_dict_of_df["{}".format(stock)].set_index('rows', inplace = True)
        rent_dict_of_df["{}".format(stock)].columns = columns
    except Exception as e:
        print(stock, str(e))



for eachstock in tickers:
    get_rento_info(eachstock)
    
df_rent = pd.concat(rent_dict_of_df)


df_rent.to_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indicators\rentownosc.csv', encoding = 'utf_8_sig')

# =============================================================================
# Debt info
debt_dict_of_df = {}
debt_dict_of_list = {}   
def get_debt_info(stock):
    '''
    Getting debt info about each stock

    Args:
        stock (list of strings)
    Returns:
        Dataframe dictionary of dataframes for each ticker
    '''
    try:
        html_file = urllib.request.urlopen('https://www.biznesradar.pl/wskazniki-zadluzenia/'+stock)
        soup = BeautifulSoup(html_file, 'lxml')
    #wiersze
        rows = []
        for dat in soup.find_all('th', class_ = re.compile('thq h+')):#ogarnac jak dodac ostatnia wartosc za pomoca reg exp
            rows.append(re.search(r'\d\d\d\d/Q\d', dat.text).group(0))
        #kolumny    
        columns = ['Zadłużenie ogólne']
        # columns = []
        # for tyt_tab in soup.find_all('td', class_ ='f'):
        #     # print(tyt_tab.prettify())
        #     columns.append(tyt_tab.text)
        
        # fields = [item['data-field'] for item in soup.find_all('tr', attrs = {'data-field': True})]
        fields = ['DTAR']
        row_data = []
        for field in fields:
            for war in soup.find(attrs = {f'data-field': '{}'.format(field)}).find_all('td', class_ = 'h'):
                if war.span is None:
                    row_data.append(np.nan)
                else:
                    row_data.append(float(war.span.text.replace(' ', '')))                               
        for field in enumerate(fields):       
            debt_dict_of_list["zadl_{}".format(field[1])] = np.array_split(row_data, len(fields))[field[0]].astype(np.float)
        debt_dict_of_list['rows'] = np.array(rows)
    
        debt_dict_of_df["{}".format(stock)] = pd.DataFrame.from_dict(debt_dict_of_list)
        debt_dict_of_df["{}".format(stock)].set_index('rows', inplace = True)
        debt_dict_of_df["{}".format(stock)].columns = columns
    except Exception as e:
        print(stock, str(e))



for eachstock in tickers:
    get_debt_info(eachstock)
               
       
df_debt = pd.concat(debt_dict_of_df)
df_debt.to_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indicators\zadluzenie_tel.csv', encoding = 'utf_8_sig')



# =============================================================================
# liquidity
liq_dict_of_df = {}
liq_dict_of_list = {}   
def get_plynn_info(stock):
    '''
    Getting liquidity info about each stock

    Args:
        stock (list of strings)
    Returns:
        Dataframe dictionary of dataframes for each ticker
    '''
    try:
        html_file = urllib.request.urlopen('https://www.biznesradar.pl/wskazniki-plynnosci/'+stock)
        soup = BeautifulSoup(html_file, 'lxml')
    #wiersze
        rows = []
        for dat in soup.find_all('th', class_ = re.compile('thq h+')):
            rows.append(re.search(r'\d\d\d\d/Q\d', dat.text).group(0))
        #kolumny    
        columns = ['Płynność bieżąca']
        # columns = []
        # for tyt_tab in soup.find_all('td', class_ ='f'):
        #     # print(tyt_tab.prettify())
        #     columns.append(tyt_tab.text)
        
        # fields = [item['data-field'] for item in soup.find_all('tr', attrs = {'data-field': True})]
        fields = ['CR']
        row_data = []
        for field in fields:
            for war in soup.find(attrs = {f'data-field': '{}'.format(field)}).find_all('td', class_ = 'h'):
                if war.span is None:
                    row_data.append(np.nan)
                else:
                    row_data.append(float(war.span.text.replace(' ', '')))                               
        for field in enumerate(fields):       
            liq_dict_of_list["plynn_{}".format(field[1])] = np.array_split(row_data, len(fields))[field[0]].astype(np.float)
        liq_dict_of_list['rows'] = np.array(rows)
    
        liq_dict_of_df["{}".format(stock)] = pd.DataFrame.from_dict(liq_dict_of_list)
        liq_dict_of_df["{}".format(stock)].set_index('rows', inplace = True)
        liq_dict_of_df["{}".format(stock)].columns = columns
    except Exception as e:
        print(stock, str(e))



for eachstock in tickers:
    get_plynn_info(eachstock)
               
df_liq = pd.concat(liq_dict_of_df)
df_liq.to_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indicators\plynnosc_tel.csv', encoding = 'utf_8_sig')


# =============================================================================
# Przeplywy pieniezne
przep_dict_of_df = {}
przep_dict_of_list = {}   
def get_przep_info(stock):
    '''
    Getting przep info about each stock
    
    Args:
        stock (list of strings)
    Returns:
        Dataframe dictionary of dataframes for each ticker
    '''
    try:
        html_file = urllib.request.urlopen('https://www.biznesradar.pl/wskazniki-przeplywow-pienieznych/'+stock)
        soup = BeautifulSoup(html_file, 'lxml')
    #wiersze
        rows = []
        for dat in soup.find_all('th', class_ = re.compile('thq h+')):
            rows.append(re.search(r'\d\d\d\d/Q\d', dat.text).group(0))
        #kolumny    
        columns = ['Udział zysku netto w przepływach operacyjnych']
        # columns = []
        # for tyt_tab in soup.find_all('td', class_ ='f'):
        #     # print(tyt_tab.prettify())
        #     columns.append(tyt_tab.text)
        
        # fields = [item['data-field'] for item in soup.find_all('tr', attrs = {'data-field': True})]
        fields = ['ZNPO']
        row_data = []
        for field in fields:
            for war in soup.find(attrs = {f'data-field': '{}'.format(field)}).find_all('td', class_ = 'h'):
                if war.span is None:
                    row_data.append(np.nan)
                else:
                    row_data.append(war.span.text.replace(' ', ''))                              
        for field in enumerate(fields):       
            przep_dict_of_list["przep_{}".format(field[1])] = np.array_split(row_data, len(fields))[field[0]]
        przep_dict_of_list['rows'] = np.array(rows)
    
        przep_dict_of_df["{}".format(stock)] = pd.DataFrame.from_dict(przep_dict_of_list)
        przep_dict_of_df["{}".format(stock)].set_index('rows', inplace = True)
        przep_dict_of_df["{}".format(stock)].columns = columns
    except Exception as e:
        print(stock, str(e))



for eachstock in tickers:
    get_przep_info(eachstock)
               
df_przep = pd.concat(przep_dict_of_df)
df_przep.to_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indicators\przeplywy_tel.csv', encoding = 'utf_8_sig')
