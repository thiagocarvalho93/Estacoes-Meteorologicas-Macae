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
bar_colors = ['#EA6A47','#0091D5']
font_color = '#202020'
bg_color = '#F1F1F1'


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
    tempdf = filtered_df2[['t high', 't low','station']]
    fig1 = px.bar(tempdf,x='station',y=['t high', 't low'], barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
    fig1.update_layout(title='Temperatura',yaxis_title="Temperatura (°F)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=12, showlegend=False)
    # Mostra os valores em cima do gráfico
    texts1 = [tempdf['t high'], tempdf['t low']]
    for i, t in enumerate(texts1):
        fig1.data[i].text = t
        fig1.data[i].textposition = 'inside'



    # Pega as colunas de humidade relativa para o gráfico 2
    rhdf = filtered_df2[['rh high', 'rh low','station']]
    fig2 = px.bar(rhdf, x='station', y=['rh high', 'rh low'], barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
    fig2.update_layout(title='Humidade Relativa',yaxis_title="Humidade (%)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=12, showlegend=False)
    # Mostra os valores em cima do gráfico
    texts2 = [rhdf['rh high'], rhdf['rh low']]
    for i, t in enumerate(texts2):
        fig2.data[i].text = t
        fig2.data[i].textposition = 'inside'

    # Pega as colunas de velocidade do vento para o gráfico 3
    winddf = filtered_df2[['gust high', 'wind high','station']]
    fig3 = px.bar(winddf, x= 'station', y= ['gust high', 'wind high'], barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
    fig3.update_layout(title='Velocidade do vento',yaxis_title="Velocidade (mph)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=12, showlegend=False)
    # Mostra os valores em cima do gráfico
    texts3 = [winddf['gust high'], winddf['wind high']]
    for i, t in enumerate(texts3):
        fig3.data[i].text = t
        fig3.data[i].textposition = 'inside'

    # Pega a coluna de precipitação para o gráfico 4
    precdf = filtered_df2[['prec','station']]
    fig4 = px.bar(precdf,x= 'station', y='prec', template="ygridoff",color_discrete_sequence= ['#0091D5'])
    fig4.update_layout(title='Precipitação',yaxis_title="Precipitação (in)",
    xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
    font_color=font_color,xaxis_tickfont_size=12, showlegend=False)
    # Mostra os valores em cima do gráfico
    texts4 = [precdf['prec']]
    for i, t in enumerate(texts4):
        fig4.data[i].text = t
        fig4.data[i].textposition = 'inside'

    # Retorna os gráficos
    return fig1, fig2, fig3, fig4
# Roda o servidor interno (8050)
if __name__ == '__main__':
    app.run_server(debug=True)
