# AWS Cost & Code Sentinel 🛡️☁️

**AWS Cost & Code Sentinel** é uma solução avançada de FinOps projetada para integrar análise técnica de repositórios multilinguagem com planejamento estratégico de infraestrutura AWS.

A ferramenta realiza uma análise estática profunda para identificar tecnologias e requisitos de infraestrutura, traduzindo métricas de código em recomendações reais de **Deployment** e custos de nuvem.

---

## 🎯 Objetivo

O projeto automatiza a análise de viabilidade financeira de projetos de software. Ao escanear um repositório, o sistema identifica o perfil tecnológico e sugere a **estratégia de deployment** mais eficiente, calculando o impacto mensal baseado em preços reais da AWS.

## 🚀 Funcionalidades Principais

### 1. Scanner de Deployment & Infraestrutura
- **Detecção de Containers**: Identifica arquivos `Dockerfile` e sugere automaticamente o deploy via **AWS Fargate** ou **Amazon ECS**.
- **Análise Poliglota**: Suporte nativo para **Python, JavaScript, TypeScript, Java, Go, C++, PHP, Ruby e SQL**.
- **Mapeamento de Dependências**: Detecta automaticamente a necessidade de Bancos de Dados (RDS) e instâncias de processamento pesado.

### 2. Motor de Precificação FinOps (Real-Time)
- **Suporte Regional**: Cálculos baseados nos preços de **São Paulo (sa-east-1)**, **N. Virginia (us-east-1)** e **Ireland (eu-west-1)**.
- **Modelagem de Custo de Compute**:
    - **Serverless (Lambda)**: Estimado via latência heurística detectada no código.
    - **Provisionado (EC2)**: Recomendado para cargas constantes e aplicações legadas.
    - **Containerizado (Fargate)**: Focado em microserviços modernos.

### 3. Métricas de Performance
- **Estimativa de Latência**: Modelo que calcula o tempo de execução (ms) baseado na complexidade e volume de cada script.
- **Risco de Manutenção**: Projeção de custo operacional baseada na densidade técnica do projeto.

---

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.10+
- **Frontend**: Streamlit (Dashboard Interativo)
- **Análise Estática**: Python AST & Regex Patterns.
- **Data Engine**: Pandas para relatórios financeiros.

---

## ⚙️ Instalação e Execução

1. **Clonar e Acessar**:
   ```bash
   git clone https://github.com/seu-usuario/aws-cost-sentinel.git
   cd aws-cost-sentinel
   ```

2. **Configurar Ambiente**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar**:
   ```bash
   streamlit run app.py
   ```

---

## 🏗️ Estratégia de Hospedagem (Onde fazer o Deploy desta ferramenta)
Esta ferramenta pode ser facilmente hospedada no **Streamlit Cloud**, **AWS App Runner** ou em um container **Docker** próprio, permitindo que equipes de Cloud e FinOps analisem projetos de forma centralizada.

---

## 📝 Licença
MIT License.

---
**Desenvolvido para demonstração de competências em Arquitetura Cloud, FinOps e Engenharia de Software.**
