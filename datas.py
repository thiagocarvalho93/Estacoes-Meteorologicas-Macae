from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

# Fuso horário
timezone_offset = -3.0
tzinfo = timezone(timedelta(hours = timezone_offset))

# Formatação da data no link do site
ontem = (datetime.now(tzinfo) - relativedelta(days=1)).strftime("%Y-%m-%d")

# Input numero de dias passados e retorna a data no formato do link
def dia_atras_tabela (dias_atras):
    dia = (datetime.now()-relativedelta(days=dias_atras)).strftime("%Y-%m-%d")
    return dia

# Formatação brasileira
ontem_br = (datetime.now(tzinfo) - relativedelta(days=1)).strftime("%d/%m/%Y")

# ------------- Formatação da data na tabela do site
# Ontem no formato usado na tabela:
ontem_tabela = (datetime.now(tzinfo) - relativedelta(days=1)).strftime("%m/%d/%Y")
# Tira o zero do início se o mês menor que 10
if int((datetime.now(tzinfo) - relativedelta(days=1)).strftime("%m")) < 10:
    ontem_tabela = ontem_tabela[1:]

# Hoje no formato da tabela
if int(datetime.now(tzinfo).strftime('%m')) < 10:
    hoje_tabela = datetime.now(tzinfo).strftime("%m/%d/%Y")[1:]
else:
    hoje_tabela = datetime.now(tzinfo).strftime("%m/%d/%Y")
