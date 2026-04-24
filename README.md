# AWS Cost & Code Sentinel 🛡️☁️

**AWS Cost & Code Sentinel** é uma solução avançada de FinOps (Financial Operations) projetada para integrar análise técnica de repositórios multilinguagem com planejamento orçamentário de infraestrutura AWS.

A ferramenta realiza uma análise estática profunda (AST para Python e Padrões Heurísticos para outras linguagens) para identificar tecnologias, dependências e requisitos de infraestrutura, traduzindo métricas de código em custos reais de nuvem.

---

## 🎯 Objetivo

O projeto preenche a lacuna entre o desenvolvimento de software e a arquitetura de nuvem. Ao escanear um repositório, o sistema identifica automaticamente o perfil tecnológico e recomenda a infraestrutura mais eficiente (Serverless, Containers ou Servidores Dedicados), calculando o impacto financeiro baseado em preços reais da AWS.

## 🚀 Funcionalidades Principais

### 1. Scanner Multilinguagem de Infraestrutura
- **Suporte Poliglota**: Detecção automática de **Python, JavaScript, TypeScript, Java, Go, C++, PHP, Ruby e SQL**.
- **Cloud Native & Docker**: Identifica arquivos `Dockerfile` e recomenda automaticamente arquiteturas baseadas em **AWS Fargate** ou **EKS**.
- **Análise de Dependências**: Detecta bibliotecas de bancos de dados, frameworks web e pacotes de processamento pesado (Data Science/ML).
- **Mix de Tecnologias**: Visualização gráfica da distribuição de linguagens no repositório.

### 2. Motor de Precificação Real (FinOps)
- **Cálculo por Região**: Suporte a preços reais para **São Paulo (sa-east-1)**, **N. Virginia (us-east-1)** e **Ireland (eu-west-1)**.
- **Modelagem de Custo de Compute**:
    - **AWS Lambda**: Calculado via latência média detectada no código e volume de requisições.
    - **Amazon EC2**: Recomendado para cargas constantes ou processamento intensivo.
    - **AWS Fargate**: Recomendado para aplicações containerizadas.
- **Amazon RDS**: Estimativa automática ao detectar drivers de conexão SQL.

### 3. Métricas de Performance e Manutenção
- **Estimativa de Latência**: Modelo heurístico que calcula o tempo de execução (ms) baseado na complexidade e volume de cada arquivo.
- **Risco Operacional**: Estimativa de custo de manutenção baseada na densidade de linhas e complexidade técnica.

---

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.10+
- **Frontend**: Streamlit (Dashboard Interativo)
- **Análise Estática**: AST (Abstract Syntax Trees) & Regex Heuristics.
- **Visualização**: Pandas & Streamlit Charts.

---

## ⚙️ Instalação e Uso

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/aws-cost-sentinel.git
   cd aws-cost-sentinel
   ```

2. **Configurar Ambiente Virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar Aplicação**:
   ```bash
   streamlit run app.py
   ```

---

## 📝 Licença

Este projeto está sob a licença MIT. 

---
**Desenvolvido como demonstração de competências em Arquitetura Cloud, FinOps e Engenharia de Software.**
