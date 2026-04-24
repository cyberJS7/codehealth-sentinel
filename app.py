import streamlit as st
import pandas as pd
from core.analyzer import analisar_projeto
from core.cost_estimator import calcular_custo_manutencao, estimar_infra_aws

st.set_page_config(page_title="CodeHealth Sentinel", page_icon="🛡️")

st.title("🛡️ CodeHealth Sentinel")
st.markdown("Analise a saúde técnica e financeira do seu repositório.")

if st.button("Iniciar Escaneamento"):
    resultados = analisar_projeto()
    df = pd.DataFrame(resultados)
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Arquivos Analisados", len(resultados))
    col2.metric("Débito Técnico", f"${calcular_custo_manutencao(resultados)}")
    col3.metric("Custo Infra (AWS)", f"${estimar_infra_aws(len(resultados))}")
    
    # Gráfico de Complexidade
    st.subheader("Análise por Arquivo")
    st.bar_chart(df.set_index("arquivo"))
    
    st.table(df)