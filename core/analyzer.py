import os
from radon.complexity import cc_visit

def analisar_projeto(diretorio="."):
    """
    Varre o diretório em busca de arquivos .py e calcula a complexidade.
    """
    relatorio = []
    
    for root, dirs, files in os.walk(diretorio):
        # Pula pastas irrelevantes
        if 'venv' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                caminho_completo = os.path.join(root, file)
                with open(caminho_completo, "r") as f:
                    codigo = f.read()
                    try:
                        metricas = cc_visit(codigo)
                        # Pegamos a média de complexidade do arquivo
                        if metricas:
                            media = sum(m.complexity for m in metricas) / len(metricas)
                        else:
                            media = 0
                        
                        relatorio.append({
                            "arquivo": file,
                            "complexidade": media
                        })
                    except Exception as e:
                        print(f"Erro ao analisar {file}: {e}")
    
    return relatorio

if __name__ == "__main__":
    print("🔍 Iniciando análise de saúde do código...")
    resultados = analisar_projeto()
    for res in resultados:
        status = "✅ Limpo" if res['complexidade'] < 5 else "⚠️ Complexo"
        print(f"Arquivo: {res['arquivo']} | Score: {res['complexidade']:.2f} | Status: {status}")