import streamlit as st
import pandas as pd
from core.analyzer import analisar_projeto
from core.cost_estimator import calcular_custo_manutencao, mapear_codigo_para_infra
from core.aws_calculator import PRICES

st.set_page_config(page_title="AWS Cost Sentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ AWS Cost & Code Sentinel")
st.markdown("""
Análise técnica de código e estimativa financeira de infraestrutura AWS em um só lugar.
""")

tab1, tab2 = st.tabs(["🔍 Análise de Repositório", "💰 Calculadora Manual"])

with tab1:
    st.header("Scanner de Projeto")
    regiao_scan = st.selectbox("Região AWS", options=list(PRICES["regions"].keys()), format_func=lambda x: PRICES["regions"][x])
    
    if st.button("Iniciar Análise do Código"):
        with st.spinner("Escaneando árvore sintática e calculando latência..."):
            relatorio = analisar_projeto()
            
            # Métricas de Cabeçalho
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Arquivos", len(relatorio["arquivos"]))
            c2.metric("Linhas de Código", relatorio["total_linhas"])
            c3.metric("Usa Banco de Dados", "Sim" if relatorio["usa_db"] else "Não")
            lat_media = relatorio["latencia_total_ms"] / max(len(relatorio["arquivos"]), 1)
            c4.metric("Latência Média", f"{lat_media:.0f} ms")

            st.divider()

            infra = mapear_codigo_para_infra(relatorio, regiao_scan)
            
            st.subheader("🏗️ Infraestrutura Recomendada")
            col_infra_1, col_infra_2 = st.columns([2, 1])
            
            with col_infra_1:
                df_infra = pd.DataFrame(infra["servicos"])
                st.table(df_infra)
            
            with col_infra_2:
                st.metric("Custo Mensal AWS", f"${infra['custo_total']:.2f}")
                debito = calcular_custo_manutencao(relatorio)
                st.metric("Risco Operacional", f"${debito:.2f}")

            with st.expander("📊 Detalhamento Técnico por Arquivo"):
                df_files = pd.DataFrame(relatorio["arquivos"])
                # Renomeando para ficar mais profissional
                df_files.columns = ["Nome do Arquivo", "Linhas", "Complexidade", "Latência Estimada (ms)"]
                st.dataframe(df_files.sort_values(by="Latência Estimada (ms)", ascending=False), use_container_width=True)

with tab2:
    st.header("Simulador de Custos Manual")
    st.info("Utilize esta aba para orçamentos rápidos sem necessidade de código.")
    # ... (Calculadora manual mantida conforme versão anterior)
    st.warning("Esta aba está em modo simplificado. Use a 'Análise de Repositório' para dados reais.")
