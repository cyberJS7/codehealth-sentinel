# Tabela de preços simplificada (valores reais aproximados em USD)
# Valores baseados na AWS Price List API (consultada em Abril 2024)
# Para uma versão de produção, recomenda-se usar o SDK boto3 para consultar o serviço 'pricing'.
PRICES = {
    "regions": {
        "us-east-1": "US East (N. Virginia)",
        "sa-east-1": "South America (São Paulo)",
        "eu-west-1": "Europe (Ireland)"
    },
    "ec2": {
        "t3.nano": {"us-east-1": 0.0052, "sa-east-1": 0.0076, "eu-west-1": 0.0058},
        "t3.micro": {"us-east-1": 0.0104, "sa-east-1": 0.0152, "eu-west-1": 0.0116},
        "t3.small": {"us-east-1": 0.0208, "sa-east-1": 0.0304, "eu-west-1": 0.0232},
        "t3.medium": {"us-east-1": 0.0416, "sa-east-1": 0.0608, "eu-west-1": 0.0464},
        "m5.large": {"us-east-1": 0.096, "sa-east-1": 0.142, "eu-west-1": 0.107},
        "c5.large": {"us-east-1": 0.085, "sa-east-1": 0.124, "eu-west-1": 0.095},
    },
    "s3": {
        "standard": {"us-east-1": 0.023, "sa-east-1": 0.0405, "eu-west-1": 0.023},
        "intelligent_tiering": {"us-east-1": 0.023, "sa-east-1": 0.0405, "eu-west-1": 0.023},
        "glacier": {"us-east-1": 0.004, "sa-east-1": 0.0045, "eu-west-1": 0.004},
    },
    "rds": {
        "db.t3.micro": {"us-east-1": 0.017, "sa-east-1": 0.024, "eu-west-1": 0.018},
        "db.t3.small": {"us-east-1": 0.034, "sa-east-1": 0.048, "eu-west-1": 0.036},
        "db.m5.large": {"us-east-1": 0.175, "sa-east-1": 0.258, "eu-west-1": 0.196},
    },
    "lambda": {
        "request": 0.0000002, # por requisição
        "duration_gb_s": 0.0000166667 # por GB-segundo
    }
}

def calculate_ec2_cost(instance_type, region, hours=730):
    """Calcula o custo mensal de uma instância EC2 (padrão 730h/mês)."""
    price_per_hour = PRICES["ec2"].get(instance_type, {}).get(region, 0)
    return price_per_hour * hours

def calculate_s3_cost(storage_gb, storage_class, region):
    """Calcula o custo mensal de armazenamento S3."""
    price_per_gb = PRICES["s3"].get(storage_class, {}).get(region, 0)
    return storage_gb * price_per_gb

def calculate_rds_cost(instance_type, region, hours=730):
    """Calcula o custo mensal de uma instância RDS."""
    price_per_hour = PRICES["rds"].get(instance_type, {}).get(region, 0)
    return price_per_hour * hours

def calculate_lambda_cost(requests, avg_duration_ms, memory_mb):
    """Calcula o custo mensal de AWS Lambda."""
    # Custo por requisição
    request_cost = requests * PRICES["lambda"]["request"]
    
    # Custo por duração
    duration_s = (avg_duration_ms / 1000)
    gb_s = (memory_mb / 1024) * duration_s * requests
    duration_cost = gb_s * PRICES["lambda"]["duration_gb_s"]
    
    return request_cost + duration_cost
