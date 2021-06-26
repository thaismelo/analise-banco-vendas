#importando as bibliotecas
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy.ma as ma
from natsort import index_natsorted
import seaborn as sns

data = pd.read_csv("vendas.csv", sep=';', decimal=',')

# transformando coluna DataVendo em apenas ano
dataFormatada = data['DataVenda'] 
ano = [a.split('/')[-1] for a in dataFormatada]
meses = [a.split('/')[1] for a in dataFormatada]
data['Meses'] = meses
data['Ano'] = ano

def vendasPorAno():
    dadoPlot = data.groupby(["Ano"])['ValorVenda'].aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
    plt.ylabel('Total de Vendas')
    plt.xlabel('Ano')
    plt.title("Total de vendas por ano")
    plt.bar(dadoPlot['Ano'],dadoPlot['ValorVenda'])
    st.pyplot(plt.show())

    colocacao = ['1°','2°','3°','4°','5°','6°']
    dados = pd.DataFrame(dadoPlot)
    dados.insert(0, "Colocação", colocacao, allow_duplicates=False)
    st.write("Abaixo temos a tabela com o total de vendas por ano:")
    st.dataframe(dados)

def vendasPorCategoria():
    dadoPlot = data.groupby("Categoria")["ValorVenda"].aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
    plt.ylabel('Total de Vendas')
    plt.xlabel('Categoria')
    plt.title("Total de vendas por categoria")
    plt.bar(dadoPlot['Categoria'],dadoPlot['ValorVenda'])
    st.pyplot(plt.show())

    colocacao = ['1°','2°','3°','4°']
    dados = pd.DataFrame(dadoPlot)
    st.write("Abaixo temos a tabela com o total de vendas por categoria:")
    st.dataframe(dados)
    
def vendasPorCategoriaAno():
    df = data.groupby(['Categoria', 'Ano'], as_index=False)["ValorVenda"].sum()
    df = pd.DataFrame(df)
    df= df.sort_values(by='ValorVenda',ascending = False)
    df = df.pivot("Categoria", "Ano", "ValorVenda")
    df.plot.bar()
    plt.ylabel('Total de Vendas')
    plt.title("Total de vendas por categoria e por ano")
    st.pyplot()
    st.write("Abaixo temos a tabela com o total de vendas por categoria e ano:")
    st.dataframe(df)

def vendasPorAnoCategoria():
    df = data.groupby(['Ano', 'Categoria'], as_index=False)["ValorVenda"].sum()
    df = pd.DataFrame(df)
    df= df.sort_values(by='ValorVenda',ascending = False)
    df = df.pivot("Ano", "Categoria", "ValorVenda")
    df.plot.bar()
    plt.ylabel('Total de Vendas')
    plt.title("Total de vendas por ano e por categoria")
    st.pyplot()
    st.write("Abaixo temos a tabela com o total de vendas por ano e por categoria:")
    st.dataframe(df)


def vendasCategoriaMesesAno(opcao):
    if(opcao == "Todos os anos"):
        anosUnicos = data.Ano.unique()
        for ano in anosUnicos:
          dfFilter = data[(data["Ano"] == ano)]
          dfFilter = dfFilter.groupby(['Categoria', 'Meses','Ano'])["ValorVenda"].sum()
          dfFilter = pd.DataFrame(dfFilter)
          dfFilter= dfFilter.sort_values(by='ValorVenda',ascending = False)
          table = pd.pivot_table(dfFilter, values='ValorVenda', index=['Meses'],columns=['Categoria'])
          table.plot.bar()
          plt.title("Total de vendas por categoria e por meses do ano de " + ano)
          plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
          plt.ylabel('Total de Vendas')
          st.pyplot()
          st.write("Abaixo temos a tabela com o total de vendas por ano e por categoria:")
          st.dataframe(dfFilter)
    else:
        dfFilter = data[(data["Ano"] == opcao)]
        dfFilter = dfFilter.groupby(['Categoria', 'Meses','Ano'])["ValorVenda"].sum()
        dfFilter = pd.DataFrame(dfFilter)
        dfFilter= dfFilter.sort_values(by='ValorVenda',ascending = False)
        table = pd.pivot_table(dfFilter, values='ValorVenda', index=['Meses'],columns=['Categoria'])
        table.plot.bar()
        plt.title("Total de vendas por categoria e por meses do ano de " + opcao)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        plt.ylabel('Total de Vendas')
        st.pyplot()
        st.write("Abaixo temos a tabela com o total de vendas por ano e por categoria:")
        st.dataframe(dfFilter)

