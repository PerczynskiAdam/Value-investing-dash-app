import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import re

from statistics import mean

data = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indis_df.csv', encoding = 'utf_8_sig')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([
   dbc.Row([
      dbc.Col(
         dcc.Dropdown(
            id = 'dynamic-start-date',
            options = [{"label": i, "value": i} for i in data[data.columns[0]].unique()],
            value = "2007-12-31"
         ), width ={"size": 4, "offset": 4}
      )
   ], style = {'margin-top': '1rem'}),
   dbc.Row([
      dbc.Col(
         dbc.Input(
            id = 'p/e-low',
            type = "number",
            placeholder = "C/Z większe od:",
            value = 5
         ), width = {"width":2}
      ),
      dbc.Col(
         dbc.Input(
            id = 'p/e-high',
            type = "number",
            placeholder = "C/Z mniejsze od:",
            value = 10
         ), width = {"width":2}
      ),
      dbc.Col(
         dbc.Input(
            id = 'roe-low',
            type = "number",
            placeholder = "ROE większe od:",
            value = 5
         ), width = {"width":2}
      ),
      dbc.Col(
         dbc.Input(
            id = 'roe-high',
            type = "number",
            placeholder = "ROE mniejsze od:",
            value = 10
         ), width = {"width":2}
      )
   ], justify = "center", style = {'margin-top': '1rem'}),
   dbc.Row([
      dbc.Col(
         dash_table.DataTable(
            id = "overall-table",
            page_size = 10,
            sort_action='native',
            style_header={ 'border': '1px solid black' },
            style_cell={ 'border': '1px solid grey' }
         ), width ={"size": 10, "offset": 1}
      )
   ], style = {'margin-top': '1rem'}),
   dbc.Row([
      dbc.Col(
         dcc.Dropdown(
            id = "dynamic-end-date",
            options = [{"label": i, "value": i} for i in data[data.columns[0]].unique()],
            value = "2019-12-31"
         ), width ={"size": 4, "offset": 4}
      )
   ], style = {'margin-top': '1rem'}),
   dbc.Row([
      dbc.Col(
         dash_table.DataTable(
            id = "start-table",
            page_size = 10,
            style_header={ 'border': '1px solid black' },
            style_cell={ 'border': '1px solid grey' }
         ), width ={"size": 4, "offset": 1}
      ),
      dbc.Col(
         dash_table.DataTable(
            id = "end-table",
            page_size = 10,
            style_header={ 'border': '1px solid black' },
            style_cell={ 'border': '1px solid grey' }
         ), width ={"size": 4, "offset": 2}
      )
   ], style = {'margin-top': '1rem'}),
   dbc.Row([
      dbc.Col(
         dash_table.DataTable(
            id = "diff-table",
            page_size = 10,
            style_header={ 'border': '1px solid black' },
            style_cell={ 'border': '1px solid grey' }
         ), width ={"size": 10, "offset": 1}
      )
   ], style = {'margin-top': '1rem'}),
   dbc.Row([
      dbc.Col(
         html.H5(
            children = "Średnia % zmiana kursu notowań w wybranym okresie:"
         ), width = {"width":4, "offset": 1}
      ),
      dbc.Col(
         id = "avg-change"
      )
   ], style = {'margin-top': '1rem'})
])

@app.callback(
   [Output("overall-table", "data"),
   Output("overall-table", "columns")],
   [Input("dynamic-start-date", "value"),
   Input("p/e-low", "value"),
   Input("p/e-high", "value"),
   Input("roe-low", "value"),
   Input("roe-high", "value")]
)

def update_overall_table(start_date, p_e_low, p_e_high, roe_low, roe_high):
   """ 
   Function serves the callback. It's transform the imported data.
   Args:
      start_date (date): choosen date to filter data
      p_e_low (float): Prize to Earning value to campare data with > sign
      p_e_high (float): Prize to Earning value to campare data with < sign
      roe_low (float): Return on equity value to campare data with > sign
      roe_high (float): Return on equity value to campare data with < sign
   Returns:
      Filtered data and columns names for dash_table component with id = "overall-table"
   """
   #load data
   data_table = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Indis_df.csv', encoding = 'utf_8_sig')
   #save chosen start_date to dataframe
   data_table = data_table[data_table["Data"] == start_date]
   #filtering data with chosen values
   data_table = data_table[(data_table["Cena / Zysk"] > p_e_low) & (data_table["Cena / Zysk"] <= p_e_high)]
   data_table = data_table[(data_table['ROE'] > roe_low) & (data_table['ROE'] <= roe_high)]
   #rounding all numeric values to 2 decimals
   data_table = data_table.round(2)
   #setting columns to variable for dash_table
   columns = [{"name": i, "id": i} for i in data_table.columns]
   return (data_table.to_dict("records"), columns)


@app.callback(
   [Output("start-table", "data"),
   Output("start-table", "columns")],
   [Input("overall-table", "data")]
)

