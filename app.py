import streamlit as st
import pandas as pd
from core.analyzer import analisar_projeto
from core.cost_estimator import calcular_custo_manutencao, mapear_codigo_para_infra
from core.aws_calculator import PRICES

st.set_page_config(page_title="AWS Cost Sentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ AWS Cost & Code Sentinel")
st.markdown("""
Analise repositórios **multilinguagem** e estime custos reais de infraestrutura AWS.
""")

tab1, tab2 = st.tabs(["🔍 Scanner Multi-Language", "💰 Calculadora Manual"])

with tab1:
    st.header("Análise de Repositório")
    regiao_scan = st.selectbox("Região AWS", options=list(PRICES["regions"].keys()), format_func=lambda x: PRICES["regions"][x])
    
    if st.button("Iniciar Escaneamento"):
        with st.spinner("Analisando arquivos e tecnologias..."):
            relatorio = analisar_projeto()
            
            # Métricas
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Arquivos Detectados", len(relatorio["arquivos"]))
            c2.metric("Linguagens", len(relatorio["linguagens"]))
            c3.metric("Usa Docker?", "Sim" if relatorio["usa_docker"] else "Não")
            c4.metric("Total de Linhas", relatorio["total_linhas"])

            # Mix de Linguagens
            st.subheader("📊 Mix de Tecnologias")
            lang_data = pd.DataFrame(list(relatorio["linguagens"].items()), columns=["Linguagem", "Qtd"])
            st.bar_chart(lang_data.set_index("Linguagem"))

            st.divider()

            # Recomendação
            infra = mapear_codigo_para_infra(relatorio, regiao_scan)
            st.subheader("🏗️ Arquitetura AWS Recomendada")
            col_inf_1, col_inf_2 = st.columns([2, 1])
            
            with col_inf_1:
                st.table(pd.DataFrame(infra["servicos"]))
            
            with col_inf_2:
                st.metric("Custo Mensal AWS", f"${infra['custo_total']:.2f}")
                risco = calcular_custo_manutencao(relatorio)
                st.metric("Estimativa Operacional", f"${risco:.2f}")

            with st.expander("📝 Detalhes dos Arquivos"):
                df_detalhe = pd.DataFrame(relatorio["arquivos"])
                df_detalhe.columns = ["Arquivo", "Linguagem", "Linhas", "Latência Est. (ms)"]
                st.dataframe(df_detalhe, use_container_width=True)

with tab2:
    st.header("Simulador de Custos")
    st.info("Utilize para orçamentos rápidos sem necessidade de escaneamento.")
    st.warning("Acesse a aba de Scanner para uma análise inteligente baseada no seu código.")
