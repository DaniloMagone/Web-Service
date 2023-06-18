import xml.etree.ElementTree as ET
import requests
import pandas as pd
import datetime

def get_week_day(date_str):
  date = datetime.datetime.strptime(date_str.split("T")[0],"%Y-%m-%d").weekday()
  week_days = "segunda,terca,quarta,quinta,sexta,sabado,domingo".split(",")
  return week_days[date]

def remove_tag(tags, document,generic_tag):
  # Separando todas as tags 
  # Como o final de cada tag é indicada por > , quebra o texto por esse caractere
  # assim, tem uma lista de <tag1 , <tagX, texto, </tagX, </tag 1 (por exemplo)
  document = document.split(">")

  for tag_to_remove in tags:
    # remove da lista de tags, todos os elementos que contem parte do "tag_to_remove" em seu conteudo
    document = list(filter(lambda x : not tag_to_remove in x , document))

  # unindo a lista com o operador > , que anteriormente havia sido removido
  document = ">".join(document)

  # inserindo ao inico e ao final a <generic_tag> </generic_tag>
  document = f"<{generic_tag}>{document}\n</{generic_tag}>"

  return document
text=""
cols = ["Feriado","date"]
rows = []
tags_to_remove=["GetNationalHolidaysResult", "GetNationalHolidaysResponse"]
#Coleta os dados de 2018 a 2023
for year in range(2018,2023):
  url = 'https://services.sapo.pt/Holiday/GetNationalHolidays?year='+ str(year)
  req = requests.get(url)
  if req.status_code == 200:
    content = req.content.decode('utf-8')
    content= remove_tag(tags_to_remove,content,"data")
    root = ET.fromstring(content)
    for child in root:
      feriado =  child.find('Name').text
      date = child.find('Date').text
      rows.append({"Feriado": feriado,
                 "date": date})
  else:
    print('Requisição mal sucedida')
    break

df = pd.DataFrame(rows, columns=cols)
# Escreve o dataframe em um csv, adicionando os dias da semana e a data
cols2 = ["Feriado","Data","Ano","Mes","Dia","DiaSemana"]
rows2 = []
csv_2 = pd.DataFrame(rows2, columns=cols2)
csv_2["Feriado"] = df["Feriado"]
csv_2["Ano"] = df["date"].apply(lambda x : datetime.datetime.strptime(x.split("T")[0],"%Y-%m-%d").year)
csv_2["Mes"] = df["date"].apply(lambda x : datetime.datetime.strptime(x.split("T")[0],"%Y-%m-%d").month)
csv_2["Dia"] = df["date"].apply(lambda x : datetime.datetime.strptime(x.split("T")[0],"%Y-%m-%d").day)
csv_2["DiaSemana"] = df["date"].apply( get_week_day )
csv_2["Data"] = df["date"].apply( lambda x : x.split("T")[0])
print(csv_2)
#df_cities.to_csv('feriados_municipais.csv')
csv_2.to_csv('feriados_nacionais.csv')
