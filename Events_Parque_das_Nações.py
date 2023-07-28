#Parque das Nações
from bs4.element import SoupStrainer
import pandas as pd
import requests
from bs4 import BeautifulSoup
host = "https://www.jf-parquedasnacoes.pt/"
req = requests.get('https://www.jf-parquedasnacoes.pt/pages/667')
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
if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content
soup = BeautifulSoup(content, "html.parser")
page_list = requests.get(host + 'pages/667')
page_list = BeautifulSoup(page_list.content, "html.parser")
page_list = page_list.find("div",class_="pagination").find_all("a")
link_base = host + page_list[0].get("href").split("=")[0] + "="

page_list = [ int(p.get("href").split("=")[-1]) for p in page_list] + [1]
page_list = list(range(min(page_list),max(page_list)+1))
links = list(set([ link_base + str(p) for p in page_list]))
links.sort(key= lambda x : int(x.split("=")[-1]))
table = {i:[] for i in "titulo,dia_inicio,dia_final,mes_inicio,mes_final,ano_inicio,ano_final".split(",")}

for i in range(0,len(links)):
  link = requests.get(links[i])
  link = BeautifulSoup(link.content, "html.parser")
  for j in range(1, 12):
    if j == 1:
      classe = "pos_1 first"
    else:
      classe="pos_{0}".format(j)
    posts = link.find_all("li",class_= classe)
    for post in posts:
      dias = [ x.find_all("span", class_="dia") for x in post.find_all("div", class_="dates widget_field ")]
      meses = [ x.find_all("span", class_="mes_extenso")for x in post.find_all("div", class_="dates widget_field ")]
      anos  = [ x.find_all("span", class_="ano")for x in post.find_all("div", class_="dates widget_field ")]
      titulo = [x.find("h4").text for x in post.find_all("div", class_ = "title widget_field ")]
      #Verifica se a o span encontrado é da classe dia
      if dias:
        for var in [dias[0],meses[0],anos[0],titulo[0]]:
          if len(var) == 1 : var *= 2
        table["titulo"].append(titulo[0])
        table["dia_inicio"].append(dias[0][0].text)
        table["dia_final"].append(dias[0][1].text)
        table["mes_inicio"].append(meses[0][0].text)
        table["mes_final"].append(meses[0][1].text)
        table["ano_inicio"].append(anos[0][0].text)
        table["ano_final"].append(anos[0][1].text)
df = pd.DataFrame(table)
df["format"] = df["titulo"].apply(lambda x: formata(x))
df['ano_final'] = pd.to_numeric(df['ano_final'])
df.drop(df[df['ano_final'] < 16].index, inplace = True)
unique_events = df['titulo'].unique().tolist()
score_sort = [(x,) + i
             for x in unique_events
             for i in process.extract(x, unique_events,     scorer=score)]
#Create a dataframe from the tuples
similarity_sort = pd.DataFrame(score_sort, columns=['event_sort','match_sort','score_sort'])
similarity_sort['sorted_event_sort'] = np.minimum(similarity_sort['event_sort'], similarity_sort['event_sort'])
high_score_sort = similarity_sort[(similarity_sort['score_sort'] >= 71) &
                (similarity_sort['event_sort'] !=  similarity_sort['match_sort']) &
                (similarity_sort['sorted_event_sort'] != similarity_sort['match_sort'])]
high_score_sort = high_score_sort.drop('sorted_event_sort',axis=1).copy()
new_df = df
new_df["match"]  = df["titulo"]
for key, value in high_score_sort['event_sort'].iteritems():
    new_df['match'] = df['titulo'].replace([high_score_sort['match_sort'][key]],value)
new_df = new_df[new_df.duplicated(subset=['titulo'], keep=False)]
new_df.drop(new_df[new_df['ano_final'] < 2018].index, inplace = True)
new_df
