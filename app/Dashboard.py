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

#import data
df = pd.read_csv('https://raw.githubusercontent.com/PerczynskiAdam/Value-investing-dash-app/master/Indi_db/truncated_db.csv', index_col = 0, encoding = 'utf_8_sig')

df_map = pd.read_csv('https://raw.githubusercontent.com/PerczynskiAdam/Value-investing-dash-app/master/Macro_db/Eu_iso_gdp.csv', index_col  = 0, encoding = 'utf_8_sig')

df_ind = pd.read_csv('https://raw.githubusercontent.com/PerczynskiAdam/Value-investing-dash-app/master/Macro_db/trun_index_data.csv', index_col = 0, encoding = 'utf_8_sig')

sector_dict = {'GPW Informatyka': ['11B', 'ABS', 'ACP', 'ALL', 'ART', 'ASE', 'ATD', 'BBT', 'BCM',
       'CDR', 'CIG', 'CMP', 'CMR', 'CTG', 'DAT', 'DTR', 'ELZ', 'GOP',
       'IFI', 'LRK', 'LSI', 'LVC', 'MDG', 'NTT', 'OPM', 'PCG', 'PLW',
       'PRD', 'PSW', 'QNT', 'R22', 'SGN', 'SME', 'SVRS', 'TBL', 'TEN',
       'TLX', 'U2K', 'ULG', 'VVD', 'WAS', 'XTP'],
       'GPW Telekomunikacja': ['ATM', 'CPS', 'MTL', 'MXC', 'NET', 'OPL', 'PLY']}

sectors = list(sector_dict.keys())

scopes = ["world", "europe", "asia", "africa", "north america", "south america"]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