def produtosPorFrabricante():
    df = data.groupby(['Fabricante','Produto'])["ValorVenda"].count()
    df = pd.DataFrame(df)
    df = df.sort_values(by='ValorVenda', ascending = False)
    table = pd.pivot_table(df, values='ValorVenda', index=['Fabricante'],columns=['Produto'])
    ax = table.plot.bar(stacked=True, align='center')
    for container in ax.containers:
        plt.setp(container, width=1)
    x0, x1 = ax.get_xlim()
    ax.set_xlim(x0 -0.5, x1 + 0.5)
    plt.subplots_adjust(top=1)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.ylabel('Total de Vendas')
    plt.title("Produtos mais vendidos por fabricante")
    st.pyplot()
    st.write("Abaixo temos a tabela com os produtos mais vendidos por fabricante:")
    st.dataframe(df)
    
def vendasLojaCategoria():
    dadoPlot = data.groupby(["Categoria", "Loja"])["ValorVenda"].sum()
    dadoPlot = pd.DataFrame(dadoPlot)
    dadoPlot = dadoPlot.sort_values(by='ValorVenda',ascending = False)
    table = pd.pivot_table(dadoPlot, values='ValorVenda', index=['Loja'],columns=['Categoria'])
    table.plot.bar()
    plt.ylabel('Total de Vendas')
    plt.title("Total de vendas por loja e por categoria")
    st.pyplot()
    st.write("Abaixo temos a tabela com o total de vendas por loja e por categoria:")
    st.dataframe(dadoPlot)

def rankingProdutosPorLojaMaioresVendas(opcao1):
    if opcao1 == "No geral":
        df = data.groupby('Produto').aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
        sns.barplot(x='Produto', y="ValorVenda", data=df, order=df['Produto'])
        plt.xticks(rotation=90)
        plt.title("Ranking dos produtos com maiores vendas no geral")
        plt.ylabel('Total de Vendas')
        st.pyplot(plt.show())
        colocacao = ['1°','2°','3°','4°','5°','6°','7°','8°','9°','10°','11°','12°','13°','14°','15°','16°','17°','18°','19°']
        df = pd.DataFrame(df)
        df.insert(0, "Colocação", colocacao, allow_duplicates=False)
        st.write("Abaixo temos a tabela com dos produtos com maiores vendas:")
        st.dataframe(df)
    else:
        dfFilter = data[(data["Loja"] == opcao1)]
        dfFilter = dfFilter.groupby(['Produto','Loja']).aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
        sns.barplot(x='Produto', y="ValorVenda", data=dfFilter, order=dfFilter['Produto'])
        plt.xticks(rotation=90)
        plt.title("Ranking dos produtos com maiores vendas na loja:" + opcao1)
        plt.ylabel('Total de Vendas')
        st.pyplot(plt.show())
        dfFilter = pd.DataFrame(dfFilter)
        st.write("Abaixo temos a tabela com dos produtos com maiores vendas:")
        st.dataframe(dfFilter)

