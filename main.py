# coding=cp1252
import pandas as pd
import streamlit as st
from datetime import date

from grafico_burnup import gerarGraficoBurnup

st.set_page_config(page_title="Burnup/Burndown", layout="wide", page_icon=":bar_chart:", initial_sidebar_state="expanded")

df_arquivo = pd.read_csv('./files/STC-RHU.csv', sep=',', decimal='.')

def getSprints(arquivo):
    dfsprint = pd.DataFrame(data=arquivo['Sprint'], columns=['Sprint'])
    dfresultado = pd.DataFrame(columns=['Sprint'])
    dfsprint.dropna(inplace=True)
    dfresultado['Sprint'] = dfsprint['Sprint'].sort_values().unique()
    dfresultado['Sprint'] = dfresultado['Sprint'].astype('int')
    return dfresultado

def configurarDataFrameGrafico(filtro_sprint, filtro_data_inicio, filtro_quantidade_dias_sprint):
    if filtro_data_inicio is None:
        return None

    if int(filtro_quantidade_dias_sprint) <= 0:
        return None

    # Crie uma lista de 10 dias úteis
    datas_uteis = pd.bdate_range(start=filtro_data_inicio, periods=filtro_quantidade_dias_sprint)
    # Crie um DataFrame a partir da lista de datas
    df_diasuteis = pd.DataFrame(datas_uteis, columns=['Data'])
    df_diasuteis.reset_index()
    # Frame com os dados filtrados por sprint e a data que foi para Code Review
    df_sprint = df_arquivo.loc[df_arquivo['Sprint'] == filtro_sprint, ['id', 'Sprint', 'Code review']]
    df_sprint['Code review'] = df_sprint['Code review'].apply(lambda x: pd.to_datetime(x))
    # Frame que será utilizado no gráfico
    colunas = {
        'Data': 'object',
        'Planejado': 'float64',
        'Concluído': 'float64'
    }
    df_grafico = pd.DataFrame(columns=colunas.keys()).astype(colunas)
    quantidade_dias_sprint = len(df_diasuteis)
    quantidade_total_sprint = len(df_sprint)
    meta_diaria_sprint = round(quantidade_total_sprint/quantidade_dias_sprint)
    quantidade_total_por_dia = 0
    for index, valor in df_diasuteis.iterrows():
        df_grafico.loc[index, 'Data'] = pd.to_datetime(valor.values[0]).strftime('%Y-%m-%d')
        # Buscar os itens que foram concluídos na data (valor)
        quantidade_por_dia = len(df_sprint.loc[df_sprint['Code review'].eq(valor.values[0])])
        quantidade_total_por_dia += quantidade_por_dia
        df_grafico.loc[index, 'Planejado'] = meta_diaria_sprint * index
        df_grafico.loc[index, 'Concluído'] = quantidade_total_por_dia

    return df_grafico

with st.sidebar:
    filtro_sprint = st.selectbox('Sprint que deseja avaliar', getSprints(df_arquivo))
    filtro_data_inicio = st.date_input('Data de início da sprint selecionada', date.today())
    filtro_quantidade_dias_da_sprint = st.number_input('Quantos dias úteis a sprint possui', min_value=0, value=10)

df = configurarDataFrameGrafico(filtro_sprint, filtro_data_inicio, filtro_quantidade_dias_da_sprint)
if df is not None:
    gerarGraficoBurnup(df)

    st.header('Tickets da sprint')
    df_table = df_arquivo[df_arquivo['Sprint'] == filtro_sprint][['id','name','Code review','Type','Assignee']].sort_values(by='Code review')
    # st.table(df_table)
    st.data_editor(
        df_table,
        disabled=['id','name','Type','Assignee'],
        use_container_width=True,
        hide_index=True
    )