app.layout = html.Div([
   dcc.Tabs(children = [
      dcc.Tab(label = 'Makro', children = [
         html.Div([
            dbc.Row([
               dbc.Col(
                  html.H2(
                     children = 'GDP and stock market index of country',
                     style = {
                        'margin-left': '1rem'
                     }
                  ), width = 'auto'
               )
            ], style = {
               'background-color': '#58595B',
               'margin-top': '0.5rem',
               'margin-bottom': '0.5rem'
            }
            ),
            dbc.Row([
               dbc.Col(
                  html.Div([
                     dcc.Dropdown(
                        id = 'scope',
                        options = [{'label': i.capitalize(), 'value':i} for i in scopes],
                        value = 'europe'
                     ),
                     dcc.Graph(
                        id = 'map-chart',
                        style = {'height': '865px'}
                        )
                  ]), width = 6
               ),
               dbc.Col(
                  html.Div([
                     dcc.Graph(
                        id = 'pkb-line-chart',
                        style = {
                           'margin-bottom': '0.5rem'
                        }
                     ),
                     dcc.Graph(
                        id = 'index-line-chart'
                     )
                  ]), width = 6
               )
            ], align = 'center')
         ])
      ], selected_style = {
         'color': 'black',
         'box-shadow': '2px 4px #FF851B',
         'border-left': '1px solid #F1F2F2',
         'border-right': '1px solid #F1F2F2',
         'border-top': '1px solid #F1F2F2'
         }
      ),
      dcc.Tab(
         label = 'Analiza giełdy',
         disabled = True
      ),
      dcc.Tab(label = 'Analiza branży', children = [#Sector tab
         html.Div([
            dbc.Row([
               dbc.Col(
                  html.H2(
                     children = "Tabela danych",
                     style = {
                        'margin-left': '1rem'
                     }
                  )
               )
            ],
            style = {
               'background-color': '#58595B',
               'margin-top': '0.5rem',
               'margin-bottom': '0.5rem'
            }
            ),
            dbc.Row(
               dbc.Col(
                  dcc.Dropdown(
                     id = "table-date",
                     options = [{'label': i, 'value': i} for i in df.index.unique()],
                     value = "2019-12-31",
                     style ={
                        'margin': '0.5rem',
                        'width': '10rem'
                     }
                  )
               )
            ),
            dbc.Row(
               dbc.Col(
                  dash_table.DataTable(
                     style_header={
                        'height': 'auto',
                     },
                     id = 'table',
                     columns = [{"name": i, "id": i} for i in df.columns],
                     page_size = 10,
                     filter_action = "native",
                     sort_action="native",
                  ),
                  width = {"size": 8, "offset": 2},
                  style ={
                     'margin-left': '2rem',
                  }
               )
            ),
            dbc.Row([
               dbc.Col(
                  html.H2(
                     children = 'Branża:',
                     style = {
                        'margin-left': '1rem'
                     }
                  ), width = 'auto'
               ),
               dbc.Col(
                  dcc.Dropdown(
                     id = 'sector',
                     options = [{'label': i, 'value': i} for i in sectors],
                     value = sectors[0]
                  ), width = 2, align = 'center'
               )
            ], style = {
               'background-color': '#58595B',
               'margin-top': '0.5rem',
               'margin-bottom': '0.5rem'
            }
            ),
            dbc.Row(
               dbc.Col(
                  dcc.Dropdown(
                     id = 'dynamic-indi',
                     options = [{'label': i, 'value':i} for i in df.columns[1:]],
                     value = ['Cena / Zysk', 'ROE'],
                     multi = True,
                     style = {
                        'margin-left': '0.5rem'
                     }
                  ), width = 'auto'
               )
            ),
            dbc.Row(
               id = 'container-tab1'
            )
         ])
      ], selected_style = {
         'color': 'black',
         'box-shadow': '2px 4px #FF851B',
         'border-left': '1px solid #F1F2F2',
         'border-right': '1px solid #F1F2F2',
         'border-top': '1px solid #F1F2F2'
         }
      ),
      dcc.Tab(label = 'Analiza spółki', children = [#Stock tab
         html.Div([
            dbc.Row([
               dbc.Col(
                  html.H2(
                     children = 'Spółka:',
                     style = {
                        'margin-left': '1rem'
                     }
                  ), width = 'auto'
               ),
               dbc.Col(
                  dcc.Dropdown(
                     id = 'dynamic-stock-ticker',
                     options = [{'label': i, 'value':i} for i in df['Ticker'].unique()],
                     value = df['Ticker'].unique()[0]
                  ), width = 1, align = 'center'
               )
            ], style = {
               'background-color': '#58595B',
               'margin-top': '0.5rem',
               'margin-bottom': '0.5rem'
            }
            ),
            dbc.Row([
               dbc.Col(
                  dbc.Button(
                     children = 'Dodaj wykres', 
                     id = 'add-chart-tab2', 
                     n_clicks = 0,
                     color = 'primary',
                     style = {
                        'margin-left': '0.5rem'
                     }
                  ), width = 'auto'
               )
            ]),
            dbc.Row(
               id = 'container-tab2',
               children = []
            )
         ]) 
      ], selected_style = {
         'color': 'black',
         'box-shadow': '2px 4px #FF851B',
         'border-left': '1px solid #F1F2F2',
         'border-right': '1px solid #F1F2F2',
         'border-top': '1px solid #F1F2F2'
         }
      )#Style for selected tab (not content of the tab)
   ], style = {'borderBottom': '1px solid #d6d6d6', 'fontWeight': 'bold'})#Style of all Tabs
])

############################## Content of Tab-1
#Map chart
def create_map(scope):
   """
   Function creates Choropleth mapchart
   
   Args:
      scope (String corresponds to area of map to plot)
   Returns:
      Display map for the choosen scope from dcc Dropdown
   """
   fig = go.Figure()
   fig.add_trace(go.Choropleth(
      locations = df_map['Code'],
      z = df_map[df_map.columns[-2]].astype(float),
      text = df_map.index,
      colorbar_title = dict(text = 'Thousands<br>US$')
   ))
   fig.update_layout(
      geo = dict(
         scope = scope,
         projection_type = 'natural earth',
         bgcolor = '#939598'
      ),
      title = dict(text = '{}<br>GDP per capita'.format(scope.capitalize())),
      margin = dict(
         t = 45,
         r = 35,
         b = 45,
         l = 35
      ),
      paper_bgcolor = '#F2F8FD'
   )
   return fig

@app.callback(
   Output('map-chart', 'figure'),
   [Input('scope', 'value')]
)

