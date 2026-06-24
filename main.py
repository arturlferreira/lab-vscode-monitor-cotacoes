import requests
from datetime import datetime

def buscar_cotacoes():
    """Busca cotações em tempo real via AwesomeAPI"""
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO ao buscar cotações: {e}")
        return None

def exibir_cotacoes(dados):
    """Exibe as cotações no terminal de forma legível"""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"\n📊 Cotações — {agora}")
    print("-" * 40)
    
    moedas = {
        "USDBRL": "Dólar (USD)",
        "EURBRL": "Euro (EUR)",
        "BTCBRL": "Bitcoin (BTC)"
    }
    
    for codigo, nome in moedas.items():
        cotacao = dados[codigo]
        valor = float(cotacao["bid"])
        print(f"{nome}: R$ {valor:,.2f}")
    
    print("-" * 40)

# Ponto de entrada
dados = buscar_cotacoes()
if dados:
    exibir_cotacoes(dados)