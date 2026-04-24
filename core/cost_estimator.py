from core.aws_calculator import calculate_ec2_cost, calculate_rds_cost, calculate_lambda_cost

def mapear_codigo_para_infra(relatorio_analise, regiao="us-east-1"):
    recomendacao = {
        "servicos": [],
        "custo_total": 0
    }
    
    # 1. Decisão de Compute
    if relatorio_analise["usa_docker"]:
        # Se tem Docker, sugere Fargate (estimativa simplificada baseada em EC2 small)
        custo = calculate_ec2_cost("t3.small", regiao)
        recomendacao["servicos"].append({
            "servico": "AWS Fargate (Container)",
            "custo": custo,
            "motivo": "Detectado Dockerfile. Recomendado para microserviços containerizados."
        })
        recomendacao["custo_total"] += custo
        
    elif relatorio_analise["total_linhas"] > 3000 or relatorio_analise["usa_processamento_pesado"]:
        tipo_ec2 = "t3.medium" if relatorio_analise["usa_processamento_pesado"] else "t3.micro"
        custo = calculate_ec2_cost(tipo_ec2, regiao)
        recomendacao["servicos"].append({
            "servico": f"EC2 ({tipo_ec2})",
            "custo": custo,
            "motivo": "Volume de código ou processamento intensivo detectado."
        })
        recomendacao["custo_total"] += custo
    else:
        latencia_media = relatorio_analise["latencia_total_ms"] / max(len(relatorio_analise["arquivos"]), 1)
        custo = calculate_lambda_cost(200000, latencia_media, 512)
        recomendacao["servicos"].append({
            "servico": "AWS Lambda",
            "custo": custo,
            "motivo": f"Latência média de {latencia_media:.0f}ms ideal para Serverless."
        })
        recomendacao["custo_total"] += custo

    # 2. Banco de Dados
    if relatorio_analise["usa_db"]:
        custo_db = calculate_rds_cost("db.t3.micro", regiao)
        recomendacao["servicos"].append({
            "servico": "RDS (MySQL/Postgres)",
            "custo": custo_db,
            "motivo": "Detectado uso de persistência SQL ou drivers de banco."
        })
        recomendacao["custo_total"] += custo_db

    return recomendacao

def calcular_custo_manutencao(relatorio_analise):
    # Risco financeiro baseado em linguagens variadas e linhas totais
    score = relatorio_analise["total_linhas"] / 1000
    return score * 15
