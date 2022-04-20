import plotly.graph_objects as go
import pandas as pd

import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State, ClientsideFunction

path = './'

data = pd.read_csv(path + 'data/reduced_data.csv')
data = data[data.date.str[:4].astype(int) >= 2013]
year = data.date.str[:4].astype(int)

grouped = data[data.date >  '2013-01'].groupby(['regions','date'])['date'].count()
regions = data.regions.unique()
fig = go.Figure()

fig.add_trace(go.Scatter(x = grouped.loc[regions[0]].index,
                             y=grouped.loc[regions[0]].values,
                             name = regions[0],
                             mode = 'lines'
                            ))
fig.add_trace(go.Scatter(x = grouped.loc[regions[1]].index,
                             y=grouped.loc[regions[1]].values,
                             name = regions[1],
                             mode = 'lines'
                            ))

for region in regions[2:]:
    fig.add_trace(go.Scatter(x = grouped.loc[region].index,
                             y=grouped.loc[region].values,
                             name = region,
                             visible='legendonly',
                             mode = 'lines'
                            ))

# fig.update_traces(opacity=0.5)
fig.update_layout(hovermode="x", height = 500, template = "plotly_dark", font=dict(family="Playfair Display",), title= "Viloyatlar bo'yicha sodir bo'lgan avtohalokatlar")
# Samarqand + Xorazm
# Buxoro + Toshkent
# S+J+Q


violation_data = pd.read_csv(path + 'data/violation_data_19_20_Dec')

values_ = violation_data['0'][:6].values + [violation_data['0'][6:].sum()]
labels_ = violation_data.violation_type[:6] + ['boshqa_qoidabuzarliklar']

fig_pie = go.Figure()

fig_pie.add_trace(
    go.Pie(
        labels = labels_,
        values = values_,
    )
)
fig_pie.update_layout(
    title = '2020 hamda 2019-yillar dekabr oyida piyodani urib yuborinsh bilan sodir etilgan<br>yo\'l transport hodisalari tahlili' 
)
fig_pie.update_layout(hovermode="x", height = 520, template = "plotly_dark", font=dict(family="Playfair Display",))

grouped = data.groupby(['regions'])['date'].count().sort_values()

fig_whole_uzb = go.Figure()
fig_whole_uzb.add_trace(go.Bar(y = grouped.index,
                     x=grouped.values,
                     text = grouped.values,
                     orientation = 'h'))

fig_whole_uzb.layout = {
    'title': "Viloyatlar bo'yicha sodir bo'lgan avtohalokatlar",
    'xaxis': dict(
        zeroline = False,
        range = [1,15200]
    )
}
fig_whole_uzb.update_traces(textposition = 'outside')
fig_whole_uzb.update_layout(hovermode="x", height = 600, template = "plotly_dark", font=dict(family="Playfair Display",))


layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    # mapbox=dict(
    #     accesstoken=mapbox_access_token,
    #     style="light",
    #     center=dict(lon=-78.05, lat=42.54),
    #     zoom=7,
    # ),
)
YEARS = list(range(2013, 2022))

def br(n):
    return [html.Br()] * n

layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div([
            html.Div([
                        html.H1(children="Avtohalokatlar"),
                        dcc.Link(html.Button('Xarita', style = {'margin-left': 'auto', 'color': '#7fafdf', 'width': '100px', 'text-align': 'center'}, id = 'stat-button'), href="/", refresh=True, style = {'margin-left': 'auto'}),
                    ],
                        id="btn-title",
                    ),],
            id = 'header'),
   
        html.Div(
            [
                html.Div(
                    [
                        *br(3),
                        html.P(
                            "Yilni tanlang:",
                            className="control_label",
                        ),
                        html.Br(),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=min(year),
                            max=max(year),
                            step = 1,
                            value=[min(year), max(year)],
                            className="dcc_control",
                            marks={
                                        str(y): {
                                            "label": str(y),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for y in year
                                    },
                            
                            
                            ),
                            
                        *br(2),
                        html.P("Viloyatni tanlang:", className="control_label"),
                        html.Br(),
                        dcc.Dropdown(
                            id="viloyat",
                            options=data.regions.unique(),
                            # value=data.regions.unique(),
                            className="dcc_control",
                        ),
                        *br(3),
                        html.P("Avtohalokat turini tanlang:", className="control_label"),
                        html.Br(),
                        dcc.Dropdown(
                            id="halokat",
                            options=data.accident_type.unique(),
                            className="dcc_control",
                        ),
                        html.Br(),
                        html.Br(),
                        dcc.RadioItems(
                            id="well_type_selector",
                            options=[
                                {"label": " Barchasi ", "value": "all"},
                                {"label": " O'lim ", "value": "productive"},
                                {"label": " Jarohat ", "value": "custom"},
                            ],
                            value="productive",
                            labelStyle={"display": "block"},
                            className="dcc_control",
                        ),
                        *br(10),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="well_text", children=['Avtohalokatlar soni:']),html.H4(id="acc_nbr")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText", children='O\'lim:'),html.H4(id="death_nbr")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilText", children='Jarohat:'),html.H4(id="inj_nbr")],
                                    id="oil",
                                    className="mini_container",
                                )
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph", figure = fig)],
                    className="pretty_container fourteen columns",
                    id="countGraphContainer",
                )
            ],
            className="row flex-display",
           
        ),
        html.Div(
            [
                html.Div([
                    # html.P("Bar graph"),
                    dcc.Graph(id="main_graph2", figure = fig_whole_uzb)],
                    className="pretty_container sixteen columns",
                )
            ],
            className="row flex-display",
           
        ),
        html.Div(
            [
                html.Div([
                    # html.P("Pie chart"),
                    dcc.Graph(id="main_graph3", figure = fig_pie)],
                    className="pretty_container sixteen columns",
                )
            ],
            className="row flex-display",
           
        ),
    ],
    id="root",
    # id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


@callback(
    [
        Output("count_graph", "figure"),
        Output("acc_nbr", "children"),
        Output("death_nbr", "children"),
        Output("inj_nbr", "children")
        ],
    [
        Input("viloyat", "value"),
        Input("halokat", "value"),
        Input("year_slider", "value"),
    ],
)
def make_count_figure(viloyat, halokat, year_slider):
    d = data[((data.date.str[:4].astype(int) >= year_slider[0])&(data.date.str[:4].astype(int) < year_slider[1]))] 
    place = "O'zbekiston"
    time = str(year_slider[0]) + '-' + str(year_slider[1])
    if viloyat:
        d = d[d.regions == viloyat]
        place = viloyat
    if halokat:
        d = d[d.accident_type == halokat]
    text = "{0}da {1} yillar orasida sodir bo'lgan avtohalokatlar".format(place, time)

    fig = go.Figure()

    fig.add_trace(go.Histogram(x = d.date)) # space between bins 
    fig.layout = go.Layout(template = "plotly_dark", title = text, font=dict(family="Playfair Display",))
    # fig.update_traces( xbins = dict(size = 'M1'))

    acc_nbr = d.shape[0]
    death_nbr = d.died.sum()
    inj_nbr = d.injured.sum()
    
    return fig, acc_nbr, death_nbr, inj_nbr



# Main



