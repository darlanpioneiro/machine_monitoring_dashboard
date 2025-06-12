import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(layout='wide', page_title='Dashboard Monitoramento de Máquinas')
# Exibe os títulos com cores e ícone gráfico
st.title(":green[Dashboard] :red[Monitoramento] :blue[de Máquinas] :bar_chart:")

# *---------------------------------*
# 	Carregando arquivo de DADOS
# *---------------------------------*
dados = pd.read_csv('smart_manufacturing_data.csv')

# --------------------
#       Funções e estrutura do dashboard com abas
# --------------------

# Criar abas para Gráficos, Análise, Matriz de Correlação e Média por Sensores
abas = st.tabs(["Gráficos", "Análise", "Matriz de Correlação", "Média por Sensores"])

with abas[0]:
    st.header("Gráficos de Monitoramento de Máquinas")

    # Gráfico 1: Temperatura média por máquina
    fig1 = px.bar(dados.groupby('machine')['temperature'].mean().reset_index(),
                  x='machine', y='temperature',
                  title='Temperatura Média por Máquina')
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Vibração média por máquina
    fig2 = px.bar(dados.groupby('machine')['vibration'].mean().reset_index(),
                  x='machine', y='vibration',
                  title='Vibração Média por Máquina')
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Consumo total de energia por máquina
    fig3 = px.bar(dados.groupby('machine')['energy_consumption'].sum().reset_index(),
                  x='machine', y='energy_consumption',
                  title='Consumo Total de Energia por Máquina')
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Anomalias por tipo de falha
    fig4 = px.histogram(dados, x='failure_type', color='anomaly_flag',
                        title='Anomalias por Tipo de Falha')
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Status da máquina
    fig5 = px.pie(dados, names='machine_status', title='Distribuição do Status das Máquinas')
    st.plotly_chart(fig5, use_container_width=True)

    # Gráfico 6: Temperatura vs Vibração
    fig6 = px.scatter(dados, x='temperature', y='vibration',
                      color='anomaly_flag',
                      title='Temperatura vs Vibração')
    st.plotly_chart(fig6, use_container_width=True)

    # Gráfico 7: Umidade média por máquina
    fig7 = px.bar(dados.groupby('machine')['humidity'].mean().reset_index(),
                  x='machine', y='humidity',
                  title='Umidade Média por Máquina')
    st.plotly_chart(fig7, use_container_width=True)

    # Gráfico 8: Pressão média por máquina
    fig8 = px.bar(dados.groupby('machine')['pressure'].mean().reset_index(),
                  x='machine', y='pressure',
                  title='Pressão Média por Máquina')
    st.plotly_chart(fig8, use_container_width=True)

    # Gráfico 9: Evolução temporal da Temperatura média geral
    dados['timestamp'] = pd.to_datetime(dados['timestamp'])
    temp_tempo = dados.groupby('timestamp')['temperature'].mean().reset_index()
    fig9 = px.line(temp_tempo, x='timestamp', y='temperature', title='Evolução Temporal da Temperatura Média')
    st.plotly_chart(fig9, use_container_width=True)

    # Gráfico 10: Boxplot da Vibração por máquina
    fig10 = px.box(dados, x='machine', y='vibration', title='Distribuição da Vibração por Máquina')
    st.plotly_chart(fig10, use_container_width=True)

    # Gráfico 11: Gráfico de dispersão 3D (temperatura, vibração, energia_consumption)
    fig11 = px.scatter_3d(dados, x='temperature', y='vibration', z='energy_consumption',
                          color='machine_status', opacity=0.7,
                          title='Gráfico 3D: Temperatura, Vibração e Consumo de Energia')
    st.plotly_chart(fig11, use_container_width=True)

    # Gráfico 12: Heatmap temporal da temperatura por máquina
    dados['date'] = dados['timestamp'].dt.date
    heatmap_data = dados.groupby(['machine', 'date'])['temperature'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='machine', columns='date', values='temperature')
    plt.figure(figsize=(12, 7))
    sns.heatmap(heatmap_pivot, cmap='coolwarm', cbar_kws={'label': 'Temperatura Média'})
    plt.title('Heatmap - Temperatura Média Diária por Máquina')
    plt.xlabel('Data')
    plt.ylabel('Máquina')
    st.pyplot(plt)

with abas[1]:
    st.header("Análise de Manutenção")

    # Mapear valores "Yes" e "no" para 1 e 0 para a coluna maintenance_required
    dados['maintenance_required'] = dados['maintenance_required'].map({'Yes': 1, 'no': 0})

    # Filtrar dados para máquinas que precisam de manutenção
    manutencao_necessaria = dados[dados['maintenance_required'] == 1]
    num_machines_needing_maintenance = manutencao_necessaria['machine'].nunique()

    # Exibir número de máquinas que requerem manutenção
    st.markdown(f"### Número de máquinas que requerem manutenção: {num_machines_needing_maintenance}")

    # Criar tabela para exibir as máquinas que precisam de manutenção
    maquinas_df = pd.DataFrame(manutencao_necessaria['machine'].unique(), columns=['Máquinas que precisam de manutenção'])
    st.dataframe(maquinas_df, height=200)

    # Gráfico da distribuição do risco de inatividade
    fig_risco = px.histogram(dados, x='downtime_risk',
                             title='Distribuição do Risco de Inatividade')
    st.plotly_chart(fig_risco, use_container_width=True)

    # Gráfico 13: Gráfico de violino da pressão por status da máquina
    fig13 = px.violin(dados, y='pressure', x='machine_status', color='machine_status',
                      box=True, points='all', title='Distribuição da Pressão por Status da Máquina')
    st.plotly_chart(fig13, use_container_width=True)

    # Gráfico 14: Gráfico de barras agrupadas para média de temperatura e vibração por status
    media_status = dados.groupby('machine_status')[['temperature', 'vibration']].mean().reset_index()
    fig14 = px.bar(media_status, x='machine_status', y=['temperature', 'vibration'], barmode='group',
                  title='Média de Temperatura e Vibração por Status da Máquina')
    st.plotly_chart(fig14, use_container_width=True)

with abas[2]:
    st.header("Matriz de Correlação")

    # Seleciona apenas colunas numéricas para calcular correlação
    colunas_numericas = dados.select_dtypes(include=['float64', 'int64'])
    correlacao = colunas_numericas.corr()

    # Criar heatmap com seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlacao, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title("Matriz de Correlação entre Features")
    st.pyplot(plt)

with abas[3]:
    st.header("Média por Sensores")

    # Definir colunas de sensores para média
    colunas_sensores = ['temperature', 'vibration', 'humidity', 'pressure', 'energy_consumption']

    # Calcular médias por máquina
    medias_por_maquina = dados.groupby('machine')[colunas_sensores].mean().reset_index()

    # Exibir tabela com formatação para 2 casas decimais
    st.dataframe(medias_por_maquina.style.format({col: '{:.2f}' for col in colunas_sensores}), height=600)