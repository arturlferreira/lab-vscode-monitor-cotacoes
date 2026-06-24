# Monitor de Cotações Financeiras

## O que este projeto faz
Script Python que busca cotações em tempo real (Dólar, Euro, Bitcoin)
via AwesomeAPI e salva um relatório CSV na pasta output/.

## Stack
- Python 3.14
- requests

## API
- URL: https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL
- Gratuita, sem autenticação

## Padrões que devo seguir
- Comentar funções em português
- Tratar erros de API com try/except
- Salvar arquivos gerados sempre em output/