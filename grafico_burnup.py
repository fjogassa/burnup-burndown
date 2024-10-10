import streamlit as st
import plotly.graph_objects as go

"""
A estrutura necessária para geração do gráfico é um dataframe com as colunas
{
Data: [],
Planejado: [],
Concluído: []
}
Data:
- Os dias (dia a dia útil) do decorrer do prazo
Planejado:
- Onde o planejado será a quantidade total (do total para o saldo), reduzindo dia após dia e com base na "Data"
Concluído:
- Quantidade de itens (saldo) concluído dia após dia, com base na "Data" 
"""

def gerarGraficoBurnup(df_arquivo):
    st.header('Gráfico de Burnup')

    # Criar uma nova instância de Figure
    fig = go.Figure()

    # Adicionar os traces
    fig.add_trace(go.Scatter(
        x=df_arquivo['Data'],
        y=df_arquivo['Planejado'],
        mode='lines+markers',
        name='Planejados',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=df_arquivo['Data'],
        y=df_arquivo['Concluído'],
        mode='lines+markers',
        name='Concluídos',
        line=dict(color='green')
    ))

    # Forçar a renderização correta no Streamlit
    st.plotly_chart(fig, use_container_width=True)