def rankingProdutosPorLojaMenoresVendas(opcao2):
    if opcao2 == "No geral":
        df = data.groupby('Produto').aggregate(np.sum).reset_index().sort_values('ValorVenda')
        sns.barplot(x='Produto', y="ValorVenda", data=df, order=df['Produto'])
        plt.xticks(rotation=90)
        plt.title("Ranking dos produtos com menores vendas no geral")
        plt.ylabel('Total de Vendas')
        st.pyplot(plt.show())
        colocacao = ['1°','2°','3°','4°','5°','6°','7°','8°','9°','10°','11°','12°','13°','14°','15°','16°','17°','18°','19°']
        df = pd.DataFrame(df)
        df.insert(0, "Colocação", colocacao, allow_duplicates=False)
        st.write("Abaixo temos a tabela com dos produtos com menores vendas:")
        st.dataframe(df)

    else:
      dfFilter = data[(data["Loja"] == opcao2)]
      dfFilter = dfFilter.groupby(['Produto','Loja']).aggregate(np.sum).reset_index().sort_values('ValorVenda')
      sns.barplot(x='Produto', y="ValorVenda", data=dfFilter, order=dfFilter['Produto'])
      plt.xticks(rotation=90)
      plt.title("Ranking dos produtos com menores vendas na loja:" + opcao2)
      plt.ylabel('Total de Vendas')
      st.pyplot(plt.show())
      dfFilter = pd.DataFrame(dfFilter)
      st.write("Abaixo temos a tabela com dos produtos com menores vendas:")
      st.dataframe(dfFilter)

def rankingProdutosRentaveisPorLoja(opcao3):
    for line in data:
        data['Rentaveis'] = data['ValorVenda'] - data['preço Custo']
        
    if opcao3 == "No geral":
        df = data.groupby('Produto').aggregate(np.sum).reset_index().sort_values('Rentaveis',ascending = False)
        sns.barplot(x='Produto', y="Rentaveis", data=df, order=df['Produto'])
        plt.xticks(rotation=90)
        plt.title("Ranking dos produtos mais rentáveis no geral")
        plt.ylabel('Mais Rentáveis')
        st.pyplot(plt.show())
        colocacao = ['1°','2°','3°','4°','5°','6°','7°','8°','9°','10°','11°','12°','13°','14°','15°','16°','17°','18°','19°']
        df = pd.DataFrame(df)
        df.insert(0, "Colocação", colocacao, allow_duplicates=False)
        st.write("Abaixo temos a tabela com dos produtos mais rentáveis por loja:")
        st.dataframe(df)
    else:
        dfFilter = data[(data["Loja"] == opcao3)]
        dfFilter = dfFilter.groupby(['Produto','Loja']).aggregate(np.sum).reset_index().sort_values('Rentaveis',ascending = False)
        sns.barplot(x='Produto', y="Rentaveis", data=dfFilter, order=dfFilter['Produto'])
        plt.xticks(rotation=90)
        plt.title("Ranking dos produtos mais rentáveis na loja:" + opcao3)
        plt.ylabel('Mais Rentáveis')
        st.pyplot(plt.show())
        df = pd.DataFrame(dfFilter)
        st.write("Abaixo temos a tabela com dos produtos mais rentáveis da loja "+opcao3)
        st.dataframe(df)
    
def rankingVendasLoja():
    df = data.groupby('Loja').aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
    sns.barplot(x='Loja', y="ValorVenda", data=df, order=df['Loja'])
    plt.xticks(rotation=90)
    plt.title("Ranking das vendas por loja")
    st.pyplot(plt.show())
    df = pd.DataFrame(df)
    colocacao = ['1°','2°','3°','4°','5°','6°','7°']
    df.insert(0, "Colocação", colocacao, allow_duplicates=False)
    st.write("Abaixo temos a tabela com o ranking de vendas por loja:")
    st.dataframe(df)

