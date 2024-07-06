# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:43:28 2024

@author: GarbiG
"""

##### imports #####

import streamlit as st
import requests
import pandas as pd
import time

##### functions #####

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso', icon='✅')
    time.sleep(5)
    sucesso.empty()


##### code #####

st.title('DADOS BRUTOS')
url = 'https://labdados.com/produtos'

response = requests.get(url, verify=False)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))
    
st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do Produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())

with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

with st.sidebar.expander('Preço do frete'):
    frete = st.slider('Selecione o Frete', 0, 220, (0,220))

with st.sidebar.expander('Categoria do Produto'):
    cat_produtos = st.multiselect('Selecione a Categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o Vendedor', dados['Vendedor'].unique(), dados['Vendedor'].unique())

with st.sidebar.expander('Local da Compra'):
    local = st.multiselect('Selecione o Estado', dados['Local da compra'].unique(), dados['Local da compra'].unique())

with st.sidebar.expander('Avaliação Cliente'):
    avaliacao = st.slider('Selecione a Nota', 1, 5, (1,5))

with st.sidebar.expander('Tipo de pagamento'):
    tipo_pgto = st.multiselect('Selecione o tipo de pgto', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

with st.sidebar.expander('Parcelas'):
    qtd_parcelas = st.slider('Selecione o Número de Parcelas', 1, 24, (1,24))

query1 = '''
            Produto in @produtos and \
            @preco[0] <= Preço <= @preco[1] and \
            @data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''
query2 = '''
            @frete[0] <= Frete <= @frete[1] and \
            `Categoria do Produto` in @cat_produtos and \
            Vendedor in @vendedor
'''
query3 = '''
            `Local da compra` in @local and \
            @avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and \
            `Tipo de pagamento` in @tipo_pgto and \
            @qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

dados_filtrados = dados.query(query1)
dados_filtrados = dados_filtrados.query(query2)
dados_filtrados = dados_filtrados.query(query3)
dados_filtrados = dados_filtrados[colunas]
st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]} colunas]')

st.markdown('Escreva o nome do arquivo:')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Download (csv)', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)    
