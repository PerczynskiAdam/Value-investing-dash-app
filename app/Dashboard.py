import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import re

#import data
df = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Indi_db\DB.csv', index_col = 0, encoding = 'utf_8_sig')

df_map = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Macro_db\Eu_iso_gdp.csv', index_col  = 0, encoding = 'utf_8_sig')

df_ind = pd.read_csv(r'C:\Users\AdamPer\Desktop\Python\Dash\Macro_db\trun_index_data.csv', index_col = 0, encoding = 'utf_8_sig')

sector_dict = {'GPW Informatyka': ['11B', 'ABS', 'ACP', 'ALL', 'ART', 'ASE', 'ATD', 'BBT', 'BCM',
       'CDR', 'CIG', 'CMP', 'CMR', 'CTG', 'DAT', 'DTR', 'ELZ', 'GOP',
       'IFI', 'LRK', 'LSI', 'LVC', 'MDG', 'NTT', 'OPM', 'PCG', 'PLW',
       'PRD', 'PSW', 'QNT', 'R22', 'SGN', 'SME', 'SVRS', 'TBL', 'TEN',
       'TLX', 'U2K', 'ULG', 'VVD', 'WAS', 'XTP'],
       'GPW Telekomunikacja': ['ATM', 'CPS', 'MTL', 'MXC', 'NET', 'OPL', 'PLY']}

sectors = list(sector_dict.keys())

scopes = ["world", "europe", "asia", "africa", "north america", "south america"]






#import css stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
   dcc.Tabs(children = [
      dcc.Tab(label = 'Makro', children = [
         html.Div([
            html.H2(children = 'GDP and stock market index of country',
            style = {#style of the H3 element
               'color': '#111111',
               'padding-top': '1.5rem',
               'padding-bottom': '1.5rem',
               'padding-left': '4rem',
               'background-color': '#939598',
               'margin-top': '0.5rem'
               }
            ),
            html.Div([
               html.Div([
                  dcc.Dropdown(
                     id = 'scope',
                     options = [{'label': i.capitalize(), 'value':i} for i in scopes],
                     value = 'europe'
                  ),
                  dcc.Graph(
                     id = 'map-chart',
                     style = {'position': 'relative', 'height': '865px'}#style of dcc.Graph element
                     )
               ], className = 'six columns'),
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
               ], className = 'six columns')
            ], className = 'row',
               style = {
                  'margin-bottom': '0.5rem'
               }
            )#Classname for map and 2 horizontal line charts
         ], className = 'ten columns offset-by-one')#Offset for the biggest container in first tab
      ], selected_style = {
         'color': 'black',
         'box-shadow': '2px 4px #FF851B',
         'border-left': '1px solid #F1F2F2',
         'border-right': '1px solid #F1F2F2',
         'border-top': '1px solid #F1F2F2'
         }
      ),#Style for selected tab (not content of the tab)
      dcc.Tab(label = 'Analiza branży', children = [#Sector tab
         html.Div([
            html.Div([
               html.H2(children = 'Branża:',
                  style = {#Style of H3 element
                  'padding-left': '2.5%'
                  },
                  className = 'two columns'
               ),
               dcc.Dropdown(
                  id = 'sector',
                  options = [{'label': i, 'value': i} for i in sectors],
                  value = sectors[0],
                  className = 'ten columns',
                  style = {
                     'margin-top': '1.2rem',
                     'padding-left': '1%',
                     'display': 'inline-block',
                     'width': '45%'
                  }
               )
            ], className = 'row', style = {
               'margin-top': '0.5rem',
               'background-color':'#939598'
               }
            ),
            html.Div([
               dcc.Dropdown(
                  id = 'dynamic-indi',
                  options = [{'label': i, 'value':i} for i in df.columns[1:]],
                  value = ['Cena / Wartość księgowa', 'Cena / Zysk', 'ROE', 'Marża zysku operacyjnego', 'Zadłużenie ogólne'],
                  multi = True
               )
            ], style = {
               'margin-top': '0.5rem',
               'display': 'inline-block'
               }
            ),
            html.Div(
               id = 'container-tab1', 
               children = []
            )
         ], className = 'ten columns offset-by-one')#Offset for the biggest container in Sector tab
      ], selected_style = {
         'color': 'black',
         'box-shadow': '2px 4px #FF851B',
         'border-left': '1px solid #F1F2F2',
         'border-right': '1px solid #F1F2F2',
         'border-top': '1px solid #F1F2F2'
         }
      ),#Style for selected tab (not content of the tab)
      dcc.Tab(label = 'Analiza spółki', children = [#Stock tab
         html.Div([
            html.Div([
               html.H2(
                  children = 'Spółka:', 
                  className = 'two columns',
                  style = {
                     'padding-left': '2.5%'
                  }
               ),
               dcc.Dropdown(
                  id = 'dynamic-stock-ticker',
                  options = [{'label': i, 'value':i} for i in df['Ticker'].unique()],
                  value = df['Ticker'].unique()[0],
                  style = {
                     'margin-top': '1.2rem',
                     'padding-left': '1%',
                     'display': 'inline-block',
                     'width': '30%'
                  },
                  className = 'ten columns'
               )
            ], className = 'row', style = {#Style of whole container element with H3 and Dropdown inside 
               'margin-top': '0.5rem',
               'background-color': '#939598'
               }
            ),
            html.Div([
               html.Button(
                  children = 'Dodaj wykres', 
                  id = 'add-chart-tab2', 
                  n_clicks = 0,
                  style = {#Style of the Button element
                     'margin-top': '0.5rem'
                  },
                  className = 'button-primary'
               )
            ]),
            html.Div(
               id = 'container-tab2',
               children = [],
               style = {
                  'margin-top': '0.5rem'
               }
            )
         ], className = 'ten columns offset-by-one',#Offset for the biggest container in Stock tab
         style = {
            'margin-bottom': '0.5rem'
         }) 
      ], selected_style = {
         'color': 'black',
         'box-shadow': '2px 4px #FF851B',
         'border-left': '1px solid #F1F2F2',
         'border-right': '1px solid #F1F2F2',
         'border-top': '1px solid #F1F2F2'
         }
      )#Style for selected tab (not content of the tab)
   ], style = {'borderBottom': '1px solid #d6d6d6', 'fontWeight': 'bold'})#Style of all Tabs
      # content_style = {'background-color': '#AAAAAA'})#Style of all Tabs content
])
def create_map(scope):# function creating map
   fig = go.Figure()
   fig.add_trace(go.Choropleth(
      locations = df_map['Code'],
      z = df_map[df_map.columns[-2]].astype(float),
      text = df_map.index,
      colorbar_title = 'GDP<br>Billions US$'
   ))
   fig.update_layout(
      geo = dict(
         scope = scope,
         projection_type = 'natural earth',
         bgcolor = '#939598'
      ),
      title = dict(text = '{} GDP'.format(scope.capitalize())),
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
   return create_map(scope)

#function creating line chart under map in Makro tab
def create_pkb_linechart(country):
   fig = go.Figure()
   fig.add_trace(go.Scatter(
      x = df_map.columns,
      y = list(df_map[df_map.index == country].iloc[0])[:-1],
      marker_color = '#FF851B'#Color of line
   ))
   fig.update_layout(title = 'GDP {}'.format(country),
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
   [Input('map-chart', 'hoverData')]
)

def update_pkb_line_chart(hoverData):
   if hoverData is None:
      return create_pkb_linechart(country = 'Poland')
   else:
      country = hoverData['points'][0]['text']
      return create_pkb_linechart(country)

def create_ind_linechart(country):
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
   [Input('map-chart', 'hoverData')]
)