def update_scope(scope):
   """
   Function serves a callback that passes a scope variable to create_map function
   """
   return create_map(scope)

#Gdp line chart
def create_pkb_linechart(country):
   """
   Fucntion creates gdp line chart for choosen country

   Args:
      country (String with name of country)

   Returns:
      GDP line chart for country choosen by clicking at Choropleth map
      If country name not in dataframe function return empty graph objects
   """
   if country not in df_map.index.unique():
      return {}
   else:
      fig = go.Figure()
      fig.add_trace(go.Scatter(
         x = df_map.columns,
         y = list(df_map[df_map.index == country].iloc[0])[:-1],
         marker_color = '#FF851B'#Color of line
      ))
      fig.update_layout(title = '{}<br>GDP per capita'.format(country),
      xaxis = dict(
         showgrid = False,
         ticks = 'inside',
         tickwidth = 2,
         tickangle = 45,
         tickfont = dict(
            size = 14
         )
      ),
      yaxis = dict(
         title_text = 'GDP'
      ),
      paper_bgcolor = '#F2F8FD',
      plot_bgcolor = '#F2F4F6'
      )
      return fig

@app.callback(
   Output('pkb-line-chart', 'figure'),
   [Input('map-chart', 'clickData')]
)

def update_pkb_line_chart(clickData):
   """
   Function serves a callback that passes a clickData value as a variable to pkb line chart
   """
   if clickData is None:
      return create_pkb_linechart(country = 'Poland')
   else:
      country = clickData['points'][0]['text']
      return create_pkb_linechart(country)

# Stock market index line chart
def create_ind_linechart(country):
      """
   Fucntion creates stock index line chart for choosen country

   Args:
      country (String with name of country)

   Returns:
      GDP line chart for country choosen by clicking at Choropleth map
      If country name not in dataframe function return empty graph objects
   """
      if country not in df_ind['Country'].unique():
         return {}
      else:
         filtered_df = df_ind[df_ind['Country'] == country]
         indeks = str(filtered_df['Ind'].unique()).split('^')[1].split('_')[0]
         fig = go.Figure()
         fig.add_trace(go.Scatter(
            x = filtered_df.index,
            y = filtered_df['Zamkniecie'],
            marker_color = '#FF851B'#Color of line
         ))
         fig.update_layout(title = '{}<br>Index: {}'.format(country, indeks.capitalize()),
         xaxis = dict(
            showgrid = False,
            ticks = 'inside',
            tickwidth = 2,
            tickangle = 45,
            tickfont = dict(
               size = 14
            )
         ),
         paper_bgcolor = '#F2F8FD',
         plot_bgcolor = '#F2F4F6'
         )
         return fig

@app.callback(
   Output('index-line-chart', 'figure'),
   [Input('map-chart', 'clickData')]
)

def update_ind_line_chart(clickData):
   """
   Function serves a callback that passes a clickData value as a variable to index line chart
   """
   if clickData is None:
      return create_ind_linechart(country = 'Poland')
   else:
      country = clickData['points'][0]['text']
      return create_ind_linechart(country)
########################

#Branza tab
def create_fig(indi, sect):
   """
   Function creates Bar chart
   
   Args:
      indi (String that corresponds to choosen indicator)
      sect (String that corresponds to choosen sector of GPW stocks)
   Returns:
      Stocks bar chart for choosen gpw sectors shows values of choosen indicator
   """
   filtered_df = df[df['Ticker'].isin(sector_dict[sect])]
   grouped_df = filtered_df.groupby('Ticker').tail(1)[['Ticker', '{}'.format(indi)]].dropna()#choose the latest data depends of indicator and drop rows with nan value
   grouped_df = grouped_df.sort_values('{}'.format(indi))
   trace_bar = go.Bar(
      x = grouped_df['Ticker'],
      y = grouped_df['{}'.format(indi)],
      hovertext = grouped_df.index,#That show date of used data to plot bar
      showlegend = False,
      marker_color = '#FF851B'#Color of Bars
   )
   trace_line = go.Scatter(
      x = [grouped_df['Ticker'][-1], grouped_df['Ticker'][0]],
      y = [grouped_df['{}'.format(indi)].mean(), grouped_df['{}'.format(indi)].mean()],
      mode = 'lines',
      name = 'Średnia',
      line = dict(color = '#111111', width = 3)
   )
   layout = dict(
      title = "{}".format(indi),
      legend = dict(
         x = 0.4, 
         y = 1.15),
      margin = dict(
         l = 40,
         r = 20
      ),
      xaxis = dict(
         tickangle = 90,
         tickfont = dict(
            size = 10
         )
      ),
      paper_bgcolor = '#F2F8FD',
      plot_bgcolor = '#F2F4F6'
   )

   return {
      'data': [trace_bar, trace_line],
      'layout': layout
   }


