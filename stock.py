from typing import final
from webbrowser import BackgroundBrowser
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from secrets_1 import IEX_CLOUD_API_TOKEN


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def batch_call(my_columns, val):
    symbol_groups = list(chunks(stocks['Ticker'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))
        #print(symbol_strings)

    final_dataframe = pd.DataFrame(columns = my_columns)

    for symbol_string in symbol_strings:
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
        print(batch_api_call_url)
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            final_dataframe = final_dataframe.append(
                pd.Series(
                    [
                        symbol,
                        data[symbol]['quote']['latestPrice'],
                        data[symbol]['quote']['marketCap'],
                        'N/A',
                        data[symbol]['quote']['currency'],
                        data[symbol]['quote']['peRatio'],
                    ],
                    index = my_columns
                ),
                ignore_index=True
            )
    val = float(val)
    position_size = val/len(final_dataframe.index)
    for i in range(0, len(final_dataframe.index)):
        final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])

    #print(final_dataframe)
    return final_dataframe



stocks = pd.read_csv(r'C:\Users\coold\Desktop\Stock\sp500.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA', 'HFC','VIAC','WLTW'])]
my_columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy', 'Currency', 'PE Ratio']




orig_final_dataframe = batch_call(my_columns, 10000000)
orig_final_dataframe.sort_values('PE Ratio', ascending = False, inplace = True)
orig_final_dataframe = orig_final_dataframe[:50]
orig_final_dataframe.reset_index(drop = True, inplace = True)

writer = pd.ExcelWriter('cringe_trades.xlsx', engine = 'xlsxwriter')
orig_final_dataframe.to_excel(writer, 'Cringe Trades', index = False)

background_color = '#ffffff'
font_color = '#000000'

string_format = writer.book.add_format(
    {
        'font_color': font_color,
        'bg_color': background_color,
        'border':1
    }
)

dollar_format = writer.book.add_format(
    {
        'num_format': '$0.00',
        'font_color': font_color,
        'bg_color':background_color,
        'border':1
    }
)

integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color': font_color,
        'bg_color': background_color,
        'border':1
    }
)

column_formats = {
    'A':['Ticker', string_format],
    'B':['Stock Price', dollar_format],
    'C':['Market Capitalization', integer_format],
    'D':['Number of Shares to Buy', integer_format],
    'E':['Currencey', string_format],
    'F':['PE Ratio', integer_format]
}

for column in column_formats.keys():
    writer.sheets['Cringe Trades'].set_column(f'{column}:{column}', 25, column_formats[column][1])

writer.save()