def update_ind_line_chart(hoverData):
   if hoverData is None:
      return create_ind_linechart(country = 'Poland')
   else:
      country = hoverData['points'][0]['text']
      return create_ind_linechart(country)


#Branza tab
#function creating fig in branza tab
def create_fig(indi, sect):
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
         l = 25,
         r = 25
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
   Output('container-tab1', 'children'),#where and what to change
   [Input('dynamic-indi', 'value'),
   Input('sector', 'value')]#where and how its starting
)

#function to support callback
def update_graph(indicators, sect):
   graphs = []
   if len(indicators) < 2:
      class_choice = 'twelve columns'
   else:
      class_choice = 'six columns'

   for indi in indicators:
      graphs.append(html.Div([
         dcc.Graph(
         figure = create_fig(indi, sect),
         style ={
            'margin-bottom': '0.5rem'
         }
      )], className = class_choice)
      )
   return graphs



#Stock Tab
#function creating figure in stock tab
def create_fig2(ticker, indi):
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
         l = 25,
         r = 25
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
   new_element = html.Div(
      children = [
         dcc.Graph(
            id = {
               'type': 'dynamic-output-tab2',
               'index': n_clicks
            }
         ),
         dcc.Dropdown(
            id ={
               'type': 'dynamic-dropdown-tab2',
               'index': n_clicks
            },
            options = [{'label':i, 'value':i} for i in df.columns[1:]],
            value = df.columns[1]
         )
      ], className = 'six columns'#className of children element in Html.Div
   )
   children.append(new_element)
   return children

@app.callback(
   Output({'type': 'dynamic-output-tab2', 'index': MATCH}, 'figure'),
   [Input('dynamic-stock-ticker', 'value'),
   Input({'type':'dynamic-dropdown-tab2', 'index': MATCH}, 'value')]
)

def disp_output(ticker, indi):
   return create_fig2(ticker, indi)

if __name__ == '__main__':
    app.run_server(debug=True)