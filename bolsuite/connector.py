#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Bolsuite Web API connector for Python
# https://github.com/crapher/bolsuite.python.git
#
# Copyright 2020 Diego Degese
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import requests as rq
import pandas as pd
import numpy as np
import json

class Connector():
    
    def __init__(self, base_url = 'http://localhost:6091'):
        self._base_url = base_url
    
    def _get_json(self, url):
        data = rq.get(url=url)
        
        if data.status_code == rq.codes.ok:
            return data.json()
                
        return json.loads("[]")

    def _get_dataframe(self, url):
        json = self._get_json(url)
        return pd.json_normalize(json)

    def _get_level2_dataframe(self, url):
        json = self._get_json(url)
        
        df = pd.DataFrame()

        def _get_level2_row(x, name, suffix, row):
            if type(x) is dict:
                for key in x:
                    _get_level2_row(x[key], name + key, suffix, row)
            elif type(x) is list:
                i = 1
                for item in x:
                    _get_level2_row(item, name, suffix + '.' + str(i), row)
                    i += 1
            else:
                if "Asks" in name:
                    name = name.replace('Asks', 'Ask')
                elif "Bids" in name:
                    name = name.replace('Bids', 'Bid')
                
                if "LastUpdate" in name and len(x) > 19:
                    x = x[:19] # Remove ms & Timezone data
                
                row[name + suffix] = x
                
            return row

        for item in json:
            row = _get_level2_row(item, name='', suffix='', row={})
            df = df.append(row, ignore_index=True)
            
        return df

    def _get_common_panel(self, url):
        df = self._get_dataframe(url)
        
        if not df.empty:
            df.drop(columns=['Source', 'Mode'], inplace=True)
            
            df.rename(columns={
                'Ask.Price': 'Ask',
                'Ask.Size': 'AskSize',
                'Bid.Size': 'BidSize',
                'Bid.Price': 'Bid',
                'LastQuote.DateTime': 'DateTime', 
                'LastQuote.Open': 'Open', 
                'LastQuote.High': 'High',
                'LastQuote.Low': 'Low', 
                'LastQuote.Close': 'Close', 
                'LastQuote.Volume': 'Volume'}, inplace=True)

            df['LastUpdate'] = df['LastUpdate'].str.slice(0, 19, 1)
            df['LastUpdate'] = pd.to_datetime(df['LastUpdate'], format='%Y-%m-%dT%H:%M:%S',errors='coerce')
            df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%dT%H:%M:%S',errors='coerce')
            
            df.replace({'Settlement': {0: '', 1: 'Spot', 2: '24hs', 3: '48hs'}}, inplace=True)
            df.set_index(['Symbol', 'Settlement'], inplace=True)
            
            df.sort_index(inplace=True)
        
        return df
    
    def _get_options_panel(self, url):
        df = self._get_common_panel(url)
        
        if not df.empty:
            df['Expiration'] = pd.to_datetime(df['Expiration'], format='%Y-%m-%dT%H:%M:%S',errors='coerce')

            if 'IntrisicValue' in df.columns: # Wrong column name to be fixed in a future Bolsuite version
                df.rename(columns={'IntrisicValue': 'IntrinsicValue'}, inplace=True)

            security_columns = [c for c in df.columns if c.lower()[:8] == 'security'] # Remove all the Security related columns
            df.drop(columns=security_columns, inplace=True)
        
        return df
        
    def _get_repos_panel(self, url):
        df = self._get_dataframe(url)
        
        if not df.empty:
            df.drop(columns=['Source', 'Mode'], inplace=True)
            
            df.rename(columns={
                'Ask.Value': 'AskValue',
                'Ask.Rate': 'AskRate',
                'Bid.Rate': 'BidRate',
                'Bid.Value': 'BidValue'}, inplace=True)

            df['LastUpdate'] = df['LastUpdate'].str.slice(0, 19, 1)
            df['LastUpdate'] = pd.to_datetime(df['LastUpdate'], format='%Y-%m-%dT%H:%M:%S',errors='coerce')
            df['Expiration'] = pd.to_datetime(df['Expiration'], format='%Y-%m-%dT%H:%M:%S',errors='coerce')
            
            df.set_index(['Days', 'Currency'], inplace=True)
            df.sort_index(inplace=True)
        
        return df
        
    def _get_quotes(self, url, isTick):
        df = self._get_dataframe(url)

        if not df.empty:
            df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%dT%H:%M:%S',errors='coerce')
            
            if isTick:
                df.drop(columns=['Open', 'High', 'Low'], inplace=True)
                df.rename(columns={'Close': 'Price'}, inplace=True)
            
        return df

    def _get_level2_quotes(self, url):
        df = self._get_level2_dataframe(url)
        
        if not df.empty:
            df.drop(columns=['Source', 'Mode'], inplace=True)
            
            lastupdate_columns = [c for c in df.columns if 'lastupdate' in c.lower()]
            df[lastupdate_columns] = df[lastupdate_columns].apply(pd.to_datetime, format='%Y-%m-%dT%H:%M:%S', errors='coerce')

            df.replace({'Settlement': {0: '', 1: 'Spot', 2: '24hs', 3: '48hs'}}, inplace=True)
            df.set_index(['Symbol', 'Settlement'], inplace=True)

        return df
        
    def indices(self, ticker = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/indices/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/indices'.format(self._base_url)
        
        return self._get_common_panel(url)

    def bluechips(self, ticker = None, settlement = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
            settlement : str
                Opcional. Si se requiere obtener un settlement especifico (Valores Validos: Spot - 24hs - 48hs)  
                Default: None
        """
        if ticker is not None:
            url = '{}/api/bluechips/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/bluechips'.format(self._base_url)
        
        if settlement is not None:
            url = '{}?settlement={}'.format(url, settlement)
            
        return self._get_common_panel(url)

    def general_board(self, ticker = None, settlement = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
            settlement : str
                Opcional. Si se requiere obtener un settlement especifico (Valores Validos: Spot - 24hs - 48hs)  
                Default: None
        """
        if ticker is not None:
            url = '{}/api/generalboard/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/generalboard'.format(self._base_url)
        
        if settlement is not None:
            url = '{}?settlement={}'.format(url, settlement)

        return self._get_common_panel(url)

    def cedear_stocks(self, ticker = None, settlement = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/cedearstocks/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/cedearstocks'.format(self._base_url)
        
        if settlement is not None:
            url = '{}?settlement={}'.format(url, settlement)

        return self._get_common_panel(url)

    def government_bonds(self, ticker = None, settlement = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/governmentbonds/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/governmentbonds'.format(self._base_url)
        
        if settlement is not None:
            url = '{}?settlement={}'.format(url, settlement)

        return self._get_common_panel(url)

    def government_short_term_bonds(self, ticker = None, settlement = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/governmentshorttermbonds/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/governmentshorttermbonds'.format(self._base_url)
        
        if settlement is not None:
            url = '{}?settlement={}'.format(url, settlement)

        return self._get_common_panel(url)

    def options(self, underlying_asset):
        """
        :Parametros:
            underlying_asset : str
                El activo del que se necesitan las opciones
        """
        if underlying_asset is None or underlying_asset == '':
            raise Exception('Underlying asset is None or invalid')
            
        url = '{}/api/options/{}'.format(self._base_url, underlying_asset)
        
        return self._get_options_panel(url)

    def repos(self, days = None, currency = None):
        """
        :Parametros:
            days : int
                Opcional. Cantidad de dias a la expiracion
                Default: None
            currency : str
                Opcional. La moneda de la caucion (Monedas validas: ARS,USD)
                Default: None
        """
        if days is not None and currency is not None:
            url = '{}/api/repos/{}/{}'.format(self._base_url, days, currency)
        elif days is not None and currency is None:
            url = '{}/api/repos/{}'.format(self._base_url, days)
        elif days is None and currency is not None:
            url = '{}/api/repos/{}'.format(self._base_url, currency)
        else:
            url = '{}/api/repos'.format(self._base_url)
        
        return self._get_repos_panel(url)

    def corporate_bonds(self, ticker = None, settlement = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/corporatebonds/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/corporatebonds'.format(self._base_url)
        
        if settlement is not None:
            url = '{}?settlement={}'.format(url, settlement)

        return self._get_common_panel(url)

    def adrs(self, ticker = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/adrs/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/adrs'.format(self._base_url)
        
        return self._get_common_panel(url)

    def currency_pairs(self, ticker = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/currencypairs/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/currencypairs'.format(self._base_url)
        
        return self._get_common_panel(url)

    def commodities(self, ticker = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/commodities/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/commodities'.format(self._base_url)
        
        return self._get_common_panel(url)

    def personal_portfolio(self, ticker = None):
        """
        :Parametros:
            ticker : str
                Opcional. Si se requiere obtener un ticker especifico
                Default: None
        """
        if ticker is not None:
            url = '{}/api/personalportfolio/{}'.format(self._base_url, ticker)
        else:
            url = '{}/api/personalportfolio'.format(self._base_url)
        
        return self._get_common_panel(url)

    def level_2_quotes(self, tickers):
        """
        :Parametros:
            tickers : list
                La lista de tickers de la cual se necesita la profundidad de mercado
        """
        if tickers is None or len(tickers) == 0:
            raise Exception('Tickers is None or empty')
            
        url = '{}/api/level2?symbols={}'.format(self._base_url, '|'.join(tickers))

        return self._get_level2_quotes(url)

    def intraday_quotes(self, ticker, timeframe=None, sort=None, filter=None, fillgap=None):
        """
        :Parametros:
            ticker : str
                El ticker del cual se necesita la informacion historica
            timeframe : int
                Opcional. El intervalo en minutos que se va a usar para agrupar la informacion.
                0: tick - Mayor que 0: Cantidad de minutos
                Default: 0
            sort : int
                Opcional. La forma en que se va a ordenar la informacion retornada. (Valores Validos: 0: Mas nuevo a mas viejo - 1: Mas viejo a mas nuevo)                
                Default: 1
            filter : int
                Opcional. La cantidad de minutos hacia atras que se requiere la informacion.
                Default: 1800
            fillgap : int
                Opcional. En los timeframe mayores a 0 (1: Llenar los espacios que no hubo cotizaciones con la ultima cotizacion - 0: No agregar informacion)
                Default: 0
        """
        
        if ticker is None or ticker == '':
            raise Exception('Ticker is None or invalid')

        params = []
        if timeframe is not None:
            params.append('timeframe={}'.format(timeframe));
        if sort is not None:
            params.append('sort={}'.format(sort));
        if filter is not None:
            params.append('filter={}'.format(filter));
        if fillgap is not None:
            params.append('fillgap={}'.format(fillgap));
        
        if len(params) > 0:
            url = '{}/api/intraday/{}?{}'.format(self._base_url, ticker, '&'.join(params))
        else:
            url = '{}/api/intraday/{}'.format(self._base_url, ticker)

        return self._get_quotes(url, timeframe is None or timeframe == 0)