@app.callback(
   Output('container-tab1', 'children'),
   [Input('dynamic-indi', 'value'),
   Input('sector', 'value')]
)

#function to support callback
def update_graph(indicators, sect):
   """
   Function serves a callback that update graph objects depends on choosen sector and indicator
   """
   graphs = []
   if len(indicators) < 2:
      width = 12
      xl = 12
   else:
      width = 12
      xl = 6
   for indi in indicators:
      graphs.append(dbc.Col(
         dcc.Graph(
            figure = create_fig(indi, sect),
            style = {
               'margin-top': '0.5rem'
            }
         ), width = width, xl = xl
      )
   )
   return graphs

@app.callback(
   Output('table', 'data'),
   [Input('table-date', 'value')]
)
def update_table_data(date):
   """
   Function serves a callback that passes date to filter dataset 
   """
   df2 = pd.read_csv(r'https://raw.githubusercontent.com/PerczynskiAdam/Value-investing-dash-app/master/Indi_db/truncated_db.csv')
   df2 = df2[df2['Data'] == date].dropna()
   return df2.to_dict('records')

#Stock Tab
#function creating figure in stock tab
def create_fig2(ticker, indi):
   """
   Function creates historical indicator Bar chart for each stock
   
   Args:
      indi (String that corresponds to choosen indicator)
      ticker (String that corrseponds to chooosen gpw stock)
   Returns:
      Display historical bar chart
   """
   filtered_df = df[df['Ticker'] == ticker]
   trace_sca = go.Scatter(
      x = filtered_df.index,
      y = filtered_df['{}'.format(indi)],
      line_color = '#FF851B',
      mode = 'lines'
   )
   layout = dict(
      title = '{} spółki: {}'.format(indi, ticker),
      paper_bgcolor = '#F2F8FD',
      plot_bgcolor = '#F2F4F6',
      xaxis = dict(
         showgrid = False,
         tickangle = 45
      ),
      margin = dict(
         l = 40,
         r = 20
      )
   )
   return {
      'data': [trace_sca],
      'layout': layout
   }

@app.callback(
   Output('container-tab2', 'children'),
   [Input('add-chart-tab2', 'n_clicks')],
   [State('container-tab2', 'children')]
)

def disp_graph_tab2(n_clicks, children):
   """
   Function serves a callback that passes a scope variable to create_map function

   Args:
      n_clicks (It's a number increasing by 1 every time button is clicked)
      children (Dash component populating when all the data is passes)
   Returns
      Returns a graph objects
   """
   new_element = dbc.Col(
      children = [
         dcc.Graph(
            id = {
               'type': 'dynamic-output-tab2',
               'index': n_clicks
            },
            style = {
               'margin-top': '0.5rem'
            }
         ),
         dcc.Dropdown(
            id ={
               'type': 'dynamic-dropdown-tab2',
               'index': n_clicks
            },
            options = [{'label':i, 'value':i} for i in df.columns[1:]],
            value = df.columns[5]
         )
      ], width = 12, xl = 6
   )
   children.append(new_element)
   return children

@app.callback(
   Output({'type': 'dynamic-output-tab2', 'index': MATCH}, 'figure'),
   [Input('dynamic-stock-ticker', 'value'),
   Input({'type':'dynamic-dropdown-tab2', 'index': MATCH}, 'value')]
)

def disp_output(ticker, indi):
   """
   Function serves a callback that passes ticker and indicator to create_fig2 function
   """
   return create_fig2(ticker, indi)

if __name__ == '__main__':
    app.run_server(debug=True)