def calcular_custo_manutencao(relatorio_complexidade):
    """
    Calcula uma estimativa simbólica de 'Débito Técnico' em dólares.
    Lógica: Cada ponto de complexidade acima de 5 custa $10 em manutenção/mês.
    """
    custo_total = 0
    for item in relatorio_complexidade:
        score = item['complexidade']
        if score > 5:
            # Cálculo fictício de débito técnico
            excesso = score - 5
            custo_total += excesso * 10 
            
    return round(custo_total, 2)

def estimar_infra_aws(num_arquivos, tem_dependencias=True):
    """
    Simula o custo de processamento na AWS para análise estática.
    """
    base_price = 2.50 # Preço base por execução em Lambda/Serverless
    custo_arquivos = num_arquivos * 0.10
    
    total = base_price + custo_arquivos
    return round(total, 2)