# Monitor de Cotações Financeiras

## O que este projeto faz
Script Python que busca cotações em tempo real (Dólar, Euro, Bitcoin)
via AwesomeAPI, salva histórico em CSV e exibe um dashboard web com Streamlit.

## Stack
- Python 3.14
- requests
- streamlit
- pandas

## APIs utilizadas
### Cotação atual
GET https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL

### Histórico 30 dias
GET https://economia.awesomeapi.com.br/json/daily/USD-BRL/30
GET https://economia.awesomeapi.com.br/json/daily/EUR-BRL/30
GET https://economia.awesomeapi.com.br/json/daily/BTC-BRL/30

Gratuita, sem autenticação, sem limite para uso básico.

## Estrutura de arquivos
meu-projeto/
├── main.py           → busca e exibe cotações no terminal
├── relatorio.py      → salva histórico em CSV
├── dashboard.py      → dashboard Streamlit
├── output/
│   └── cotacoes.csv  → histórico acumulado
├── CLAUDE.md
├── .gitignore
└── requirements.txt

## O que o dashboard deve ter
1. Cards de destaque com valor atual de Dólar, Euro e Bitcoin
2. Data e hora da última atualização
3. Botão "Atualizar" para buscar cotação em tempo real
4. Gráfico de linha com evolução dos últimos 30 dias por moeda
5. Tabela com histórico salvo no cotacoes.csv

## Padrões que devo seguir
- Comentar funções em português
- Tratar erros de API com try/except
- Salvar arquivos gerados sempre em output/
- Separar responsabilidades: main.py (terminal), dashboard.py (Streamlit)