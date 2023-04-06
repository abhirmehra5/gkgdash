import pandas as pd
from dash import  dcc, Input, Output, html
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np

newdata24=pd.read_csv('gkgfinal_24.csv')

newdata24['Organizations']=newdata24['Organizations'].str.replace('[','')
newdata24['Organizations']=newdata24['Organizations'].str.replace(']','')
newdata24['Organizations']=newdata24['Organizations'].str.replace("'",'')
newdata24['Organizations']=newdata24['Organizations'].str.replace('"','')

options24 = (list(newdata24['Organizations'].str.split(',', expand=True).stack()))
options24 = [x.strip(' ') for x in options24]

orgs24 = []

for i in options24:
    if (i not in orgs24):
        orgs24.append(i)
#%%
df_theme = pd.read_pickle('theme_sdg_mapping.pk')
themes=list(df_theme.keys())
actualthemes24=[]

for i in range(len(newdata24['Themes'])):
    rowthemes=newdata24['Themes'].str.split(';')[i]
    neededthemes=[]
    if type(rowthemes) is float:
        pass
    else:
        for i in range(len(themes)):
            theme=themes[i]
            if theme in rowthemes:
                neededthemes.append(theme)
            else:
                neededthemes.append(np.nan)

    cleanedList24 = [x for x in neededthemes if str(x) != 'nan']
    actualthemes24.append(cleanedList24)
#%%
newdata24['ActualThemes']=actualthemes24
newdata24['ActualThemes'] = [','.join(map(str, l)) for l in newdata24['ActualThemes']]
newdata24['ActualThemes'] = newdata24['ActualThemes'].replace(r'^\s*$', np.nan, regex=True)
newdata24=newdata24[newdata24['ActualThemes'].notna()]
#%%
newdata24['dates'] = pd.to_datetime(newdata24['DATE'], format='%Y%m%d%H%M%S')
data_15=newdata24[newdata24['dates'].isin([newdata24['dates'][0]])]
#%%
# master=pd.read_csv('/Users/AbhirMehra/PycharmProjects/stockmetadata_Abhir/mastertable.csv')
# master=master[['Ticker','Company_Name']]
# master=master[master['Company_Name'].isin([i.upper() for i in options24])]
# prices=pd.read_csv('prices.csv')
# prices=prices.merge(master,left_on="Ticker",right_on="Ticker",how="right")
#%%
layout=dbc.Container([
    html.Div([
        dcc.Dropdown(id='dropdown',options = orgs24,placeholder="Select a Company")]),
    html.Div([
        dcc.Graph(id='spyder24', style={'display': 'inline-block'}),
        dcc.Graph(id='spyder',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='scatter24', style={'display': 'inline-block','height':'1000px'}),
        dcc.Graph(id='scatter',style={'display': 'inline-block','height':'1000px'})]),
    html.Div([
        dcc.Graph(id='groupedscatter24', style={'display': 'inline-block','height':'1000px'}),
        dcc.Graph(id='groupedscatter',style={'display': 'inline-block','height':'1000px'})]),
    html.Div([
        dcc.Graph(id='freqhist24', style={'display': 'inline-block'}),
        dcc.Graph(id='freqhist',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='avghist24', style={'display': 'inline-block'}),
        dcc.Graph(id='avghist',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='heatmap24', style={'display': 'inline-block'}),
        dcc.Graph(id='heatmap',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='table24', style={'display': 'inline-block'}),
        dcc.Graph(id='table',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='tableurl24', style={'display': 'inline-block'}),
        dcc.Graph(id='tableurl',style={'display': 'inline-block'})]),
    # html.Div([
    #     dcc.Graph(id='pricegraph24', style={'display': 'inline-block'}),
    #     dcc.Graph(id='pricegraph',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='themegraph24', style={'display': 'inline-block'}),
        dcc.Graph(id='themegraph',style={'display': 'inline-block'})]),
    html.Div([
        dcc.Graph(id='stackedbar24', style={'display': 'inline-block'}),
        dcc.Graph(id='stackedbar',style={'display': 'inline-block'})])])
    # html.Div([
    #     html.Iframe(id='wordcloud24', srcDoc=None,style={'width':'45%','height':'500px','display': 'inline-block'}),
    #     html.Iframe(id='wordcloud',srcDoc=None,style={'width':'45%','height':'500px','display': 'inline-block'})]
