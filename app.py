import streamlit as st
import pandas as pd
from core.analyzer import analisar_projeto
from core.cost_estimator import calcular_custo_manutencao, mapear_codigo_para_infra
from core.aws_calculator import (
    PRICES, calculate_ec2_cost, calculate_s3_cost, 
    calculate_rds_cost, calculate_lambda_cost
)

st.set_page_config(page_title="AWS Cost Sentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ AWS Cost & Code Sentinel")
st.markdown("""
Analise repositórios **multilinguagem** para estimativa automática ou utilize a **calculadora manual** para simulações personalizadas.
""")

tab1, tab2 = st.tabs(["🔍 Scanner de Repositório", "💰 Calculadora Manual"])

with tab1:
    st.header("Análise Inteligente de Código")
    st.write("O scanner identifica tecnologias, latência e sugere a arquitetura AWS ideal.")
    regiao_scan = st.selectbox("Região AWS para Análise", options=list(PRICES["regions"].keys()), format_func=lambda x: PRICES["regions"][x], key="scan_reg")
    
    if st.button("Iniciar Escaneamento Completo"):
        with st.spinner("Analisando arquivos e mapeando arquitetura..."):
            relatorio = analisar_projeto()
            
            # Métricas Principais
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Arquivos", len(relatorio["arquivos"]))
            c2.metric("Linguagens", len(relatorio["linguagens"]))
            c3.metric("Docker Detectado", "Sim" if relatorio["usa_docker"] else "Não")
            c4.metric("Linhas Totais", relatorio["total_linhas"])

            # Gráfico de Tecnologias
            st.subheader("📊 Distribuição de Tecnologias")
            lang_data = pd.DataFrame(list(relatorio["linguagens"].items()), columns=["Linguagem", "Qtd"])
            st.bar_chart(lang_data.set_index("Linguagem"))

            st.divider()

            # Recomendação de Infraestrutura
            infra = mapear_codigo_para_infra(relatorio, regiao_scan)
            st.subheader("🏗️ Arquitetura AWS Recomendada")
            col_inf_1, col_inf_2 = st.columns([2, 1])
            
            with col_inf_1:
                st.table(pd.DataFrame(infra["servicos"]))
            
            with col_inf_2:
                st.metric("Custo Mensal AWS", f"${infra['custo_total']:.2f}")
                risco = calcular_custo_manutencao(relatorio)
                st.metric("Estimativa Operacional", f"${risco:.2f}")

            with st.expander("📝 Detalhamento por Arquivo"):
                df_detalhe = pd.DataFrame(relatorio["arquivos"])
                df_detalhe.columns = ["Arquivo", "Linguagem", "Linhas", "Latência Est. (ms)"]
                st.dataframe(df_detalhe.sort_values(by="Latência Est. (ms)", ascending=False), use_container_width=True)

with tab2:
    st.header("Simulador de Custos AWS")
    st.write("Configure manualmente os recursos para obter um orçamento detalhado.")
    
    reg_man = st.selectbox("Selecione a Região", options=list(PRICES["regions"].keys()), format_func=lambda x: PRICES["regions"][x], key="manual_reg")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖥️ Compute (EC2)")
        ec2_type = st.selectbox("Instância EC2", options=list(PRICES["ec2"].keys()))
        ec2_count = st.number_input("Qtd de Instâncias", min_value=0, value=1)
        ec2_cost = calculate_ec2_cost(ec2_type, reg_man) * ec2_count
        st.info(f"Subtotal EC2: ${ec2_cost:.2f}")

        st.subheader("💾 Storage (S3)")
        s3_gb = st.number_input("Armazenamento (GB)", min_value=0, value=100)
        s3_class = st.selectbox("Classe S3", options=list(PRICES["s3"].keys()))
        s3_cost = calculate_s3_cost(s3_gb, s3_class, reg_man)
        st.info(f"Subtotal S3: ${s3_cost:.2f}")

    with col2:
        st.subheader("🗄️ Database (RDS)")
        rds_type = st.selectbox("Instância RDS", options=list(PRICES["rds"].keys()))
        rds_count = st.number_input("Qtd de DBs", min_value=0, value=0)
        rds_cost = calculate_rds_cost(rds_type, reg_man) * rds_count
        st.info(f"Subtotal RDS: ${rds_cost:.2f}")

        st.subheader("⚡ Serverless (Lambda)")
        l_req = st.number_input("Requisições mensais", min_value=0, value=1000000, step=100000)
        l_dur = st.number_input("Duração média (ms)", min_value=1, value=200)
        l_mem = st.selectbox("Memória Alocada (MB)", options=[128, 512, 1024, 2048], index=1)
        lambda_cost = calculate_lambda_cost(l_req, l_dur, l_mem)
        st.info(f"Subtotal Lambda: ${lambda_cost:.2f}")

    st.divider()
    
    total_manual = ec2_cost + s3_cost + rds_cost + lambda_cost
    
    m1, m2 = st.columns(2)
    m1.metric("CUSTO TOTAL ESTIMADO", f"${total_manual:.2f} / mês")
    
    if st.button("Gerar Relatório em Tabela"):
        data = {
            "Recurso": ["EC2", "S3", "RDS", "Lambda", "TOTAL"],
            "Custo Mensal (USD)": [ec2_cost, s3_cost, rds_cost, lambda_cost, total_manual]
        }
        st.table(pd.DataFrame(data))
        st.success("Cálculo realizado com sucesso baseando-se nos preços reais da AWS.")
