from core.aws_calculator import calculate_ec2_cost, calculate_rds_cost, calculate_lambda_cost

def mapear_codigo_para_infra(relatorio_analise, regiao="us-east-1"):
    """
    Traduz métricas de código em componentes de infraestrutura AWS.
    """
    recomendacao = {
        "servicos": [],
        "custo_total": 0
    }
    
    # Decisão de Compute baseada em volume e tempo de execução
    if relatorio_analise["total_linhas"] > 5000 or relatorio_analise["usa_processamento_pesado"]:
        tipo_ec2 = "t3.medium" if relatorio_analise["usa_processamento_pesado"] else "t3.micro"
        custo = calculate_ec2_cost(tipo_ec2, regiao)
        recomendacao["servicos"].append({
            "servico": f"EC2 ({tipo_ec2})",
            "custo": custo,
            "motivo": "Perfil de carga constante ou processamento pesado detectado."
        })
        recomendacao["custo_total"] += custo
    else:
        # Usa a latência média detectada para calcular o Lambda
        latencia_media = relatorio_analise["latencia_total_ms"] / max(len(relatorio_analise["arquivos"]), 1)
        custo = calculate_lambda_cost(100000, latencia_media, 512) # 100k req/mês
        recomendacao["servicos"].append({
            "servico": "AWS Lambda",
            "custo": custo,
            "motivo": f"Latência estimada de {latencia_media:.2f}ms favorece modelo Serverless."
        })
        recomendacao["custo_total"] += custo

    if relatorio_analise["usa_db"]:
        custo_db = calculate_rds_cost("db.t3.micro", regiao)
        recomendacao["servicos"].append({
            "servico": "RDS (db.t3.micro)",
            "custo": custo_db,
            "motivo": "Persistência de dados relacional detectada via imports."
        })
        recomendacao["custo_total"] += custo_db

    return recomendacao

def calcular_custo_manutencao(relatorio_analise):
    """Estima custo operacional de manutenção baseado na complexidade."""
    score = relatorio_analise["complexidade_media"]
    return (score - 2) * 25 if score > 2 else 0
