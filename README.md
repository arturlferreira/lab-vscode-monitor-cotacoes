# 📊 Monitor de Cotações Financeiras

Script Python que busca cotações em tempo real e salva histórico em CSV.

## O que faz
- Busca Dólar, Euro e Bitcoin via AwesomeAPI
- Exibe os valores no terminal
- Salva histórico acumulado em `output/cotacoes.csv`

## Como usar

### 1. Instalar dependências
pip install requests

### 2. Rodar
python main.py

## Tecnologias
- Python 3.14
- [AwesomeAPI](https://economia.awesomeapi.com.br) — gratuita, sem autenticação

## Estrutura
```
monitor-cotacoes/
├── main.py        → busca e exibe cotações
├── relatorio.py   → salva CSV
├── output/        → arquivos gerados
└── CLAUDE.md      → contexto para Claude Code
```