def update_start_table(data):
   """ 
   Function serves the callback. It's transform the data gathered in previous step 
   Args:
      data (dict of data): choosen date to filter data
   Returns:
      Data with stock value for each ticker for chosen date in previous step and columns to dash_table
   """
   #save dict to dataframe
   filtered_data_table = pd.DataFrame.from_dict(data)
   #truncate data to exact columns
   filtered_data_table = filtered_data_table[["Data", "Ticker"]]
   #saving unique ticker values to list
   tickers = filtered_data_table['Ticker'].to_list()
   #declare empty list of dataframes
   list_of_dfs = []
   #for loop iterating over tickers
   for ticker in tickers:
      #loading stock data for ticker
      stock_data = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Notowania\{}_q.csv'.format(ticker.lower()), usecols = ["Data", "Zamkniecie"])
      #store ticker as values > needed for merging data
      stock_data["Ticker"] = ticker
      # merge data on Ticker and Data columns
      x = pd.merge(filtered_data_table, stock_data, on = ["Ticker", "Data"])
      #append dataframe to list od dfs
      list_of_dfs.append(x)
   #concatenating all dfs in list
   start_data = pd.concat(list_of_dfs)
   #rename column name
   start_data = start_data.rename(columns = {"Data": "Data początkowa"})
   #round all numeric values to 2 decimals
   start_data = start_data.round(2)
   #setting column names for variable
   columns = [{"name": i, "id": i} for i in start_data.columns]
   return (start_data.to_dict("records"), columns)


@app.callback(
   [Output("end-table", "data"),
   Output("end-table", "columns")],
   [Input("overall-table", "data"),
   Input("dynamic-end-date", "value")]
)

def update_end_table(data, end_date):
   """ 
   Function serves the callback. It's transform the data gathered in first step 
   Args:
      data (dict of data): choosen date to filter data
      end_date (date): End date for stock to analyze change of stock value in declared period by start_date (first step) and end_date
   Returns:
      Data with stock value for each ticker for chosen end_date and columns to dash_table
   """
   #save dict to dataframe
   filtered_data_table = pd.DataFrame.from_dict(data)
   #truncate data to exact columns
   filtered_data_table = filtered_data_table[["Ticker", "Data"]]
   #save chosen end_date to dataframe
   filtered_data_table["Data"] = end_date
   #saving unique ticker values to list
   tickers = filtered_data_table['Ticker'].to_list()
   #declare empty list of dataframes
   list_of_dfs = []
   #for loop iterating over tickers
   for ticker in tickers:
      #loading stock data for ticker
      stock_data = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Data\Notowania\{}_q.csv'.format(ticker.lower()), usecols = ["Data", "Zamkniecie"])
      #store ticker as values > needed for merging data
      stock_data["Ticker"] = ticker
      # merge data on Ticker and Data columns
      x = pd.merge(filtered_data_table, stock_data, on = ["Ticker", "Data"])
      #append dataframe to list od dfs
      list_of_dfs.append(x)
   #concatenating all dfs in list
   end_data = pd.concat(list_of_dfs)
   #rename column name
   end_data = end_data.rename(columns = {"Data": "Data końcowa"})
   #changing order of columns
   end_data = end_data[["Data końcowa", "Ticker", "Zamkniecie"]]
   #round all numeric values to 2 decimals
   end_data = end_data.round(2)
   #setting column names for variable
   columns = [{"name": i, "id": i} for i in end_data.columns]
   return (end_data.to_dict("records"), columns)

@app.callback(
   [Output("diff-table", "data"),
   Output("diff-table", "columns")],
   [Input("start-table", "data"),
   Input("end-table", "data")]
)

def update_diff_table(startdata, enddata):
   """ 
   Function serves the callback. It merged the data from previous steps with start_date and end_date
   Args:
      startdata (dict of data): data with stocks value for start_date
      enddata (dict of data): data with stocks value for end_date
   Returns:
      Data with percentage and column names for stocks and dates chosen in previous steps
   """
   #save dict to dataframe
   startdata = pd.DataFrame.from_dict(startdata)
   #drop column from dataframe
   startdata.drop(columns = "Data początkowa", inplace = True)
   #rename column
   startdata = startdata.rename(columns = {"Zamkniecie": "Zamkniecie początek"})
   #save dict to dataframe
   enddata = pd.DataFrame.from_dict(enddata)
   #drop column from dataframe
   enddata.drop(columns = "Data końcowa", inplace = True)
   #rename column
   enddata = enddata.rename(columns = {"Zamkniecie": "Zamkniecie koniec"})
   #merging data on Ticker, how = inner to drop stocks withouts stock values
   diff_data = pd.merge(startdata, enddata, on = "Ticker", how = "inner")
   #calculating percentage change
   diff_data["Zmiana %"] = (diff_data["Zamkniecie koniec"].values - diff_data["Zamkniecie początek"].values)/diff_data["Zamkniecie początek"].values*100
   #rounding all numeric values to 2 decimals
   diff_data = diff_data.round(2)
   #setting columns to variable for dash_table
   columns = [{"name": i, "id": i} for i in diff_data.columns]
   return (diff_data.to_dict("records"), columns)

@app.callback(
   Output("avg-change", "children"),
   [Input("diff-table", "data")]
)

def calc_avg_change(diffdata):
   """ 
   Function serves the callback. It's calculating average change for group of stocks
   Args:
      diffdata (dict of data): data with stocks value for start_date and end_date
   Returns:
      Average percent change for chosen stocks
   """
   #save dict to dataframe
   diffdata = pd.DataFrame.from_dict(diffdata)
   #saving series to variable
   changes = diffdata["Zmiana %"]
   #calculating mean for series
   avg_change = mean(changes)
   return round(avg_change, 2)

if __name__ == '__main__':
    app.run_server(debug=True)