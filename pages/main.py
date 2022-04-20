from dash import callback, html, dcc
import pandas as pd

from dash.dependencies import Input, Output, State

import numpy as np
import folium
from folium import plugins
from folium.features import DivIcon

path = './'

def make_map(data):
    heatmap = folium.Map(location=[41.3298,69.263],
                         zoom_start =13,
                         #tiles='CartoDBdark_matter'
                        )

    folium.plugins.HeatMap(list(zip(data.latitude,
                                    data.longitude)),
                           radius=30,
                           blur=15,
                          ).add_to(heatmap)

    for lat, lon, date, death, injury, weather, day_part, acc_type in data.values:

        # popup = folium.Popup(f'Sana: {date.strftime("%Y %m %d")}<br>O\'lim: {number}', min_width=150, max_width=300)
        tooltip = f'Sana: {date.strftime("%Y %m %d")}<br>\
                    Vaqt: {date.strftime("%H:%M")}'
        if weather: tooltip = tooltip + f'<br>Havo holati: {weather}'
        if injury: tooltip = tooltip + f'<br>Jarohat: {injury}'

        rad = 15
        opacity = 0
        fill_opacity = 0

        if death > 0:
            tooltip = tooltip + f'<br>O\'lim: {death}'
            rad = death*2 + 3
            opacity = 1
            fill_opacity = 1

            icon = DivIcon(
                icon_size=(150,150),
                icon_anchor=(0,0),
                html='<div style="font-size: 100pt color: black">%s</div>' % death,
                )
            div = folium.DivIcon(html=(
                        '<svg height="100" width="100">'
                        '<circle cx="50" cy="50" r="40" stroke="yellow" stroke-width="3" fill="none" />'
                        '<text x="30" y="50" fill="black">9000</text>'
                        '</svg>'
                    ))
        tooltip = tooltip + f'<br>Avtohalokat turi: {acc_type}'

        folium.CircleMarker([lat, lon],
                            radius = rad,
                            color = 'red',
                            fill_color = 'red',
                            fill = True,
                            tooltip=tooltip,
                            opacity = opacity,
                            fill_opacity = fill_opacity,
                            icon = False,
                           ).add_to(heatmap)
    heatmap.save('map_flt.html')
    return open('map_flt.html', 'r').read()

data_tash = pd.read_csv(path + 'data/data_tashkent.csv')
data_tash.date = pd.to_datetime(data_tash.date)
data_tash = data_tash.replace({np.nan: None})

# Initialize app
#
# app = dash.Dash(
#     __name__,
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
#     ],
# )
# app.title = "Avtohalokatlar"
# application = app.server

# App layout