#%%
app = dash.Dash(__name__)
server = app.server
app.layout=layout

@app.callback(Output('spyder', 'figure'),
              [Input('dropdown', 'value')])
def update_spyder(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes','V2Tone']]
    fig=px.line_polar(org,r='V2Tone',theta='ActualThemes',line_close=True,color_discrete_sequence=px.colors.sequential.Plasma_r)
    return fig

@app.callback(Output('spyder24', 'figure'),
              [Input('dropdown', 'value')])
def update_spyder24(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes','V2Tone']]
    fig=px.line_polar(org,r='V2Tone',theta='ActualThemes',line_close=True,color_discrete_sequence=px.colors.sequential.Plasma_r)
    return fig


@app.callback(Output('scatter', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    fig = px.scatter(x=output.V2Tone, y=output.Themes)
    return fig

@app.callback(Output('scatter24', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter24(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    fig = px.scatter(x=output.V2Tone, y=output.Themes)
    return fig

@app.callback(Output('groupedscatter', 'figure'),
              [Input('dropdown', 'value')])
def update_spyder(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes','V2Tone']]
    fig = px.scatter(x=org.V2Tone, y=org.ActualThemes)
    return fig

@app.callback(Output('groupedscatter24', 'figure'),
              [Input('dropdown', 'value')])
def update_spyder24(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes','V2Tone']]
    fig = px.scatter(x=org.V2Tone, y=org.ActualThemes)
    return fig

@app.callback(Output('freqhist', 'figure'),
              [Input('dropdown', 'value')])
def update_freqhist(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output=output['Themes']
    fig = px.histogram(output,x='Themes').update_xaxes(categoryorder="total descending")
    return fig

@app.callback(Output('freqhist24', 'figure'),
              [Input('dropdown', 'value')])
def update_freqhist24(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output=output['Themes']
    fig = px.histogram(output,x='Themes').update_xaxes(categoryorder="total descending")
    return fig

@app.callback(Output('avghist', 'figure'),
              [Input('dropdown', 'value')])
def update_avghist(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output=output.groupby('Themes', as_index=False).mean()
    output.sort_values(by=['V2Tone'],inplace=True)
    fig = px.bar(output, x='Themes', y='V2Tone')
    return fig

@app.callback(Output('avghist24', 'figure'),
              [Input('dropdown', 'value')])
def update_avghist24(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output=output.groupby('Themes', as_index=False).mean()
    output.sort_values(by=['V2Tone'],inplace=True)
    fig = px.bar(output, x='Themes', y='V2Tone')
    return fig

@app.callback(Output('heatmap', 'figure'),
              [Input('dropdown', 'value')])
def update_heatmap(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output['new']=output['V2Tone'].astype(str)+output['Themes']
    c1=output[output['V2Tone'].between(-100, -5, inclusive=True)].drop('Themes',axis=1)
    c2=output[output['V2Tone'].between(-4.99, -4, inclusive=True)].drop('Themes',axis=1)
    c3=output[output['V2Tone'].between(-3.99, -3, inclusive=True)].drop('Themes',axis=1)
    c4=output[output['V2Tone'].between(-2.99, -2, inclusive=True)].drop('Themes',axis=1)
    c5=output[output['V2Tone'].between(-1.99, -1, inclusive=True)].drop('Themes',axis=1)
    c6=output[output['V2Tone'].between(-0.99, 0, inclusive=True)].drop('Themes',axis=1)
    c7=output[output['V2Tone'].between(0.01, 1, inclusive=True)].drop('Themes',axis=1)
    c8=output[output['V2Tone'].between(1.01, 2, inclusive=True)].drop('Themes',axis=1)
    c9=output[output['V2Tone'].between(2.01, 3, inclusive=True)].drop('Themes',axis=1)
    c10=output[output['V2Tone'].between(3.01, 4, inclusive=True)].drop('Themes',axis=1)
    c11=output[output['V2Tone'].between(4.01, 5, inclusive=True)].drop('Themes',axis=1)
    c12=output[output['V2Tone'].between(5, 100, inclusive=True)].drop('Themes',axis=1)
    c1.rename(columns={"V2Tone": 'Lesser than -5'},inplace=True)
    c2.rename(columns={"V2Tone": '-5 to -4'},inplace=True)
    c3.rename(columns={"V2Tone": '-4 to -3'},inplace=True)
    c4.rename(columns={"V2Tone": '-3 to -2'},inplace=True)
    c5.rename(columns={"V2Tone": '-2 to -1'},inplace=True)
    c6.rename(columns={"V2Tone": '-1 to 0'},inplace=True)
    c7.rename(columns={"V2Tone": '0.01 to 1'},inplace=True)
    c8.rename(columns={"V2Tone": '1.01 to 2'},inplace=True)
    c9.rename(columns={"V2Tone": '2.01 to 3'},inplace=True)
    c10.rename(columns={"V2Tone": '3.01 to 4'},inplace=True)
    c11.rename(columns={"V2Tone": '4.01 to 5'},inplace=True)
    c12.rename(columns={"V2Tone": 'Greater than 5'},inplace=True)
    output=output.merge(c1, on='new',how='left')
    output=output.merge(c2, on='new',how='left')
    output=output.merge(c3, on='new',how='left')
    output=output.merge(c4, on='new',how='left')
    output=output.merge(c5, on='new',how='left')
    output=output.merge(c6, on='new',how='left')
    output=output.merge(c7, on='new',how='left')
    output=output.merge(c8, on='new',how='left')
    output=output.merge(c9, on='new',how='left')
    output=output.merge(c10, on='new',how='left')
    output=output.merge(c11, on='new',how='left')
    output=output.merge(c12, on='new',how='left')
    output=output.drop(['V2Tone','new'],axis=1).set_index('Themes')
    fig = px.imshow(output,text_auto=True,aspect='auto',color_continuous_scale=["red", "green"])
    return fig

@app.callback(Output('heatmap24', 'figure'),
              [Input('dropdown', 'value')])
def update_heatmap(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output['new']=output['V2Tone'].astype(str)+output['Themes']
    c1=output[output['V2Tone'].between(-100, -5, inclusive=True)].drop('Themes',axis=1)
    c2=output[output['V2Tone'].between(-4.99, -4, inclusive=True)].drop('Themes',axis=1)
    c3=output[output['V2Tone'].between(-3.99, -3, inclusive=True)].drop('Themes',axis=1)
    c4=output[output['V2Tone'].between(-2.99, -2, inclusive=True)].drop('Themes',axis=1)
    c5=output[output['V2Tone'].between(-1.99, -1, inclusive=True)].drop('Themes',axis=1)
    c6=output[output['V2Tone'].between(-0.99, 0, inclusive=True)].drop('Themes',axis=1)
    c7=output[output['V2Tone'].between(0.01, 1, inclusive=True)].drop('Themes',axis=1)
    c8=output[output['V2Tone'].between(1.01, 2, inclusive=True)].drop('Themes',axis=1)
    c9=output[output['V2Tone'].between(2.01, 3, inclusive=True)].drop('Themes',axis=1)
    c10=output[output['V2Tone'].between(3.01, 4, inclusive=True)].drop('Themes',axis=1)
    c11=output[output['V2Tone'].between(4.01, 5, inclusive=True)].drop('Themes',axis=1)
    c12=output[output['V2Tone'].between(5, 100, inclusive=True)].drop('Themes',axis=1)
    c1.rename(columns={"V2Tone": 'Lesser than -5'},inplace=True)
    c2.rename(columns={"V2Tone": '-5 to -4'},inplace=True)
    c3.rename(columns={"V2Tone": '-4 to -3'},inplace=True)
    c4.rename(columns={"V2Tone": '-3 to -2'},inplace=True)
    c5.rename(columns={"V2Tone": '-2 to -1'},inplace=True)
    c6.rename(columns={"V2Tone": '-1 to 0'},inplace=True)
    c7.rename(columns={"V2Tone": '0.01 to 1'},inplace=True)
    c8.rename(columns={"V2Tone": '1.01 to 2'},inplace=True)
    c9.rename(columns={"V2Tone": '2.01 to 3'},inplace=True)
    c10.rename(columns={"V2Tone": '3.01 to 4'},inplace=True)
    c11.rename(columns={"V2Tone": '4.01 to 5'},inplace=True)
    c12.rename(columns={"V2Tone": 'Greater than 5'},inplace=True)
    output=output.merge(c1, on='new',how='left')
    output=output.merge(c2, on='new',how='left')
    output=output.merge(c3, on='new',how='left')
    output=output.merge(c4, on='new',how='left')
    output=output.merge(c5, on='new',how='left')
    output=output.merge(c6, on='new',how='left')
    output=output.merge(c7, on='new',how='left')
    output=output.merge(c8, on='new',how='left')
    output=output.merge(c9, on='new',how='left')
    output=output.merge(c10, on='new',how='left')
    output=output.merge(c11, on='new',how='left')
    output=output.merge(c12, on='new',how='left')
    output=output.drop(['V2Tone','new'],axis=1).set_index('Themes')
    fig = px.imshow(output,text_auto=True,aspect='auto',color_continuous_scale=["red", "green"])
    return fig

@app.callback(Output('table', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone','DocumentIdentifier']]
    org=org.sort_values(by=['V2Tone'])
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(org.columns)),
    cells=dict(values=[org.ActualThemes, org.V2Tone, org.DocumentIdentifier],height=60))])
    return fig

@app.callback(Output('table24', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone','DocumentIdentifier']]
    org=org.sort_values(by=['V2Tone'])
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(org.columns)),
    cells=dict(values=[org.ActualThemes, org.V2Tone, org.DocumentIdentifier],height=60))])
    return fig

@app.callback(Output('tableurl', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org=data_15[data_15['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone','DocumentIdentifier']]
    org=org.sort_values(by=['V2Tone'])
    org=org['DocumentIdentifier']
    org=org.to_frame()
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(org.columns)),
    cells=dict(values=[org.DocumentIdentifier],height=60))])
    return fig

@app.callback(Output('tableurl24', 'figure'),
              [Input('dropdown', 'value')])
def update_scatter(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone','DocumentIdentifier']]
    org=org.sort_values(by=['V2Tone'])
    org=org['DocumentIdentifier']
    org=org.to_frame()
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(org.columns)),
    cells=dict(values=[org.DocumentIdentifier],height=60))])
    return fig

# @app.callback(Output('pricegraph', 'figure'),
#               [Input('dropdown', 'value')])
# def update_stsfig(input_value):
#     input_value=input_value.upper()
#     data=prices[prices['Company_Name'].isin([input_value])].set_index('date')['adjusted_close']
#     fig = px.line(data)
#     return fig
#
# @app.callback(Output('pricegraph24', 'figure'),
#               [Input('dropdown', 'value')])
# def update_stsfig(input_value):
#     input_value=input_value.upper()
#     data=prices[prices['Company_Name'].isin([input_value])].set_index('date')['adjusted_close']
#     fig = px.line(data)
#     return fig

@app.callback(Output('themegraph', 'figure'),
              [Input('dropdown', 'value')])
def update_stsfig(input_value):
    org = data_15[data_15['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone', 'dates']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org['V2Tone']
    output['Date'] = org['dates']
    output['Themes'] = new.values
    fig = px.line(output, x="Date", y="V2Tone", color='Themes')
    return fig

@app.callback(Output('themegraph24', 'figure'),
              [Input('dropdown', 'value')])
def update_stsfig(input_value):
    org = newdata24[newdata24['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone', 'dates']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org['V2Tone']
    output['Date'] = org['dates']
    output['Themes'] = new.values
    output = output.sort_values('Date')
    fig = px.line(output, x="Date", y="V2Tone", color='Themes',markers=True)
    return fig

@app.callback(Output('stackedbar', 'figure'),
              [Input('dropdown', 'value')])
def update_stackedbar(input_value):
    curr=newdata24['dates'][0]
    prev=curr-pd.Timedelta('0 days 00:15:00')
    org = newdata24[newdata24['dates'].isin([curr, prev])]
    org = org[org['Organizations'].str.contains(input_value)]
    org = org[['ActualThemes', 'V2Tone', 'dates']]
    new = org['ActualThemes'].str.split(',', expand=True).stack()
    vals = new.index.get_level_values(level=0)
    org = org.drop(columns=['ActualThemes']).loc[vals]
    output = pd.DataFrame()
    output['V2Tone'] = org['V2Tone']
    output['dates'] = org['dates']
    output['Themes'] = new.values
    d1 = output[output['dates'].isin([curr])].groupby('Themes', as_index=False).mean()
    d1['dates'] =  curr
    d2 = output[output['dates'].isin([prev])].groupby('Themes', as_index=False).mean()
    d2['dates'] = prev
    new = pd.concat([d1, d2])
    fig = px.bar(new, x="dates", y="V2Tone", color='Themes',
              hover_data=['Themes'], barmode='stack')
    return fig

@app.callback(Output('stackedbar24', 'figure'),
              [Input('dropdown', 'value')])
def update_stackedbar(input_value):
    org=newdata24[newdata24['Organizations'].str.contains(input_value)]
    org=org[['ActualThemes','V2Tone']]
    new=org['ActualThemes'].str.split(',',expand=True).stack()
    vals=new.index.get_level_values(level=0)
    org=org.drop(columns=['ActualThemes']).loc[vals]
    output=pd.DataFrame()
    output['V2Tone']=org
    output['Themes']=new.values
    output=output.groupby('Themes', as_index=False).mean()
    output.sort_values(by=['V2Tone'],inplace=True)
    output['col'] = 'Themes'
    fig = px.bar(output, x="col", y="V2Tone", color='Themes',
            hover_data=['Themes'], barmode = 'stack')
    return fig

# @app.callback(Output('wordcloud', 'srcDoc'),
#               [Input('dropdown', 'value')])
# def update_wordcloud(input_value):
#     org=data_15[data_15['Organizations'].str.contains(input_value)]
#     org=org[['ActualThemes','V2Tone']]
#     new=org['ActualThemes'].str.split(',',expand=True).stack()
#     text=""
#     for i in new.values:
#         text+=i + ' '
#     wordcloud = WordCloud(width = 800, height = 800,
#                 background_color ='white',
#                 min_font_size = 10).generate(text)
#     fig,ax=plt.subplots()
#     ax.imshow(wordcloud)
#     ax.axis("off")
#     wc = mpld3.fig_to_html(fig)
#     return wc
#
# @app.callback(Output('wordcloud24', 'srcDoc'),
#               [Input('dropdown', 'value')])
# def update_wordcloud(input_value):
#     org=newdata24[newdata24['Organizations'].str.contains(input_value)]
#     org=org[['ActualThemes','V2Tone']]
#     new=org['ActualThemes'].str.split(',',expand=True).stack()
#     text=""
#     for i in new.values:
#         text+=i + ' '
#     wordcloud = WordCloud(width = 800, height = 800,
#                 background_color ='white',
#                 min_font_size = 10).generate(text)
#     fig,ax=plt.subplots()
#     ax.imshow(wordcloud)
#     ax.axis("off")
#     wc = mpld3.fig_to_html(fig)
#     return wc



if __name__ == '__main__':
    app.run_server()