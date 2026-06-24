import os
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

URL_COTACAO_ATUAL = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"
URL_HISTORICO = "https://economia.awesomeapi.com.br/json/daily/{par}/30"

# Caminho ancorado ao diretório do script para ser válido em qualquer CWD
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(_BASE_DIR, "output", "cotacoes.csv")
_OUTPUT_DIR = os.path.join(_BASE_DIR, "output")

CHAVES_COTACAO = {"bid", "pctChange"}
CHAVES_HISTORICO = {"timestamp", "bid"}

MOEDAS: dict[str, dict[str, str]] = {
    "USDBRL": {"nome": "Dólar (USD)", "simbolo": "USD", "par": "USD-BRL", "cor": "#1f77b4"},
    "EURBRL": {"nome": "Euro (EUR)", "simbolo": "EUR", "par": "EUR-BRL", "cor": "#ff7f0e"},
    "BTCBRL": {"nome": "Bitcoin (BTC)", "simbolo": "BTC", "par": "BTC-BRL", "cor": "#f7931a"},
}


def buscar_cotacao_atual() -> dict | None:
    """Busca cotações em tempo real via AwesomeAPI e valida o formato da resposta"""
    try:
        response = requests.get(URL_COTACAO_ATUAL, timeout=10)
        response.raise_for_status()
        dados = response.json()
        if not all(
            cod in dados and CHAVES_COTACAO.issubset(dados[cod])
            for cod in MOEDAS
        ):
            st.error("Resposta da API em formato inesperado.")
            return None
        return dados
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar cotações: {e}")
        return None


def buscar_historico(par: str) -> list[dict] | None:
    """Busca histórico de 30 dias de uma moeda via AwesomeAPI"""
    try:
        url = URL_HISTORICO.format(par=par)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar histórico de {par}: {e}")
        return None


def salvar_cotacao_csv(dados: dict) -> None:
    """Salva cotações atuais no histórico CSV"""
    os.makedirs(_OUTPUT_DIR, exist_ok=True)

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    arquivo_novo = not os.path.exists(ARQUIVO_CSV)

    rows = []
    for codigo, info in MOEDAS.items():
        try:
            valor = float(dados[codigo]["bid"])
        except (KeyError, ValueError) as e:
            st.error(f"Valor inválido para {codigo}: {e}")
            return
        rows.append({"Data/Hora": agora, "Moeda": info["nome"], "Valor (R$)": f"{valor:.2f}"})

    df_novo = pd.DataFrame(rows)

    if arquivo_novo:
        df_novo.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8")
    else:
        df_novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8")


def carregar_historico_csv() -> pd.DataFrame | None:
    """Carrega o histórico salvo do CSV"""
    if not os.path.exists(ARQUIVO_CSV):
        return None

    try:
        df = pd.read_csv(ARQUIVO_CSV, encoding="utf-8")
        df["Valor (R$)"] = pd.to_numeric(df["Valor (R$)"], errors="coerce")
        return df
    except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError) as e:
        st.error(f"Erro ao carregar histórico: {e}")
        return None


def construir_grafico_historico() -> go.Figure | None:
    """Monta gráfico de linha com histórico de 30 dias via API"""
    fig = go.Figure()
    encontrou_dados = False

    for codigo, info in MOEDAS.items():
        historico = buscar_historico(info["par"])
        if not historico:
            continue

        encontrou_dados = True
        pontos_validos = [p for p in historico if CHAVES_HISTORICO.issubset(p)]
        try:
            datas = [
                datetime.fromtimestamp(int(p["timestamp"])).strftime("%d/%m")
                for p in reversed(pontos_validos)
            ]
            valores = [float(p["bid"]) for p in reversed(pontos_validos)]
        except (ValueError, OSError) as e:
            st.error(f"Erro ao processar histórico de {info['nome']}: {e}")
            continue

        fig.add_trace(
            go.Scatter(
                x=datas,
                y=valores,
                mode="lines+markers",
                name=info["nome"],
                line={"color": info["cor"], "width": 2},
                marker={"size": 4},
            )
        )

    if not encontrou_dados:
        return None

    fig.update_layout(
        title="Evolução dos últimos 30 dias",
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        hovermode="x unified",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font={"color": "#fafafa"},
        xaxis={"gridcolor": "#333"},
        yaxis={"gridcolor": "#333"},
        margin={"t": 60, "b": 40},
    )

    return fig


def renderizar_cards(dados: dict, atualizado_em: str) -> None:
    """Exibe cards de destaque com cotações atuais"""
    st.markdown(f"**Última atualização:** {atualizado_em}")
    cols = st.columns(3)

    for col, (codigo, info) in zip(cols, MOEDAS.items()):
        cotacao = dados[codigo]
        try:
            valor = float(cotacao["bid"])
            variacao = float(cotacao["pctChange"])
        except (KeyError, ValueError):
            with col:
                st.metric(label=info["nome"], value="—", delta="erro")
            continue

        seta = "▲" if variacao >= 0 else "▼"

        with col:
            st.metric(
                label=info["nome"],
                value=f"R$ {valor:,.2f}",
                delta=f"{seta} {abs(variacao):.2f}%",
            )


def main() -> None:
    """Ponto de entrada do dashboard Streamlit"""
    st.set_page_config(
        page_title="Monitor de Cotações",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 Monitor de Cotações Financeiras")

    # Inicializa estado da sessão para evitar chamadas desnecessárias à API
    if "dados_atuais" not in st.session_state:
        st.session_state.dados_atuais = None
        st.session_state.atualizado_em = None

    col_btn, _ = st.columns([1, 5])
    with col_btn:
        if st.button("🔄 Atualizar", use_container_width=True):
            with st.spinner("Buscando cotações..."):
                dados = buscar_cotacao_atual()
                if dados:
                    st.session_state.dados_atuais = dados
                    st.session_state.atualizado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    salvar_cotacao_csv(dados)

    # Busca automática na primeira visita
    if st.session_state.dados_atuais is None:
        with st.spinner("Carregando cotações..."):
            dados = buscar_cotacao_atual()
            if dados:
                st.session_state.dados_atuais = dados
                st.session_state.atualizado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                salvar_cotacao_csv(dados)

    if st.session_state.dados_atuais:
        renderizar_cards(st.session_state.dados_atuais, st.session_state.atualizado_em)

    st.divider()

    # Gráfico de histórico de 30 dias
    st.subheader("Evolução histórica — 30 dias")
    with st.spinner("Carregando histórico..."):
        fig = construir_grafico_historico()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não foi possível carregar o histórico no momento.")

    st.divider()

    # Tabela com histórico local do CSV
    st.subheader("Histórico salvo localmente")
    df = carregar_historico_csv()
    if df is not None and not df.empty:
        st.dataframe(
            df.sort_values("Data/Hora", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Nenhum histórico salvo ainda. Clique em Atualizar para começar.")


if __name__ == "__main__":
    main()
