from re import X
from dash import Dash
from dash_html_components import H1, Div, P
from dash_core_components import Graph, RadioItems, Checklist
from dash.dependencies import Input, Output
from pandas.core.tools.numeric import to_numeric
import pandas as pd
import plotly.express as px
import api

# Desativa falso alarme
pd.options.mode.chained_assignment = None

# Variáveis iniciais
ids = ['IMACA7', 'IMACA13', 'ICAMPO96', 'IMACA15']
cidade = 'Macaé, RJ'

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- DASH
# Define o objeto Dash
app = Dash(__name__)
server = app.server

# Layout (como a página em si será apresentada)
app.layout = Div(
    className="app-header",
    children=[
        H1(cidade),

        Div(
            className='history',
            children=[
                'Dados de: ' + api.api_df['date'].iloc[-1]
            ]
        ),

        #DatePickerSingle(
        #    display_format='DD/MM/YYYY',
        #    id='my-date-picker-single',
        #    date=datas.ontem
        #),

        RadioItems(
            id='radio',
            options=[
                {'label': '°C', 'value': 1},
                {'label': '°F', 'value': 0}
            ],
            value=1
        ),

        Checklist(
            id='checklist',
            options=[
                {'label': 'IMACA7 (Mirante da Lagoa)', 'value': 'IMACA7'},
                {'label': 'IMACA13 (Glicério)', 'value': 'IMACA13'},
                {'label': 'ICAMPO96 (Campos dos Goytacazes)', 'value': 'ICAMPO96'},
                {'label': 'IMACA15 (Colégio Ativo)', 'value': 'IMACA15'}
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

# Atualiza os gráficos
@app.callback(
    Output('grafico1', 'figure'),
    Output('grafico2', 'figure'),
    Output('grafico3', 'figure'),
    Output('grafico4', 'figure'),
    Input('checklist', 'value'),
    Input('radio', 'value')
)
def update_output(id, celsius):

    # Inicia com as figuras vazias
    if len(id) == 0:
        fig1 = dict({
        "data": [],
        "layout": {"title": {"text": "No Data"},
                    'plot_bgcolor': bg_color,
                    'paper_bgcolor': bg_color,
        }
        })
        fig2 = fig1
        fig3 = fig1
        fig4 = fig1
    else:
        # Busca a API
        df = api.api_df
        filtered_df = df[df.id.isin(id)]
        tempdf = filtered_df[['t_high', 't_low','id']]
        # Filtra pela estação
        #filtered_df = df[df.id.isin(id)]
        # Filtra pela data
        #filtered_df2 = filtered_df[filtered_df['date']==datas.ontem]
        # Pega as colunas de temperatura para o gráfico 1
        #tempdf = filtered_df2[['t_high', 't_low','id']]
        # Converte valores
        if celsius:
            tempdf['t_high'] = round((tempdf['t_high']-32)*(5/9),1)
            tempdf['t_low'] = round((tempdf['t_low']-32)*(5/9), 1)
            escala1 = '<b>Temperatura (°C)</b>'
            scalerange = [0,50]
        else:
            escala1 = '<b>Temperatura (°F)</b>'
            scalerange = [32,122]

        # Construção do gráfico
        fig1 = px.bar(tempdf,x='id',y=['t_high', 't_low'], barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
        fig1.update_layout(title='<b>Temperatura</b>',yaxis_title= escala1,
        xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
        font_color=font_color,xaxis_tickfont_size=12, showlegend=False, dragmode= False)
        fig1.update_traces(hovertemplate=None, hoverinfo='skip')
        fig1.update_layout(yaxis_range=scalerange)
        # Mostra os valores em cima do gráfico
        texts1 = [tempdf['t_high'], tempdf['t_low']]

        for i, t in enumerate(texts1):
            fig1.data[i].text = t 
            fig1.data[i].textposition = 'outside'    
        # Pega as colunas de humidade relativa para o gráfico 2
        rhdf = filtered_df[['rh_high', 'rh_low','id']]
        #rhdf = filtered_df2[['rh_high', 'rh_low','id']]
        # Construção do gráfico
        fig2 = px.bar(rhdf, x='id', y=['rh_high', 'rh_low'], barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
        fig2.update_layout(title='<b>Humidade Relativa</b>',yaxis_title="<b>Humidade (%)</b>",
        xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
        font_color=font_color,xaxis_tickfont_size=12, showlegend=False, dragmode= False)
        fig2.update_layout(yaxis_range=[0,100])
        fig2.update_traces(hovertemplate=None, hoverinfo='skip')


        # Mostra os valores em cima do gráfico
        texts2 = [rhdf['rh_high'], rhdf['rh_low']]
        for i, t in enumerate(texts2):
            fig2.data[i].text = t
            fig2.data[i].textposition = 'outside'

        # Pega as colunas de velocidade do vento para o gráfico 3
        winddf = filtered_df[['gust_high', 'wind_high','id']]
        #winddf = filtered_df2[['gust_high', 'wind_high','id']]
        # Conversão de unidades
        if celsius:
            winddf['gust_high'] = round(winddf['gust_high']*1.60934,1)
            winddf['wind_high'] = round(winddf['wind_high']*1.60934, 1)
            escala2 = '<b>Velocidade (Km/h)</b>'
            scalerange3 = [0,200]
        else:
            escala2 = '<b>Velocidade (mph)</b>'
            scalerange3 = [0,125]
        # Construção do gráfico
        fig3 = px.bar(winddf, x= 'id', y= ['gust_high', 'wind_high'], barmode='group', template="ygridoff",color_discrete_sequence= bar_colors)
        fig3.update_layout(title='<b>Velocidade do vento</b>',yaxis_title= escala2,
        xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
        font_color=font_color,xaxis_tickfont_size=12, showlegend=False, dragmode= False)
        fig3.update_layout(yaxis_range=scalerange3)
        fig3.update_traces(hovertemplate=None, hoverinfo='skip')

        # Mostra os valores em cima do gráfico
        texts3 = [winddf['gust_high'], winddf['wind_high']]
        for i, t in enumerate(texts3):
            fig3.data[i].text = t
            fig3.data[i].textposition = 'outside'

        # Pega a coluna de precipitação para o gráfico 4
        precdf = filtered_df[['prec','id']]
        #precdf = filtered_df2[['prec','id']]
        if celsius:
            precdf['prec'] = round(precdf['prec']*25.4,1)
            escala3 = '<b>Precipitação (mm)</b>'
            scalerange4 = [0,150]
        else:
            escala3 = "<b>Precipitação (in)</b>"
            scalerange4 = [0,8]
        # Construção do gráfico
        fig4 = px.bar(precdf,x= 'id', y='prec', template="ygridoff",color_discrete_sequence= ['#0091D5'])
        fig4.update_layout(title='<b>Precipitação</b>',yaxis_title= escala3,
        xaxis_title="Estação",legend_title="Legenda", plot_bgcolor=bg_color, paper_bgcolor=bg_color,
        font_color=font_color,xaxis_tickfont_size=12, showlegend=False, dragmode= False)
        fig4.update_layout(yaxis_range=scalerange4)
        fig4.update_traces(hovertemplate=None, hoverinfo='skip')

        # Mostra os valores em cima do gráfico
        texts4 = [precdf['prec']]
        for i, t in enumerate(texts4):
            fig4.data[i].text = t
            fig4.data[i].textposition = 'outside'

    # Retorna os gráficos
    return fig1, fig2, fig3, fig4

# Roda o app no servidor
if __name__ == '__main__':
    app.run_server(debug=True)
