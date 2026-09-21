from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def carregar_dados() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega contas e histórico fictícios usados pelo agente."""
    contas = pd.read_csv(DATA_DIR / "contas.csv", parse_dates=["data_fechamento", "data_vencimento"])
    historico = pd.read_csv(DATA_DIR / "historico_atendimento.csv", parse_dates=["data"])
    return contas, historico


def dinheiro(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def data_br(valor: Any) -> str:
    if pd.isna(valor):
        return "data não informada"
    return pd.Timestamp(valor).strftime("%d/%m/%Y")


def _encontrar_conta(pergunta: str, contas: pd.DataFrame) -> pd.DataFrame:
    termos = re.findall(r"[\wÀ-ÿ]+", pergunta.lower())
    mascaras = []
    for nome in contas["conta"].astype(str):
        palavras = [p for p in re.findall(r"[\wÀ-ÿ]+", nome.lower()) if len(p) > 2]
        if palavras and any(p in termos or p in pergunta.lower() for p in palavras):
            mascaras.append(nome)
    return contas[contas["conta"].isin(mascaras)]


def responder_deterministico(pergunta: str, contas: pd.DataFrame, historico: pd.DataFrame) -> str:
    """Responde somente com fatos da base, servindo também como fallback do LLM."""
    texto = pergunta.strip().lower()
    if any(p in texto for p in ("senha", "token", "cartão completo", "dados sensíveis")):
        return "Não tenho acesso a senhas ou dados sensíveis. Posso ajudar com as datas e os valores informativos das contas cadastradas."
    if any(p in texto for p in ("pagar primeiro", "prioridade", "qual conta devo pagar")):
        return "Posso informar os vencimentos cadastrados, mas não recomendo prioridade de pagamentos. A decisão deve ser feita por você."
    if any(p in texto for p in ("tempo", "notícia", "receita", "esporte")):
        return "Sou o Senninha e posso ajudar com datas, valores e status informativo das contas cadastradas."

    encontradas = _encontrar_conta(texto, contas)
    if any(p in texto for p in ("fechamento", "fecha", "fechar")):
        if encontradas.empty:
            return "Não encontrei essa conta na base demonstrativa. Informe o nome cadastrado para eu consultar o fechamento."
        return " ".join(
            f"{r.conta} tem fechamento em {data_br(r.data_fechamento)} e vencimento em {data_br(r.data_vencimento)}."
            for r in encontradas.itertuples()
        )

    if any(p in texto for p in ("vencimento", "vence", "vencimentos", "datas", "contas")):
        ordenadas = contas.sort_values("data_vencimento") if encontradas.empty else encontradas.sort_values("data_vencimento")
        itens = [f"{r.conta}: {data_br(r.data_vencimento)} ({dinheiro(r.valor)})" for r in ordenadas.itertuples()]
        return "Vencimentos cadastrados: " + "; ".join(itens) + ". Essas datas são informativas; não indico prioridade de pagamento."

    if any(p in texto for p in ("histórico", "historico", "já falei", "atendimento")):
        if historico.empty:
            return "Não há atendimentos anteriores na base demonstrativa."
        temas = ", ".join(f"{r.tema} em {data_br(r.data)}" for r in historico.itertuples())
        return f"Há atendimentos anteriores registrados sobre: {temas}."

    if encontradas.empty:
        return "Posso consultar fechamento, vencimento, valor e histórico das contas cadastradas. Qual conta ou data você deseja verificar?"
    return " ".join(f"{r.conta}: valor {dinheiro(r.valor)}, vencimento em {data_br(r.data_vencimento)}." for r in encontradas.itertuples())


def contexto(pergunta: str, contas: pd.DataFrame, historico: pd.DataFrame) -> str:
    relevantes = _encontrar_conta(pergunta.lower(), contas)
    if relevantes.empty and any(p in pergunta.lower() for p in ("vencimento", "contas", "datas")):
        relevantes = contas.sort_values("data_vencimento").head(5)
    linhas = [
        f"- {r.conta} | fechamento: {data_br(r.data_fechamento)} | vencimento: {data_br(r.data_vencimento)} | valor: {dinheiro(r.valor)} | status: {r.status}"
        for r in relevantes.itertuples()
    ]
    return "Contas relevantes:\n" + ("\n".join(linhas) if linhas else "Nenhuma conta relevante encontrada.")


def gerar_resposta(pergunta: str, contas: pd.DataFrame, historico: pd.DataFrame, usar_ollama: bool = False, modelo: str = "llama3.2") -> str:
    """Usa Ollama opcionalmente; nunca deixa o modelo ser a única fonte de dados."""
    fallback = responder_deterministico(pergunta, contas, historico)
    if not usar_ollama:
        return fallback
    try:
        import requests
        prompt = (
            "Você é Senninha. Responda em português, de forma técnica e curta. "
            "Use somente o contexto; não invente dados, não revele dados sensíveis e não recomende prioridade de pagamento.\n\n"
            f"{contexto(pergunta, contas, historico)}\nPergunta: {pergunta}"
        )
        resposta = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": modelo, "prompt": prompt, "stream": False},
            timeout=20,
        )
        resposta.raise_for_status()
        texto = resposta.json().get("response", "").strip()
        return texto or fallback
    except (OSError, ValueError, requests.RequestException):
        return fallback
