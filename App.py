from re import X
from dash import Dash
from dash_html_components import H1, Div, P
from dash_core_components import Graph, DatePickerSingle, Checklist
from dash.dependencies import Input, Output
from pandas.core.tools.numeric import to_numeric
import scrape
import datas
import pandas as pd
import plotly.express as px

# Variáveis iniciais
stations = ['IMACA7', 'IMACA13', 'ICAMPO96', 'IMACA15']
cidade = 'Macaé, RJ'

# Confere se o dia anterior foi computado e atualiza os dados
df = pd.read_csv('data.csv', index_col=0)
df.columns = scrape.colunas_total
if datas.ontem not in df.values:
    for station in stations: 
        data = scrape.scrape_daily_day(station, datas.ontem)
        data.to_csv('data.csv', mode='a', header=False)


# Lê as informações atualizadas
df = pd.read_csv('data.csv', index_col=0)
df.columns = scrape.colunas_total


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- DASH
# Define o objeto Dash
app = Dash(__name__)

# Layout (como a página em si será apresentada)
app.layout = Div(
    className="app-header",
    children=[
        H1(cidade),

        Div(
            className='history',
            children=[
                datas.ontem
            ]
        ),

        #DatePickerSingle(
        #    display_format='DD/MM/YYYY',
        #    id='my-date-picker-single',
        #    date=datas.ontem
        #),

        Checklist(
            id='checklist',
            options=[
                {'label': 'IMACA7', 'value': 'IMACA7'},
                {'label': 'IMACA13', 'value': 'IMACA13'},
                {'label': 'ICAMPO96', 'value': 'ICAMPO96'},
                {'label': 'IMACA15', 'value': 'IMACA15'}
            ],
            value=['IMACA7', 'IMACA13','ICAMPO96','IMACA15']
        ),

        Div(
            className='graphs',
            children=[
                Graph(id='grafico1'),
                Graph(id='grafico2'),
                Graph(id='grafico3'),
                Graph(id='grafico4')
            ]
        )
    ]
)

# Estilo dos gráficos
bar_colors = ['#ff6361','#58508d']
font_color = '#ffa600'
bg_color = '#003f5c'


# Pega a variável que foi inserida na data
@app.callback(
    Output('grafico1', 'figure'),
    Output('grafico2', 'figure'),
    Output('grafico3', 'figure'),
    Output('grafico4', 'figure'),
    Input('checklist', 'value'))
def update_output(station):
    # Filtra pela estação
    filtered_df = df[df.station.isin(station)]
    # Filtra pela data
    filtered_df2 = filtered_df[filtered_df['date']==datas.ontem]
    # Pega as colunas de temperatura para o gráfico 1
    tempdf = filtered_df2[['t high', 't low']]
    tempdf = tempdf.apply(pd.to_numeric)
    fig1 = px.bar(tempdf, barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
    fig1.update_layout(title='Temperatura',yaxis_title="Temperatura (°F)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=1)

    # Pega as colunas de humidade relativa para o gráfico 2
    rhdf = filtered_df2[['rh high', 'rh low']]
    rhdf = rhdf.apply(pd.to_numeric)
    fig2 = px.bar(rhdf, barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
    fig2.update_layout(title='Humidade Relativa',yaxis_title="Humidade (%)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=1)

    # Pega as colunas de velocidade do vento para o gráfico 3
    winddf = filtered_df2[['wind high', 'gust high']]
    winddf = winddf.apply(pd.to_numeric)
    fig3 = px.bar(winddf, barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
    fig3.update_layout(title='Velocidade do vento',yaxis_title="Velocidade (mph)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=1)

    # Pega a coluna de precipitação para o gráfico 4
    precdf = filtered_df2[['prec']]
    precdf = precdf.apply(pd.to_numeric)
    fig4 = px.bar(precdf, template="ygridoff",color_discrete_sequence= bar_colors)
    fig4.update_layout(title='Precipitação',yaxis_title="Precipitação (mm)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=1)
    return fig1, fig2, fig3, fig4

# Roda o servidor interno (8050)
if __name__ == '__main__':
    app.run_server(debug=True)
