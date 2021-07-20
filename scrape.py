import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datas
import links
import plotly.express as px


# Coluna do dataframe obtido no link 'daily'
colunas_diario = ['t high','t low', 't avg', 'dew high', 'dew low', 'dew avg', 'rh high', 'rh low', 'rh avg', 'prec','prec low', 'prec avg', 'wind high', 'wind low', 'wind avg','gust high','gust avg',
    'w direction 1', 'wind direction 2', 'p high', 'p low', 'p avg']

colunas_total = ['date','station','t high','t low', 't avg', 'dew high', 'dew low', 'dew avg', 'rh high', 'rh low', 'rh avg', 'prec','prec low', 'prec avg', 'wind high', 'wind low', 'wind avg','gust high','gust avg',
    'w direction 1', 'wind direction 2', 'p high', 'p low', 'p avg']

# Estações
stations = ['IMACA7', 'IMACA13', 'ICAMPO96', 'IMACA15']

# Retira os dados crus em txt da web
def scrape_data(link):
    res = requests.get(link)
    if res.status_code == 200:
        soup_data = BeautifulSoup(res.text, 'html.parser')
        data_text = soup_data.text
        return data_text
    return False

# Filtra os dados do Wunderground
def filtra_dados_1(dados):
    # Obtendo os dados de ontem na tabela do site
    text1 = dados.split(datas.ontem_tabela)
    text1.pop(0)
    text1 = text1[1].split(datas.hoje_tabela)
    text1.pop(1)
    text1 = text1[0].replace('\xa0°',' ')
    text1 = re.sub(r' +',' ', text1)
    text1 = re.sub(r'[a-zA-Z/%²]','', text1)
    lista = text1.split(' ')
    lista.pop(-1)
    # Convertendo em float
    for i in range(len(lista)):
        lista[i] = float(lista[i])
    # Conversão de unidades
    # Farenheit para Celsius
    for n in range(6):
        lista[n] = round((lista[n] - 32) * 5/9, 1)
    # mph para km/h:
    for n in range(3):
        lista[n+9] = round(lista[n+9] * 1.60934, 1)


    # Dando nome aos bois
    dic = {
    'temp_high' : lista[0],
    'temp_avg' : lista[1],
    'temp_low' : lista[2],
    'dew_high' : lista[3],
    'dew_avg' : lista[4],
    'dew_low' : lista[5],
    'humi_high' : lista[6],
    'humi_avg' : lista[7],
    'humi_low' : lista[8],
    'spd_high' : lista[9],
    'spd_avg' : lista[10],
    'spd_low' : lista[11],
    'prss_high' : lista[12],
    'prss_low' : lista[13],
    'precip_ac' : lista[14]
    }
    return dic

# Filtra os dados do uwyo
def filtra_dados_2(dados):
    lista = dados.split('SBME')
    lista.pop(0)
    lista.pop(0)
    total = []
    for n in range(len(lista)):
        linha = lista[n].split()
        # Tira dados de clouds
        while len(linha) > 8:
            linha.pop(-1)
        total.append(linha)

    # Transforma os dados em um dataframe
    dataframe = pd.DataFrame(total, columns=['Time', 'ALTM', 'TMP', 'DEW', 'RH', 'DIR', 'SPD', 'VIS'])
    dataframe['ALTM'] = dataframe['ALTM'].astype(float)
    # Converte para float
    dataframe['TMP'] = dataframe['TMP'].astype(float)
    dataframe['DEW'] = dataframe['DEW'].astype(float)
    dataframe['RH'] = dataframe['RH'].astype(float)
    dataframe['DIR'] = dataframe['DIR'].astype(float)
    dataframe['SPD'] = dataframe['SPD'].astype(float)
    dataframe['VIS'] = dataframe['VIS'].astype(float)
    # Dando nome aos bois
    dic = {
        'temp_high' : dataframe['TMP'].max(),
        'temp_avg' : round(dataframe['TMP'].mean(),1),
        'temp_low' : dataframe['TMP'].min(),
        'dew_high' : dataframe['DEW'].max(),
        'dew_avg' : round(dataframe['DEW'].mean(),1),
        'dew_low' : dataframe['DEW'].min(),
        'humi_high' : dataframe['RH'].max(),
        'humi_avg' : round(dataframe['RH'].mean(),1),
        'humi_low' : dataframe['RH'].min(),
        'spd_high' : dataframe['SPD'].max(),
        'spd_avg' : round(dataframe['SPD'].mean(),1),
        'spd_low' : dataframe['SPD'].min(),
        'prss_high' : '',
        'prss_low' : '',
        'precip_ac' : ''
        }
    return dic

# Pega os dados do dia anterior da estação station
def scrape_daily_yesterday(station):
    link = links.link_base + station + '/table/' + datas.ontem + '/' + datas.ontem + '/daily'
    text1 = scrape_data(link)
    text1 = text1.split('HighLowAverageTemperature')
    text1.pop(0)
    text1 = text1[0].split('graphtable')
    text1.pop(1)
    text1 = text1[0].replace('\xa0°','')
    text1 = re.sub(r'[a-zA-Z/%²]',' ', text1)
    text1 = re.sub(r' +',' ', text1)
    text1 = re.sub(r'--','', text1)
    lista = text1.split(' ')
    lista.pop(-1)

    df = pd.DataFrame(lista).transpose()

    df.columns=colunas_diario
    
    return df

# Pega os dados de um dia específico atrás (ex: day=5 pega os dados de 5 dias atrás)
def scrape_daily_day(station, day):
    link = links.link_base + station + '/table/' + day + '/' + day + '/daily'
    text1 = scrape_data(link)
    text1 = text1.split('HighLowAverageTemperature')
    text1.pop(0)
    text1 = text1[0].split('graphtable')
    text1.pop(1)
    text1 = text1[0].replace('\xa0°','')
    text1 = re.sub(r'[a-zA-Z/%²]',' ', text1)
    text1 = re.sub(r' +',' ', text1)
    text1 = re.sub(r'--','', text1)
    lista = text1.split(' ')
    lista.pop(-1)

    df = pd.DataFrame(lista).transpose()

    df.columns=['t high','t low', 't avg', 'dew high', 'dew low', 'dew avg', 'rh high', 'rh low', 'rh avg', 'prec','prec low', 'prec avg', 'wind high', 'wind low', 'wind avg','gust high','gust avg',
    'w direction 1', 'wind direction 2', 'p high', 'p low', 'p avg']
    df.insert(0,'station',station)
    df.insert(0,'date', day)
    df.index = [station + '-' + day]

    return df

# Scraping i dias atrás
'''
if __name__ == '__main__':
    i = 5
    while i > 0:
        for station in stations: 
            data = scrape_daily_day(station, datas.dia_atras_tabela(i))
            data.to_csv('data.csv', mode='a', header=False)
            print(datas.dia_atras_tabela(i))
        i-=1

'''

'''
if __name__ == '__main__':
    df = pd.read_csv('data.csv', index_col=0)
    df.columns = colunas_total
    df = df.dropna(axis=1)
    df1 = df[['t high', 't low']]
    df = df1.apply(pd.to_numeric)
    print(df)
'''
