import streamlit as st
import pandas as pd

# Carregar dados
dados = pd.read_csv('smart_manufacturing_data.csv')

# Função para converter o DataFrame para CSV no formato bytes
def converter_df_para_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Título da página
st.title(":green[Dados] :red[das] :blue[Máquinas] :bar_chart:")

# Checkbox para selecionar todas as máquinas
todas_maquinas = st.checkbox("Selecionar todas as máquinas")

if todas_maquinas:
    # Se todas as máquinas forem selecionadas, não exibe os outros filtros
    dados_filtrados = dados
else:
    # Checkbox para permitir filtro com múltiplas máquinas
    filtrar_multiplas = st.checkbox("Deseja filtrar mais de 1 máquina?")

    if filtrar_multiplas:
        # Filtros que permitem múltiplas seleções
        machine_filter = st.multiselect("Selecione uma ou mais Máquinas:", dados['machine'].unique(), default=dados['machine'].unique()[0])
        status_filter = st.multiselect("Selecione um ou mais Status da Máquina:", dados['machine_status'].unique(), default=dados['machine_status'].unique())
        anomaly_filter = st.multiselect("Selecione um ou mais Sinalizadores de Anomalia:", dados['anomaly_flag'].unique(), default=dados['anomaly_flag'].unique())

        # Aplicar filtros considerando múltiplas opções
        dados_filtrados = dados[
            (dados['machine'].isin(machine_filter)) &
            (dados['machine_status'].isin(status_filter)) &
            (dados['anomaly_flag'].isin(anomaly_filter))
        ]
    else:
        # Filtros para seleção única
        machine_filter = st.selectbox("Selecione a Máquina:", dados['machine'].unique())
        status_filter = st.selectbox("Selecione o Status da Máquina:", dados['machine_status'].unique())
        anomaly_filter = st.selectbox("Selecione o Sinalizador de Anomalia:", dados['anomaly_flag'].unique())

        # Aplicar filtros com seleção única
        dados_filtrados = dados[
            (dados['machine'] == machine_filter) &
            (dados['machine_status'] == status_filter) &
            (dados['anomaly_flag'] == anomaly_filter)
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
