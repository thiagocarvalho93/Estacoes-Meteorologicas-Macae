import datas

# Formato do link antes dos parâmetros
link_base = 'https://www.wunderground.com/dashboard/pws/'

# Stations
stations = ['IMACA7', 'IMACA13', 'ICAMPO96', 'IMACA15']

# Links dos dados a serem extraidos
links_wunderground_daily = [link_base + station + '/table/' + datas.ontem + '/' + datas.ontem 
                      + '/daily' for station in stations]

if __name__ == '__main__':
    print(links_wunderground_daily)

