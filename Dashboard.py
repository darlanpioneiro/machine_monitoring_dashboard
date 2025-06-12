import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Configuração da página do Streamlit com layout amplo e título personalizado
st.set_page_config(layout='wide', page_title='Dashboard Monitoramento de Máquinas')

# Título colorido com emojis (Streamlit suporta markdown colorido e emojis)
st.title(":green[Dashboard] :red[Monitoramento] :blue[de Máquinas] :bar_chart:")

# *---------------------------------*
# 	Carregando arquivo de DADOS
# *---------------------------------*
dados = pd.read_csv('smart_manufacturing_data.csv')

# Converter a coluna 'timestamp' para tipo datetime para manipulação de datas
dados['timestamp'] = pd.to_datetime(dados['timestamp'])

# ---------- FILTROS NA SIDEBAR -----------

# Lógica e interface para filtros (máquina, status, anomalia e intervalo de datas)
with st.sidebar:
    # Caixinha estilizada para os filtros
    st.markdown(
        """
        <div style="
            background: linear-gradient(90deg, #4ade80, #22d3ee);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(34, 211, 238, 0.45);
            text-align: center;
            margin-bottom: 30px;
            ">
            <h1 style="
                font-family: 'Poppins', sans-serif;
                font-weight: 900;
                color: white;
                margin: 0;
                font-size: 28px;
                text-shadow: 0 0 10px rgba(255,255,255,0.8);
            ">
                📊 FILTROS
            </h1>
            <p style="
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
                color: white;
                margin-top: 5px;
                font-size: 14px;
                letter-spacing: 1.2px;
                text-transform: uppercase;
            ">Selecione os dados</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Checkbox para seleção rápida de todas as máquinas (ignorar filtros de máquina)
    todas_maquinas = st.checkbox("Selecionar todas as máquinas", value=True)  # Marcado por padrão

    if todas_maquinas:
        # Se selecionar todas as máquinas, copia todo o dataset para filtragem posterior
        dados_filtrados = dados.copy()
    else:
        # Opção entre filtro múltiplo ou filtro único
        filtrar_multiplas = st.checkbox("Deseja filtrar mais de 1 máquina?")

        if filtrar_multiplas:
            # Multiselect para máquinas, status e anomalias - permite várias seleções
            machine_filter = st.multiselect("Selecione uma ou mais Máquinas:", dados['machine'].unique(), default=dados['machine'].unique())
            status_filter = st.multiselect("Selecione um ou mais Status da Máquina:", dados['machine_status'].unique(), default=dados['machine_status'].unique())
            anomaly_filter = st.multiselect("Selecione um ou mais Sinalizadores de Anomalia:", dados['anomaly_flag'].unique(), default=dados['anomaly_flag'].unique())

            # Aplicar filtros múltiplos no DataFrame original
            dados_filtrados = dados[
                (dados['machine'].isin(machine_filter)) &
                (dados['machine_status'].isin(status_filter)) &
                (dados['anomaly_flag'].isin(anomaly_filter))
            ]
        else:
            # Selecione única opção para cada filtro com selectbox
            machine_filter = st.selectbox("Selecione a Máquina:", dados['machine'].unique())
            status_filter = st.selectbox("Selecione o Status da Máquina:", dados['machine_status'].unique())
            anomaly_filter = st.selectbox("Selecione o Sinalizador de Anomalia:", dados['anomaly_flag'].unique())

            # Dados filtrados conforme seleções únicas
            dados_filtrados = dados[
                (dados['machine'] == machine_filter) &
                (dados['machine_status'] == status_filter) &
                (dados['anomaly_flag'] == anomaly_filter)
            ]

    # ----------------------- Filtro de intervalo de datas ----------------------
    st.subheader("Filtro por Data")
    # Determinar as datas mínima e máxima disponíveis no dataset
    data_min = dados['timestamp'].min().date()
    data_max = dados['timestamp'].max().date()

    # Slider para seleção do intervalo de datas pelo usuário
    data_selecionada = st.slider("Selecione o intervalo de datas:",
                                 min_value=data_min,
                                 max_value=data_max,
                                 value=(data_min, data_max))

    # Aplicar filtro no intervalo de datas selecionado ao dataset já filtrado
    dados_filtrados = dados_filtrados[
        (dados_filtrados['timestamp'].dt.date >= data_selecionada[0]) &
        (dados_filtrados['timestamp'].dt.date <= data_selecionada[1])
    ]

# ---------- ESTRUTURA PRINCIPAL DO DASHBOARD COM ABAS -----------

# Criar abas para separar visualmente diferentes tipos de análises e gráficos
abas = st.tabs(["Gráficos", "Análise", "Matriz de Correlação", "Média por Sensores"])

with abas[0]:
    st.header("Gráficos de Monitoramento de Máquinas")

    # Gráfico 1: Temperatura média por máquina (barras)
    fig1 = px.bar(
        dados_filtrados.groupby('machine')['temperature'].mean().reset_index(),
        x='machine',
        y='temperature',
        title='Temperatura Média por Máquina'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Vibração média por máquina (barras)
    fig2 = px.bar(
        dados_filtrados.groupby('machine')['vibration'].mean().reset_index(),
        x='machine',
        y='vibration',
        title='Vibração Média por Máquina'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Consumo total de energia por máquina (barras)
    fig3 = px.bar(
        dados_filtrados.groupby('machine')['energy_consumption'].sum().reset_index(),
        x='machine',
        y='energy_consumption',
        title='Consumo Total de Energia por Máquina'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Anomalias por tipo de falha (histograma colorido)
    fig4 = px.histogram(
        dados_filtrados,
        x='failure_type',
        color='anomaly_flag',
        title='Anomalias por Tipo de Falha'
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Distribuição do status das máquinas (pizza)
    fig5 = px.pie(
        dados_filtrados,
        names='machine_status',
        title='Distribuição do Status das Máquinas'
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Gráfico 6: Temperatura vs Vibração (dispersão colorida)
    fig6 = px.scatter(
        dados_filtrados,
        x='temperature',
        y='vibration',
        color='anomaly_flag',
        title='Temperatura vs Vibração'
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Gráfico 7: Umidade média por máquina (barras)
    fig7 = px.bar(
        dados_filtrados.groupby('machine')['humidity'].mean().reset_index(),
        x='machine',
        y='humidity',
        title='Umidade Média por Máquina'
    )
    st.plotly_chart(fig7, use_container_width=True)

    # Gráfico 8: Pressão média por máquina (barras)
    fig8 = px.bar(
        dados_filtrados.groupby('machine')['pressure'].mean().reset_index(),
        x='machine',
        y='pressure',
        title='Pressão Média por Máquina'
    )
    st.plotly_chart(fig8, use_container_width=True)

    # Gráfico 9: Evolução temporal da temperatura média geral (linha)
    temp_tempo = dados_filtrados.groupby('timestamp')['temperature'].mean().reset_index()
    fig9 = px.line(
        temp_tempo,
        x='timestamp',
        y='temperature',
        title='Evolução Temporal da Temperatura Média'
    )
    st.plotly_chart(fig9, use_container_width=True)

    # Gráfico 10: Boxplot da vibração por máquina
    fig10 = px.box(
        dados_filtrados,
        x='machine',
        y='vibration',
        title='Distribuição da Vibração por Máquina'
    )
    st.plotly_chart(fig10, use_container_width=True)

    # Gráfico 11: Dispersão 3D temperatura, vibração e consumo de energia
    fig11 = px.scatter_3d(
        dados_filtrados,
        x='temperature',
        y='vibration',
        z='energy_consumption',
        color='machine_status',
        opacity=0.7,
        title='Gráfico 3D: Temperatura, Vibração e Consumo de Energia'
    )
    st.plotly_chart(fig11, use_container_width=True)

    # Gráfico 12: Heatmap temporal da temperatura média diária por máquina
    dados_filtrados['date'] = dados_filtrados['timestamp'].dt.date
    heatmap_data = dados_filtrados.groupby(['machine', 'date'])['temperature'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='machine', columns='date', values='temperature')
    plt.figure(figsize=(12, 7))
    plt.imshow(heatmap_pivot, cmap='coolwarm', aspect='auto')
    plt.colorbar(label='Temperatura Média')
    plt.title('Heatmap - Temperatura Média Diária por Máquina')
    plt.xlabel('Data')
    plt.ylabel('Máquina')
    st.pyplot(plt)
    plt.close()  # Fecha figura para evitar sobreposição em execuções futuras

with abas[1]:
    st.header("Análise de Manutenção")

    # Mapear valores "Yes" e "no" da coluna maintenance_required para 1 e 0
    dados_filtrados['maintenance_required'] = dados_filtrados['maintenance_required'].map({'Yes': 1, 'no': 0})

    # Filtrar máquinas que precisam de manutenção (valor 1)
    manutencao_necessaria = dados_filtrados[dados_filtrados['maintenance_required'] == 1]
    num_machines_needing_maintenance = manutencao_necessaria['machine'].nunique()

    # Mostrar número de máquinas que requerem manutenção
    st.markdown(f"### Número de máquinas que requerem manutenção: {num_machines_needing_maintenance}")

    # Exibir lista das máquinas que precisam de manutenção
    maquinas_df = pd.DataFrame(manutencao_necessaria['machine'].unique(), columns=['Máquinas que precisam de manutenção'])
    st.dataframe(maquinas_df, height=200)

    # Gráfico da distribuição do risco de inatividade (histograma)
    fig_risco = px.histogram(
        dados_filtrados,
        x='downtime_risk',
        title='Distribuição do Risco de Inatividade'
    )
    st.plotly_chart(fig_risco, use_container_width=True)

    # Gráfico 13: Violino da pressão por status da máquina
    fig13 = px.violin(
        dados_filtrados,
        y='pressure',
        x='machine_status',
        color='machine_status',
        box=True,
        points='all',
        title='Distribuição da Pressão por Status da Máquina'
    )
    st.plotly_chart(fig13, use_container_width=True)

    # Gráfico 14: Barras agrupadas da média de temperatura e vibração por status da máquina
    media_status = dados_filtrados.groupby('machine_status')[['temperature', 'vibration']].mean().reset_index()
    fig14 = px.bar(
        media_status,
        x='machine_status',
        y=['temperature', 'vibration'],
        barmode='group',
        title='Média de Temperatura e Vibração por Status da Máquina'
    )
    st.plotly_chart(fig14, use_container_width=True)

with abas[2]:
    st.header("Matriz de Correlação")

    # Selecionar colunas numéricas para correlação
    colunas_numericas = dados_filtrados.select_dtypes(include=['float64', 'int64'])
    correlacao = colunas_numericas.corr()

    # Plotar matriz de correlação com matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(correlacao, cmap='coolwarm', aspect='auto')
    plt.colorbar(label='Correlação')
    plt.title("Matriz de Correlação entre Features")
    st.pyplot(plt)
    plt.close()

with abas[3]:
    st.header("Média por Sensores")

    # Definir colunas correspondentes aos sensores para cálculo de média
    colunas_sensores = ['temperature', 'vibration', 'humidity', 'pressure', 'energy_consumption']

    # Calcular a média dos sensores por máquina
    medias_por_maquina = dados_filtrados.groupby('machine')[colunas_sensores].mean().reset_index()

    # Exibir tabela formatada com 2 casas decimais para as médias dos sensores
    st.dataframe(
        medias_por_maquina.style.format({col: '{:.2f}' for col in colunas_sensores}),
        height=600
    )

# Rodapé com o nome do acadêmico
st.markdown("<br><br><hr><p style='text-align: center;'>Desenvolvido por: <strong>Darlan Pedro Caron Piaia</strong></p>", unsafe_allow_html=True)
