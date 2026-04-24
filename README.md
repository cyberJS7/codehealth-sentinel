# AWS Cost & Code Sentinel 🛡️☁️

**AWS Cost & Code Sentinel** é uma solução de FinOps (Financial Operations) projetada para integrar análise técnica de software com planejamento orçamentário de infraestrutura. 

A ferramenta realiza uma análise estática do código-fonte (via AST - Abstract Syntax Trees) para identificar padrões arquiteturais, dependências e complexidade técnica, traduzindo esses dados em recomendações reais de serviços e custos na AWS.

---

## 🎯 Objetivo

O projeto resolve o gap entre o desenvolvimento de software e a gestão de custos em nuvem. Ao analisar o código local, o sistema recomenda a infraestrutura mais eficiente (Serverless vs. Servidores) e calcula o custo mensal baseado em preços reais de mercado da AWS.

## 🚀 Funcionalidades Principais

### 1. Scanner Automático de Infraestrutura (IA Logic)
- **Análise de Dependências**: Identifica automaticamente o uso de bancos de dados, bibliotecas de processamento pesado (Data Science) e frameworks web.
- **Mapeamento de Arquitetura**: 
    - Recomenda **AWS Lambda** para projetos modulares e leves.
    - Recomenda **Amazon EC2 (t3.medium/micro)** para aplicações com processamento intensivo de dados.
    - Recomenda **Amazon RDS** ao detectar lógica de persistência SQL.
- **Detecção de Região**: Ajusta os custos automaticamente para regiões como **São Paulo (sa-east-1)**, **N. Virginia (us-east-1)** e **Ireland (eu-west-1)**.

### 2. Calculadora Manual FinOps
- Interface intuitiva para simulação de cenários específicos.
- Suporte a múltiplos serviços: **EC2, S3, RDS e Lambda**.
- Cálculos granulares: Requisições por milhão, duração em milissegundos e alocação de memória GB/s.

### 3. Métricas de Saúde Técnica
- **Complexidade Estrutural**: Avaliação da densidade de lógica por arquivo.
- **Estimativa de Manutenção**: Cálculo simbólico de risco financeiro baseado na complexidade média do projeto.

---

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.10+
- **Frontend**: Streamlit (Dashboard Interativo)
- **Engine de Análise**: Python AST (Abstract Syntax Trees) para análise de código não executável.
- **Processamento de Dados**: Pandas para estruturação de relatórios financeiros.

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

## 📊 Estrutura do Projeto

- `app.py`: Interface do usuário e orquestração dos fluxos.
- `core/analyzer.py`: Motor de análise estática de código.
- `core/aws_calculator.py`: Lógica de precificação baseada na AWS Price List.
- `core/cost_estimator.py`: Mapeador de regras de negócio entre código e infraestrutura.

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar, modificar e distribuir para fins de estudo ou demonstração de portfólio.

---
**Desenvolvido para demonstração de competências em Cloud Computing, Python e FinOps.**
