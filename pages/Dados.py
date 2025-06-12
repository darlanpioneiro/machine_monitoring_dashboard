import streamlit as st
import pandas as pd

# Carregar dados
dados = pd.read_csv('smart_manufacturing_data.csv')

# Converter a coluna de timestamp para datetime
dados['timestamp'] = pd.to_datetime(dados['timestamp'])

# Função para converter o DataFrame para CSV no formato bytes
def converter_df_para_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Título da página
st.title(":green[Dados] :red[das] :blue[Máquinas] :bar_chart:")

# --------------------------------------
# Sidebar - título estilizado + filtros
# --------------------------------------
with st.sidebar:
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

    # Filtros
    todas_maquinas = st.checkbox("Selecionar todas as máquinas", value=True)  # Marcado por padrão

    if todas_maquinas:
        dados_filtrados = dados.copy()
    else:
        filtrar_multiplas = st.checkbox("Deseja filtrar mais de 1 máquina?")

        if filtrar_multiplas:
            machine_filter = st.multiselect("Selecione uma ou mais Máquinas:", dados['machine'].unique(), default=dados['machine'].unique())
            status_filter = st.multiselect("Selecione um ou mais Status da Máquina:", dados['machine_status'].unique(), default=dados['machine_status'].unique())
            anomaly_filter = st.multiselect("Selecione um ou mais Sinalizadores de Anomalia:", dados['anomaly_flag'].unique(), default=dados['anomaly_flag'].unique())

            dados_filtrados = dados[
                (dados['machine'].isin(machine_filter)) &
                (dados['machine_status'].isin(status_filter)) &
                (dados['anomaly_flag'].isin(anomaly_filter))
            ]
        else:
            machine_filter = st.selectbox("Selecione a Máquina:", dados['machine'].unique())
            status_filter = st.selectbox("Selecione o Status da Máquina:", dados['machine_status'].unique())
            anomaly_filter = st.selectbox("Selecione o Sinalizador de Anomalia:", dados['anomaly_flag'].unique())

            dados_filtrados = dados[
                (dados['machine'] == machine_filter) &
                (dados['machine_status'] == status_filter) &
                (dados['anomaly_flag'] == anomaly_filter)
            ]

    st.subheader("Filtro por Data")
    data_min = dados['timestamp'].min().date()
    data_max = dados['timestamp'].max().date()

    data_selecionada = st.slider("Selecione o intervalo de datas:", 
                                 min_value=data_min, 
                                 max_value=data_max, 
                                 value=(data_min, data_max))

    # Filtrar dados com base no intervalo de datas selecionado
    dados_filtrados = dados_filtrados[
        (dados_filtrados['timestamp'].dt.date >= data_selecionada[0]) &
        (dados_filtrados['timestamp'].dt.date <= data_selecionada[1])
    ]

# Exibir tabela interativa dos dados filtrados
st.dataframe(dados_filtrados, height=600)

# Download dos dados filtrados
csv_bytes = converter_df_para_csv(dados_filtrados)
st.download_button(
    label="Baixar dados filtrados em CSV",
    data=csv_bytes,
    file_name='dados_filtrados.csv',
    mime='text/csv'
)
