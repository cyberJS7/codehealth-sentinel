import os
import ast
import re
from typing import Dict, Any, List

# Mapeamento de extensões para linguagens
EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.cpp': 'C++',
    '.sql': 'SQL',
    'Dockerfile': 'Docker'
}

def detectar_tecnologias_generico(conteudo: str, extensao: str) -> Dict[str, bool]:
    """
    Detecta tecnologias em arquivos não-Python usando busca de padrões.
    """
    tecnologias = {
        "usa_db": False,
        "usa_processamento_pesado": False,
        "framework": None
    }
    
    # Padrões comuns de DB
    if re.search(r'(postgresql|postgres|mysql|mongodb|redis|oracle|sqlite|prisma|typeorm)', conteudo, re.I):
        tecnologias["usa_db"] = True
        
    # Padrões de Processamento Pesado
    if re.search(r'(spark|hadoop|tensorflow|pytorch|scikit-learn|linalg)', conteudo, re.I):
        tecnologias["usa_processamento_pesado"] = True

    return tecnologias

def analisar_projeto(diretorio: str = ".") -> Dict[str, Any]:
    relatorio = {
        "arquivos": [],
        "total_linhas": 0,
        "linguagens": {},
        "frameworks": set(),
        "usa_db": False,
        "usa_processamento_pesado": False,
        "usa_docker": False,
        "latencia_total_ms": 0,
        "complexidade_media": 0
    }
    
    total_cc = 0
    contagem_arquivos = 0

    for root, dirs, files in os.walk(diretorio):
        if any(ignored in root for ignored in ['venv', '.git', '__pycache__', 'node_modules', '.idea', 'dist', 'build']):
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1] or file
            if ext not in EXTENSIONS:
                continue
                
            linguagem = EXTENSIONS[ext]
            relatorio["linguagens"][linguagem] = relatorio["linguagens"].get(linguagem, 0) + 1
            
            caminho = os.path.join(root, file)
            contagem_arquivos += 1
            
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()
                    linhas = len(conteudo.splitlines())
                    relatorio["total_linhas"] += linhas
                    
                    cc_arquivo = 0
                    
                    # Análise profunda se for Python
                    if linguagem == 'Python':
                        try:
                            tree = ast.parse(conteudo)
                            cc_arquivo = len([n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))])
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.Import, ast.ImportFrom)):
                                    names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module]
                                    for name in names:
                                        if name:
                                            if any(lib in name for lib in ["pandas", "numpy", "sklearn"]): relatorio["usa_processamento_pesado"] = True
                                            if any(lib in name for lib in ["sqlalchemy", "psycopg2", "mysql"]): relatorio["usa_db"] = True
                                            if any(lib in name for lib in ["flask", "fastapi", "django", "streamlit"]): relatorio["frameworks"].add(name.split('.')[0])
                        except:
                            pass
                    
                    # Análise Genérica para outras linguagens
                    else:
                        techs = detectar_tecnologias_generico(conteudo, ext)
                        if techs["usa_db"]: relatorio["usa_db"] = True
                        if techs["usa_processamento_pesado"]: relatorio["usa_processamento_pesado"] = True
                        if linguagem == 'Docker': relatorio["usa_docker"] = True

                    # Estimativa de Latência (Baseada em linguagem e volume)
                    multiplicador_latencia = 1.5 if linguagem in ['Java', 'Python'] else 1.0
                    latencia = (50 + (linhas / 5) + (cc_arquivo * 15)) * multiplicador_latencia
                    relatorio["latencia_total_ms"] += latencia
                    total_cc += cc_arquivo

                    relatorio["arquivos"].append({
                        "nome": file,
                        "linguagem": linguagem,
                        "linhas": linhas,
                        "latencia_ms": round(latencia, 2)
                    })
            except:
                pass

    if contagem_arquivos > 0:
        relatorio["complexidade_media"] = total_cc / contagem_arquivos
    
    relatorio["frameworks"] = list(relatorio["frameworks"])
    return relatorio