def rankingVendedoresMaioresVendas(opcao4):
    lojas = data.loc[:,['Loja']].drop_duplicates()
    for i in range(len(data)):
      data.iloc[i,10]=data.iloc[i,10][6:]

    anos = data.loc[:,['Ano']]
    anos = anos.drop_duplicates()
    if opcao4 == "Todas as lojas":
        for i in range(len(lojas)):
          dados1 = data[data['Loja'] == lojas.iloc[i,0]]
          dados1 = pd.DataFrame(dados1.groupby(['Vendedor', 'Ano'],as_index=False).ValorVenda.sum())
          df = dados1.loc[:,['Ano','Vendedor', 'ValorVenda']]
          df = df.sort_values(by=['Ano','ValorVenda'], ascending=False)
          sns.catplot(x="Ano", y="ValorVenda", hue="Vendedor", kind="bar", data=df)
          plt.title("Ranking dos vendedores com maior valor de vendas na loja " + lojas.iloc[i,0])
          st.pyplot(plt.show())
          st.write("Tabela do ranking dos vendedores com maior valor de vendas na loja " + lojas.iloc[i,0])
          st.dataframe(dados1)
    else:
        dados1 = data[data['Loja'] == opcao4]
        dados1 = pd.DataFrame(dados1.groupby(['Vendedor', 'Ano'],as_index=False).ValorVenda.sum())
        df = dados1.loc[:,['Ano','Vendedor', 'ValorVenda']]
        df = df.sort_values(by=['Ano','ValorVenda'], ascending=False)
        sns.catplot(x="Ano", y="ValorVenda", hue="Vendedor", kind="bar", data=df)
        plt.title("Ranking dos vendedores com maior valor de vendas na loja " + opcao4)
        st.pyplot(plt.show())
        st.write("Tabela do ranking dos vendedores com maior valor de vendas na loja " + opcao4)
        st.dataframe(dados1)
    
st.title("Análise gráfica da base de dados de vendas")
st.sidebar.title("Escolha a opção desejada para emitir o relatório")


if st.sidebar.button("Total de vendas por ano"):
    vendasPorAno()
if st.sidebar.button("Total de vendas por categoria"):
    vendasPorCategoria()
if st.sidebar.button("Total de vendas por categoria e ano"):
    vendasPorCategoriaAno()
if st.sidebar.button("Total de vendas por ano e categoria"):
    vendasPorAnoCategoria()
    
opcao = st.sidebar.selectbox("Total de vendas por categoria pelos meses",["Selecione o ano","2014","2015","2016","2017","2018","2019", "Todos os anos"])
if opcao != "Selecione o ano":
    vendasCategoriaMesesAno(opcao)

    
if st.sidebar.button("Produtos mais vendidos por fabricante"):
    produtosPorFrabricante()
if st.sidebar.button("Total de vendas das lojas por categoria"):
    vendasLojaCategoria()

opcao1 = st.sidebar.selectbox("Ranking dos produtos com maiores vendas por loja/geral",["Selecione a loja","R1296","BA7783","JP8825","RG7742","AL1312","GA7751","JB6325", "No geral"])
if opcao1 != "Selecione a loja":
    rankingProdutosPorLojaMaioresVendas(opcao1)

opcao2 = st.sidebar.selectbox("Ranking dos produtos com menores vendas por loja/geral",["Selecione a loja","R1296","BA7783","JP8825","RG7742","AL1312","GA7751","JB6325", "No geral"])
if opcao2 != "Selecione a loja":
    rankingProdutosPorLojaMenoresVendas(opcao2)

opcao3 = st.sidebar.selectbox("Ranking dos produtos mais rentáveis por loja/geral",["Selecione a loja","R1296","BA7783","JP8825","RG7742","AL1312","GA7751","JB6325", "No geral"])
if opcao3 != "Selecione a loja":
    rankingProdutosRentaveisPorLoja(opcao3)

if st.sidebar.button("Ranking de vendas por lojas"):
    rankingVendasLoja()

opcao4 = st.sidebar.selectbox("Ranking dos vendedores com maior valor de vendas por loja e ano",["Selecione a loja","R1296","BA7783","JP8825","RG7742","AL1312","GA7751","JB6325","Todas as lojas"])
if opcao4 != "Selecione a loja":
    rankingVendedoresMaioresVendas(opcao4)
st.set_option('deprecation.showPyplotGlobalUse', False)
