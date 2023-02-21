import numpy as np
import pandas as pd
from dash import  dcc, Input, Output, html
import dash
import plotly.express as px
import plotly.figure_factory as ff

data=pd.read_csv('gkgdata.csv')

options=(list(data['Organizations'].str.split(',',expand=True).stack()))
options = [x.strip(' ') for x in options]

orgs = []

for i in options:
    if(i not in orgs):
        orgs.append(i)

layout = html.Div([
    dcc.Dropdown(id='dropdown', options=orgs, placeholder="Select a Company"),
    dcc.Graph(id='spyder'),
    dcc.Graph(id='scatter'),
    dcc.Graph(id='freqhist'),
    dcc.Graph(id='avghist'),
    dcc.Graph(id='heatmap'),
    # dcc.Graph(id='table')
])
app = dash.Dash(__name__)
server = app.server
app.layout = layout


@app.callback(Output('spyder', 'figure'),
              [Input('dropdown', 'value')])
def update_spyder(input_value):
    org = data[data['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone']]
    fig = px.line_polar(org, r='V2Tone', theta='ActualThemes', line_close=True,
                        color_discrete_sequence=px.colors.sequential.Plasma_r)
    return fig


@app.callback(Output('scatter', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org = data[data['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org
    output['Themes'] = new.values
    fig = px.scatter(x=output.V2Tone, y=output.Themes)
    return fig


@app.callback(Output('freqhist', 'figure'),
              [Input('dropdown', 'value')])
def update_freqhist(input_value):
    org = data[data['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org
    output['Themes'] = new.values
    output = output['Themes']
    fig = px.histogram(output, x='Themes')
    return fig


@app.callback(Output('avghist', 'figure'),
              [Input('dropdown', 'value')])
def update_avghist(input_value):
    org = data[data['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org
    output['Themes'] = new.values
    output = output.groupby('Themes', as_index=False).mean()
    fig = px.bar(output, x='Themes', y='V2Tone')
    return fig


@app.callback(Output('heatmap', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org = data[data['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org
    output['Themes'] = new.values
    output = output.set_index('Themes')
    fig = px.imshow(output)
    return fig


# @app.callback(Output('table', 'figure'),
#               [Input('dropdown', 'value')])
# def update_scatter(input_value):
#     org = data[data['Organizations'].str.contains(input_value)]
#     org = org[['ActualThemes', 'V2Tone', 'DocumentIdentifier']]
#     fig = ff.create_table(org)
#     return fig


if __name__ == '__main__':
    app.run_server()