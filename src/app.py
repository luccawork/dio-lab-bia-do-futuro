import streamlit as st

from agente import carregar_dados, gerar_resposta


st.set_page_config(page_title="Senninha | Contas", page_icon="📅", layout="centered")
st.title("📅 Senninha")
st.caption("Agente consultivo para acompanhamento de fechamento e vencimento de contas")

if "contas" not in st.session_state or "historico" not in st.session_state:
    st.session_state.contas, st.session_state.historico = carregar_dados()
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.subheader("Dados demonstrativos")
    st.write(f"{len(st.session_state.contas)} contas cadastradas")
    st.write(f"{len(st.session_state.historico)} atendimentos no histórico")
    usar_ollama = st.toggle("Usar Ollama local", value=False, help="Se indisponível, o app usa o fallback seguro baseado na base.")
    modelo = st.text_input("Modelo Ollama", value="llama3.2", disabled=not usar_ollama)
    if st.button("Recarregar dados"):
        st.session_state.contas, st.session_state.historico = carregar_dados()
        st.rerun()
    st.divider()
    st.warning("Dados fictícios. O Senninha informa datas e valores, mas não recomenda prioridade de pagamentos.")

st.subheader("Contas cadastradas")
st.dataframe(
    st.session_state.contas[["conta", "valor", "data_fechamento", "data_vencimento", "status"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "data_fechamento": st.column_config.DateColumn("Fechamento", format="DD/MM/YYYY"),
        "data_vencimento": st.column_config.DateColumn("Vencimento", format="DD/MM/YYYY"),
    },
)

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["papel"]):
        st.markdown(mensagem["texto"])

pergunta = st.chat_input("Ex.: quando fecha o cartão principal?")
if pergunta:
    st.session_state.mensagens.append({"papel": "user", "texto": pergunta})
    resposta = gerar_resposta(pergunta, st.session_state.contas, st.session_state.historico, usar_ollama, modelo)
    st.session_state.mensagens.append({"papel": "assistant", "texto": resposta})
    st.rerun()
