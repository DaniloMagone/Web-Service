#Matosinhos
from bs4.element import SoupStrainer
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process, fuzz
import numpy as np

def formata(palavra):
  #comando para letra minuscula
  palavra = palavra.lower()

  # removendo letras especificas
  remover_letras = "ivx,.;:-_!' \"#$%&/()={}[]@+-*/123456789ª|"
  for letra in remover_letras:
    palavra = palavra.replace(letra,"")

  # removendo acentos e chars especiais
  from unidecode import unidecode
  palavra = unidecode(palavra)

  return palavra

from Levenshtein import distance as lev
def score(pa,pb):
  return 1 - ( lev(pa,pb) / max(len(pa),len(pb)))

host = "https://www.cm-matosinhos.pt/"
link_list = []
for j in range(0,195):
   link_list.append((host + '/servicos-municipais/comunicacao-e-imagem/eventos?events_list_37_page=' + str(j+1)))

# aqui está um exemplo de uso +- igual o seu
table = {i:[] for i in "titulo,link,dia_inicio,dia_final,mes_inicio,mes_final,ano_inicio,ano_final".split(",")}
for link in link_list:
  link = requests.get(link)
  link = BeautifulSoup(link.content, "html.parser")
  posts = link.find_all("div",class_="linl_block")
  for post in posts:
    dia = [ x.text for x in post.find_all("span",class_="dia")]
    mes = [ x.text for x in post.find_all("span",class_="mes_curto")]
    ano = [ x.text for x in post.find_all("span",class_="ano")]
    for var in [dia,mes,ano] :
      if len(var) == 1 : var *= 2
    table["dia_inicio"].append(dia[0])
    table["dia_final"].append(dia[1])
    table["mes_inicio"].append(mes[0])
    table["mes_final"].append(mes[1])
    table["ano_inicio"].append(ano[0])
    table["ano_final"].append(ano[1])
    table["titulo"].append(host+post.find("a",class_="linl_overlay").get("href"))
    table["link"].append(post.find("div",class_="title").find("h2").text)
df = pd.DataFrame(table)
df["format"] = df["link"].apply(lambda x: formata(x))
df['ano_final'] = df['ano_final'].str.replace("'", "")
df['ano_final'] = pd.to_numeric(df['ano_final'])
df.drop(df[df['ano_final'] < 16].index, inplace = True)
unique_events = df['link'].unique().tolist()
score_sort = [(x,) + i
             for x in unique_events
             for i in process.extract(x, unique_events,     scorer=score)]

similarity_sort = pd.DataFrame(score_sort, columns=['event_sort','match_sort','score_sort'])
similarity_sort['sorted_event_sort'] = np.minimum(similarity_sort['event_sort'], similarity_sort['event_sort'])
high_score_sort = similarity_sort[(similarity_sort['score_sort'] >= 71) &
                (similarity_sort['event_sort'] !=  similarity_sort['match_sort']) &
                (similarity_sort['sorted_event_sort'] != similarity_sort['match_sort'])]
high_score_sort = high_score_sort.drop('sorted_event_sort',axis=1).copy()

new_df = df
new_df["match"]  = df["link"]
for key, value in high_score_sort['event_sort'].iteritems():
    new_df['match'] = df['link'].replace([high_score_sort['match_sort'][key]],value)
new_df = new_df[new_df.duplicated(subset=['link'], keep=False)]
new_df.drop(new_df[new_df['ano_final'] < 18].index, inplace = True)
new_df
