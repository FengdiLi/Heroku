# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
import pandas as pd
import numpy as np
import os
import copy
from datetime import datetime

app = dash.Dash(__name__)
server = app.server

# datasets
map_data = pd.read_csv('Dataset.csv')

map_data['Date'] = map_data['Date'].apply(lambda x: datetime.strptime(x, '%d-%b-%y')).dt.date

# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='MAP',
    geo = dict(
            scope='asia',
            center = dict(
                    lat=35,
                    lon=43
                    ),
            projection=dict( type='mercator' ),
            showland = True,
            showocean = True,
            landcolor = "navajowhite",
            oceancolor = "lightgrey",
            showcountries = True,
#            subunitcolor = "rgb(217, 217, 217)",
#            countrycolor = "rgb(217, 217, 217)",
#            countrywidth = 0.5,
#            subunitwidth = 0.5
        ),
)

# Controls (dropdowns)
group = ['All']
group = group + ['Low', 'Medium', 'High', 'Very High']
group_class = [{'label': str(item),
                      'value': str(item)}
                     for item in group]


# Creating layouts for datatable
layout_right = copy.deepcopy(layout)
layout_right['height'] = 300
layout_right['margin-top'] = '20'
layout_right['font-size'] = '12'
layout_right['backgroundcolor'] = 'whitesmoke'

mp_max = map_data['Number of Families'].max()
mp_min = map_data['Number of Families'].min()

# Components style
def color_scale(md, selected_row_indices=[]):
    color = []
    max_score = mp_max 
    min_score = mp_min
    for row in md['Number of Families']:
        scale = (row - mp_min)/(mp_max - mp_min)
        if scale <= 0.01:
            color.append("#191970")
        elif scale <= 0.02:
            color.append("#191970")
        elif scale <= 0.04:
            color.append("#4169E1")
        elif scale <= 0.06:
            color.append("#4169E1")
        elif scale <= 0.09:
            color.append("#6495ED")
        elif scale <= 0.12:
            color.append("#6495ED")
        elif scale <= 0.16:
            color.append("#D8BFD8")
        elif scale <= 0.22:
            color.append("#DDA0DD")
        elif scale <= 0.29:
            color.append("#EE82EE")
        elif scale <= 0.38:
            color.append("#EE82EE")
        elif scale <= 0.46:
            color.append("#DA70D6")
        elif scale <= 0.54:
            color.append("#DA70D6")
        elif scale <= 0.73:
            color.append("#C71585")
        elif scale <= 0.82:
            color.append("#C71585")
        elif scale <= 0.90:
            color.append("#8B008B")
        else:
            color.append("#8B008B")
    for i in selected_row_indices:
        color[i] = '#1500FA'
    return color

def gen_map(mp_data):

    mp_data['Text'] = 'Governorate: ' + mp_data['Governorate'] + '</br> Number of Families: '+ mp_data['Number of Families'].map(str) + '</br> Date: ' + mp_data['Date']
    return {
        "data": [
                {
                    "type": "scattergeo",
                    "lat": list(mp_data['Latitude']),
                    "lon": list(mp_data['Longitude']),
                    "text": list(mp_data['Text']),
                    "mode": "markers",
                    "name": list(mp_data['Location Name']),
                    "marker": {
                        "size": 6,
                        "opacity": 1.0,
                        "color": color_scale(mp_data)
                    }
                }
            ],
        "layout": layout
    }


