import os
import ast
import time
from typing import Dict, Any, List

def analisar_projeto(diretorio: str = ".") -> Dict[str, Any]:
    """
    Analisa o código-fonte e estima métricas de performance e custo.
    """
    relatorio = {
        "arquivos": [],
        "total_linhas": 0,
        "frameworks": set(),
        "usa_db": False,
        "usa_processamento_pesado": False,
        "complexidade_media": 0,
        "latencia_total_ms": 0
    }
    
    total_funcoes_classes = 0
    contagem_arquivos = 0

    for root, dirs, files in os.walk(diretorio):
        if any(ignored in root for ignored in ['venv', '.git', '__pycache__', 'node_modules', '.idea']):
            continue
            
        for file in files:
            if file.endswith(".py"):
                caminho = os.path.join(root, file)
                contagem_arquivos += 1
                try:
                    start_time = time.time()
                    with open(caminho, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                        tree = ast.parse(conteudo)
                        
                        linhas = len(conteudo.splitlines())
                        relatorio["total_linhas"] += linhas
                        
                        # Detecção de perfil tecnológico
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.Import, ast.ImportFrom)):
                                names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module]
                                for name in names:
                                    if name:
                                        if any(lib in name for lib in ["pandas", "numpy", "sklearn", "torch"]):
                                            relatorio["usa_processamento_pesado"] = True
                                        if any(lib in name for lib in ["sqlalchemy", "psycopg2", "mysql", "sqlite"]):
                                            relatorio["usa_db"] = True
                                        if any(lib in name for lib in ["flask", "fastapi", "django", "streamlit"]):
                                            relatorio["frameworks"].add(name.split('.')[0])

                        # Heurística de Performance: 
                        # Base de 50ms + 10ms por 100 linhas + 20ms por bloco lógico
                        blocos_logicos = len([n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))])
                        total_funcoes_classes += blocos_logicos
                        
                        latencia_estimada = 50 + (linhas / 10) + (blocos_logicos * 20)
                        if relatorio["usa_processamento_pesado"]:
                            latencia_estimada *= 2.5 # Processamento de dados aumenta a latência
                        
                        relatorio["latencia_total_ms"] += latencia_estimada
                        
                        relatorio["arquivos"].append({
                            "nome": file,
                            "linhas": linhas,
                            "complexidade": blocos_logicos,
                            "tempo_execucao_ms": round(latencia_estimada, 2)
                        })
                except Exception:
                    pass

    if contagem_arquivos > 0:
        relatorio["complexidade_media"] = total_funcoes_classes / contagem_arquivos
        
    relatorio["frameworks"] = list(relatorio["frameworks"])
    return relatorio
