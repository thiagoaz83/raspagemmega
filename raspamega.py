# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 21:21:46 2019
Transforma o arquivo html com os resultados da Mega-Sena (disponibilizado pela Caixa) em duas tabelas: uma com os dados gerais e outra com as cidades/ufs dos ganhadores da Sena.

@author: Thiago Azevedo
"""

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#Parte 0: CRIA FUNÇÕES AUXILIARES
#Atribuir valores de apostas
def apostas(resultados):
    r = resultados.reset_index()
    r["Concurso"] = r["Concurso"].astype(int)
    r["Aposta"] = np.NaN
    r.set_index("Concurso", inplace=True)
    
    #Estipula os preços das apostas únicas.
    r.loc[1, "Aposta"] = 1
    r.loc[511, "Aposta"] = 1.5
    r.loc[983, "Aposta"] = 1.75
    r.loc[1107, "Aposta"] = 2
    r.loc[1599, "Aposta"] = 2.5
    r.loc[1708, "Aposta"] = 3.5
    r.loc[2207, "Aposta"] = 4.5
    r["Aposta"].fillna(method="ffill", inplace = True)
    
    return r

#Cria colunas com valores correspondentes aos rateios
def rateios():
    pass

#PARTE 1: LEITURA

pagina = "d_mega.htm"

#Abre o BeautifulSoup com a página desejada.
soup = BeautifulSoup(open(pagina), "html.parser")
table = soup.find("table")

#Cria uma lista com os títulos das colunas da tabela.
titulo_colunas = []
for c in table.findNext("tr").findAll("th"):
    titulo_colunas.append(c.string)
    
#Cria uma lista em que cada linha da tabela é também uma lista.
lista_resultados = []
for row in table.findAll("tr"):
    celulas = row.findAll("td")
    linha = []
    for c in celulas:
        linha.append(c.string)
    if len(linha) > 0:
        lista_resultados.append(linha)

    
#Cria o dataframe bruto do pandas.
resultados = pd.DataFrame(data = lista_resultados, columns=titulo_colunas)

#Comando para exportar os dados brutos para um arquivo csv.
#resultados.to_csv("dadosbrutosmega.csv")

#PARTE 2: LIMPEZA
#Quando há mais de um vencedor da sena, as cidades/UFs ficam nas primeiras colunas.
#Correção para colocar as cidades/UFs nas respectivas colunas.
for index, row in resultados.iterrows():
    if row["Acumulado"] == None:
        row["Cidade"] = row["Concurso"]
        row["UF"] = row["Data Sorteio"]
        row["Concurso"] = None
        row["Data Sorteio"] = None

#Elimina espaços no início e no fim das palavras, além de converter todas as letras das Cidades e UFs para maiúsculas.
for campo in ["Cidade", "UF"]:
    resultados[campo] = resultados[campo].str.strip()
    resultados[campo] = resultados[campo].str.upper()
    resultados[campo] = resultados[campo].str.replace("\n", "")
    
resultados = resultados.replace("", np.nan)
resultados.fillna(np.nan, inplace = True)
    
#Converte as colunas para os valores numéricos/data adequados.
pd.options.display.float_format = '{:.2f}'.format

resultados["Data Sorteio"] = pd.to_datetime(resultados["Data Sorteio"], format="%d/%m/%Y")

for campo in ["Arrecadacao_Total", "Rateio_Sena", "Rateio_Quina", "Rateio_Quadra", "Valor_Acumulado", "Estimativa_Prêmio", "Acumulado_Mega_da_Virada", "Ganhadores_Sena", "Ganhadores_Quina", "Ganhadores_Quadra"]:
    resultados[campo] = resultados[campo].str.replace(".", "")
    resultados[campo] = resultados[campo].str.replace(",", ".")
    resultados[campo] = pd.to_numeric(resultados[campo])
    
#Preenche campos vazios em Concurso/Data Sorteio/Rateio Sena para preparar criação da tabela de ganhadores.
for campo in ["Concurso", "Data Sorteio", "Ganhadores_Sena", "Rateio_Sena"]:
    resultados[campo] = resultados[campo].fillna(method = "ffill")

#Faz uma cópia da tabela resultados para trabalhar com os ganhadores mais adiante.
ganhadores = resultados.copy()

#Limpa a tabela de resultados das linhas sem concursos e dezenas. Retira colunas Cidade e UFs dos resultados.
resultados = resultados[resultados["Arrecadacao_Total"] >= 0]
resultados.drop(columns=["Cidade", "UF"], inplace=True)
resultados.set_index("Concurso", drop = True, inplace = True)

#Tabela ganhadores: seleciona colunas e linhas que serão úteis.
ganhadores = ganhadores[["Concurso","Data Sorteio","Cidade","UF","Ganhadores_Sena","Rateio_Sena"]]
ganhadores = ganhadores[ganhadores["Ganhadores_Sena"] > 0]
ganhadores.drop(columns=["Ganhadores_Sena"], inplace=True)

#Verificar cidades e UFs em branco e preencher com "não disponível".
ganhadores["Cidade"].fillna("CIDADE NÃO DIVULGADA", inplace = True)
ganhadores["UF"].fillna("NDV", inplace = True)

#Verificar também se número de linhas corresponde ao número de vencedores por concurso.
concursos_vencedores = resultados[resultados["Ganhadores_Sena"] > 0].index.unique()
lista_ganhadores_extras = []
for conc in concursos_vencedores:
    vencedores = resultados.loc[conc]["Ganhadores_Sena"]
    if len(ganhadores[ganhadores["Concurso"] == conc]) < vencedores:
        duplicar = ganhadores[ganhadores["Concurso"] == conc].iloc[0].to_dict()
        duplicar["Cidade"] = "CIDADE NÃO DIVULGADA"
        duplicar["UF"] = "NDV"
        for i in range(int(vencedores) - len(ganhadores[ganhadores["Concurso"] == conc])):
            lista_ganhadores_extras.append(duplicar)
ganhadores = ganhadores.append(lista_ganhadores_extras, ignore_index=True)
ganhadores.sort_values(["Data Sorteio", "UF", "Cidade"], inplace=True)
ganhadores.reset_index(drop = True, inplace= True)

#Fase experimental: atribui valor unitário de aposta para cada concurso. Cria coluna Num_Apostas, com o número de apostas para cada sorteio.
resultados = apostas(resultados)
resultados["Num_Apostas"] = resultados["Arrecadacao_Total"] / resultados ["Aposta"]

#Exportar as duas tabelas para o Excel
writer = pd.ExcelWriter("resultadosmega.xlsx", engine = "xlsxwriter")
resultados.to_excel(writer, sheet_name = "Resultados")
ganhadores.to_excel(writer, sheet_name = "Ganhadores por Cidade", index = False)
writer.save()