# Layout
app.layout = html.Div([
    # Title - Row
    html.Div(
        [
            html.H1(
                'Forced Migration',
                style={'font-family': 'Helvetica',
                       "margin-top": "25",
                       "margin-bottom": "0"},
                className='eight columns',
            ),
            html.Img(
                src="http://www.freelogovectors.net/wp-content/uploads/2018/03/Georgetown_University_SealLogo.png",
                className='two columns',
                style={
                    'height': '5%',
                    'width': '5%',
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 10,
                    'padding-right': 0
                },
            ),
            html.P(
                'Dash_demo.',
                style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%"},
                className='eight columns',
            ),
        ],
        className='row'
    ),

    # Selectors
    html.Div(
        [
            html.Div(
                [
                    html.P('Choose Regions:'),
                    dcc.Checklist(
                            id = 'Governorate',
                            options=[
                                {'label': 'Anbar', 'value': 'Anbar'},
                                {'label': 'Baghdad', 'value': 'Baghdad'},
                                {'label': 'Diyala', 'value': 'Diyala'},
                                {'label': 'Kirkuk', 'value': 'Kirkuk'},
                                {'label': 'Ninewa', 'value': 'Ninewa'},
                                {'label': 'Salah al-Din', 'value': 'Salah al-Din'}                                
                            ],
                            values=['Salah al-Din', 'Ninewa', 'Diyala', 'Kirkuk', 'Anbar', 'Baghdad'],
                            labelStyle={'display': 'inline-block'}
                    ),
                ],
                className='six columns',
                style={'margin-top': '10',
                       'backgroundColor':'lightgrey'}
            ),
            html.Div(
                [
                    html.P('Population:'),
                    dcc.Dropdown(
                        id='Pop',
                        options= group_class,
                        multi=False,
                        value='All'
                    )
                ],
                className='two columns',
                style={'margin-top': '10',
                       'backgroundColor':'lightgrey'}
            ),
            html.Div(
                [
                    html.P('Economic Level:'),
                    dcc.Dropdown(
                        id='Econ',
                        options= group_class,
                        multi=False,
                        value='All'
                    )
                ],
                className='two columns',
                style={'margin-top': '10',
                       'backgroundColor':'lightgrey'}
            ),
            html.Div(
                [
                    html.P('Social Level:'),
                    dcc.Dropdown(
                        id='Soc',
                        options= group_class,
                        multi=False,
                        value='All'
                    )
                ],
                className='two columns',
                style={'margin-top': '10',
                       'backgroundColor':'lightgrey'}
            )
        ],
        className='row'
    ),

    # Map + table + Histogram
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='map-graph',
                              animate=True, 
                              style={'margin-top': '20'})
                ], className = "six columns"
            ),
            html.Div(
                [
                    dt.DataTable(
                        rows=map_data.to_dict('records'),
                        columns=map_data.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        id='datatable'),
                ],
                style=layout_right,
                className="six columns"
            ),
            html.Div(
                [
                    dcc.Graph(id="histogram")
                ],className="twelve columns")
        ], className="row"
    )
], className='ten columns offset-by-one')

# Callbacks and functions
@app.callback(
    Output('datatable', 'rows'),
    [dash.dependencies.Input('Governorate', 'values'),
    dash.dependencies.Input('Pop', 'value'),
    dash.dependencies.Input('Econ', 'value'),
    dash.dependencies.Input('Soc', 'value')])
def update_selected_row_indices(governorate, pop, econ, soc):
    map_aux = map_data.copy()

    # Governorate filter
    map_aux = map_aux[map_aux['Governorate'].isin(governorate)]

    # DOE filter
    if pop == 'Low':
        map_aux = map_aux[map_aux['Population'] <= 0.5]
    if pop == 'Medium':
        map_aux = map_aux[(map_aux['Population'] > 0.5) & \
                          (map_aux['Population'] <= 1.0)]
    if pop == 'High':
        map_aux = map_aux[(map_aux['Population'] > 1.0) & \
                          (map_aux['Population'] <= 1.5)]
    if pop == 'Very High':
        map_aux = map_aux[map_aux['Population'] > 1.5]

    # Econ filter
    if econ == 'Low':
        map_aux = map_aux[map_aux['Economic'] <= 0.1]
    if econ == 'Medium':
        map_aux = map_aux[(map_aux['Economic'] > 0.1) & \
                          (map_aux['Economic'] <= 0.25)]
    if econ  == 'High':
        map_aux = map_aux[(map_aux['Economic'] > 0.25) & \
                          (map_aux['Economic'] <= 0.4)]
    if econ  == 'Very High':
        map_aux = map_aux[map_aux['Economic'] > 0.4]

    # Social filter
    if soc == 'Low':
        map_aux = map_aux[map_aux['Social'] <= 15]
    if soc == 'Medium':
        map_aux = map_aux[(map_aux['Social'] > 15) & \
                          (map_aux['Social'] <= 27.5)]
    if soc  == 'High':
        map_aux = map_aux[(map_aux['Social'] > 27.5) & \
                          (map_aux['Social'] <= 35.0)]
    if soc  == 'Very High':
        map_aux = map_aux[map_aux['Social'] > 35.0]

    rows = map_aux.to_dict('records')
    return rows

@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('histogram', 'selectedData')],
    [State('datatable', 'selected_row_indices')])
def update_selected_row_indices(selectedData, selected_row_indices):
    if selectedData:
        selected_row_indices = []
        for point in selectedData['points']:
            selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('histogram', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        margin=Margin(l=50, r=10, t=0, b=100),
        showlegend=False,
        height = 250,
        dragmode="select",
        xaxis=dict(
            showgrid=False,
            nticks=50,
            fixedrange=False
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            fixedrange=False,
            rangemode='nonnegative',
            zeroline='hidden'
        )
    )
        
    dff2 = dff.groupby(['Date'], as_index = False).mean()
    data = Data([
         go.Bar(
             x=dff2['Date'],
             y=dff2['Number of Families'],
             marker = {'color': color_scale(dff2, selected_row_indices)},
             hoverinfo=dff2['Date']
         )
     ])

    return go.Figure(data=data, layout=layout)


@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)


if __name__ == '__main__':
    app.run_server(debug=True)