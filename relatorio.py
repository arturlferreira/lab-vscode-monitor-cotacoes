import csv
import os
from datetime import datetime

def salvar_csv(dados):
    """Salva as cotações em um arquivo CSV na pasta output/"""
    
    # Cria a pasta output/ se não existir
    os.makedirs("output", exist_ok=True)
    
    arquivo = "output/cotacoes.csv"
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Verifica se o arquivo já existe para não repetir o cabeçalho
    arquivo_novo = not os.path.exists(arquivo)
    
    with open(arquivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        if arquivo_novo:
            writer.writerow(["Data/Hora", "Moeda", "Valor (R$)"])
        
        moedas = {
            "USDBRL": "Dólar (USD)",
            "EURBRL": "Euro (EUR)",
            "BTCBRL": "Bitcoin (BTC)"
        }
        
        for codigo, nome in moedas.items():
            valor = float(dados[codigo]["bid"])
            writer.writerow([agora, nome, f"{valor:.2f}"])
    
    print(f"✅ Relatório salvo em {arquivo}")