layout = html.Div(
    id="root",
    children=[
        html.Div( 
            id="header",
            children=[
                html.Div([
                    html.H1(children="Avtohalokatlar"),
                    dcc.Link(html.Button('Statistika', style = {'margin-left': 'auto', 'color': '#7fafdf', 'width': '140px', 'text-align': 'center'}, id = 'stat-button'), href="/page-1", refresh=True, style = {'margin-left': 'auto'}),
                ],
                    id="btn-title",
                ),
                html.H5(children="Toshkent shahrida sodir bo'layotgan avtohalokatlar xaritasi"),
                html.H6(
                    id="description",
                    children=f"Ushbu xaritada 2020-yil 1-yanvardan buyon sodir bo'lgan 1067 ta avtohalokat ko'rsatilgan.\
                    Bu davr mobaynida 1964 ta avtohalokat sodir bo'lgan, ammo ularning\
                    864 tasida kenglik va uzunlik ma'lumotlari berilmagan.",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.Div([
                                    html.P(
                                        id="slider-text",
                                        children="Avtohalokat turini tanlang:",
                                    ),
                                    dcc.Dropdown(
                                        options=[{"label": x, "value": x}
                                            for x in data_tash.accident_type.unique()
                                        ],
                                        placeholder = 'Barchasi',
                                        multi = True,
                                        searchable = False,
                                        id="chart-dropdown",
                                    ),
                                ]),
                            
                                
                            ],
                        ),
                        html.Br(),
                        html.Div(
                            id="heatmap-container",
                            children=[
#                                 html.P(
#                                     "Heatmap of age adjusted mortality rates \
#                             from poisonings in year",
#                                     id="heatmap-title",
#                                 ),
#                                 dcc.Graph(
#                                     id="county-choropleth",
#                                     figure=dict(
#                                         layout=dict(
#                                             mapbox=dict(
#                                                 layers=[],
#                                                 accesstoken=mapbox_access_token,
#                                                 style=mapbox_style,
#                                                 center=dict(
#                                                     lat=38.72490, lon=-95.61446
#                                                 ),
#                                                 pitch=0,
#                                                 zoom=3.5,
#                                             ),
#                                             autosize=True,
#                                         ),
#                                     ),
#                                 ),
                                html.Iframe(id="county-choropleth", style = {'width' : '100%', 'height' : '600px'})
                            ],
                        style = {'width' : '100%', 'height' : '600px'}
                        ),
                    ],
                ),
#                 html.Div(
#                     id="graph-container",
#                     children=[
#                         html.P(id="chart-selector", children="Select chart:"),
#                         dcc.Dropdown(
#                             options=[
#                                 {
#                                     "label": "Histogram of total number of deaths (single year)",
#                                     "value": "show_absolute_deaths_single_year",
#                                 },
#                                 {
#                                     "label": "Histogram of total number of deaths (1999-2016)",
#                                     "value": "absolute_deaths_all_time",
#                                 },
#                                 {
#                                     "label": "Age-adjusted death rate (single year)",
#                                     "value": "show_death_rate_single_year",
#                                 },
#                                 {
#                                     "label": "Trends in age-adjusted death rate (1999-2016)",
#                                     "value": "death_rate_all_time",
#                                 },
#                             ],
#                             value="show_death_rate_single_year",
#                             id="chart-dropdown",
#                         ),
#                         dcc.Graph(
#                             id="selected-data",
#                             figure=dict(
#                                 data=[dict(x=0, y=0)],
#                                 layout=dict(
#                                     paper_bgcolor="#F4F4F8",
#                                     plot_bgcolor="#F4F4F8",
#                                     autofill=True,
#                                     margin=dict(t=75, r=50, b=100, l=50),
#                                 ),
#                             ),
#                         ),
#                     ],
#                 ),
                
            ],
        ),
        html.Div([
            html.Div([
                html.Div(
                        id="new-container",
                        children=[

                            html.Img(src = 'assets/sng_acc.png',width=50, height=50),
                            html.H5(children="Yo'l transport hodisasi",style = {'margin-left': '20px'}),
                        ],
                    style = {'display': 'flex', 'align-items': 'center'}
                ),
                html.Br(),
                html.Div(
                        id="new-container2",
                        children=[

                            html.Img(src = 'assets/death.png',width=50, height=50),
                            html.H5(children="Fuqoro vafot etgan YHT",style = {'margin-left': '20px'}),
                        ],
                    style = {'display': 'flex', 'align-items': 'center'}
                )],
            style = {'margin-left':'20px'}),
            html.Div([
                html.Div(
                        id="new-container3",
                        children=[

                            html.Img(src = 'assets/two_acc.png',width=50, height=50),
                            html.H5(children="2 ta YHT",style = {'margin-left': '20px'}),
                        ],
                    style = {'display': 'flex', 'align-items': 'center'}
                ),
                html.Br(),
                html.Div(
                        id="new-container4",
                        children=[

                            html.Img(src = 'assets/four_acc.png', width=50, height=50),
                            html.H5(children="4 ta va undan ko'p YHT",style = {'margin-left': '20px'}),
                        ],
                    style = {'display': 'flex', 'align-items': 'center'}
                )],
                style = {'margin-left':'50px'}
            )
        ],
            style = {'display': 'flex'}
        
                ),
    ],
)

# @callback(
#     Output(),
#     Input('stat-button', 'n_click')
# )
@callback(Output("county-choropleth", "srcDoc"), Input("chart-dropdown", "value"))
def update_map(acc_type):
    if acc_type:
        data = data_tash[data_tash.accident_type.isin(acc_type)]
        return make_map(data)
    else:
        return open(path + 'pages/map.html', 'r').read()

