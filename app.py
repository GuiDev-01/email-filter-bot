
import streamlit as st
import collections
import os
import dotenv
from email_reader import ler_emails
from exportador import exportar_csv
from exportador_sheets import exportar_para_google_sheets
from bot_telegram import enviar_resumo_telegram

st.set_page_config(page_title="Email Filter Bot", layout="wide")
st.title("Email Filter Bot - Dashboard")


# Filtros
st.subheader("Filtros de busca")
palavra_chave = st.text_input("Palavra-chave (opcional)")
remetente = st.text_input("Remetente (opcional)")

if "emails_filtrados" not in st.session_state:
    st.session_state["emails_filtrados"] = []
    st.session_state["resumo"] = ""

if st.button("Buscar e Filtrar Emails"):
    emails_filtrados, resumo = ler_emails()
    st.session_state["emails_filtrados"] = emails_filtrados
    st.session_state["resumo"] = resumo

emails_filtrados = st.session_state["emails_filtrados"]
resumo = st.session_state["resumo"]


# Aplicar filtros na lista de emails
def filtrar_emails(emails, palavra_chave, remetente):
    filtrados = []
    for email in emails:
        assunto = email.get("assunto", "")
        corpo = email.get("corpo", "")
        # Filtro por palavra-chave
        if palavra_chave and palavra_chave.lower() not in assunto.lower() and palavra_chave.lower() not in corpo.lower():
            continue
        # Filtro por remetente (se disponível)
        if remetente and "remetente" in email and remetente.lower() not in email["remetente"].lower():
            continue
        filtrados.append(email)
    return filtrados

emails_filtrados_exibidos = filtrar_emails(emails_filtrados, palavra_chave, remetente)

if emails_filtrados_exibidos:
    st.success(f"{len(emails_filtrados_exibidos)} emails filtrados!")
    st.write(resumo)
    st.dataframe(emails_filtrados_exibidos)

    # Estatísticas: emails por palavra-chave
    st.subheader("Estatísticas de palavras-chave")
    palavras = [
        'python', 'sql', 'dados', 'power bi', 'excel', 'projeto', 'freela', 'vaga', 'remoto', 'analista',
        'iniciante', 'junior', 'nível básico', 'estágio', 'trabalho', 'oportunidade', 'desenvolvedor', 'estudante'
    ]
    contagem = collections.Counter()
    for email in emails_filtrados_exibidos:
        texto = (email.get("assunto", "") + " " + email.get("corpo", "")).lower()
        for palavra in palavras:
            if palavra in texto:
                contagem[palavra] += 1
    if contagem:
        st.bar_chart(dict(contagem))
    else:
        st.info("Nenhuma palavra-chave encontrada nos emails filtrados.")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Exportar para CSV"):
            try:
                exportar_csv(emails_filtrados_exibidos)
                st.info("Exportado para CSV!")
            except Exception as e:
                st.error(f"Erro ao exportar para CSV: {e}")
    # Histórico de exportações
    import os
    st.subheader("Histórico de exportações (CSV)")
    arquivos_csv = [f for f in os.listdir(os.getcwd()) if f.startswith("emails_filtrados_") and f.endswith(".csv")]
    if arquivos_csv:
        for arquivo in sorted(arquivos_csv, reverse=True):
            with open(arquivo, "rb") as f:
                st.download_button(
                    label=f"Baixar {arquivo}",
                    data=f.read(),
                    file_name=arquivo,
                    mime="text/csv"
                )
    else:
        st.info("Nenhum arquivo CSV exportado encontrado.")
    with col2:
        if st.button("Exportar para Google Sheets"):
            try:
                exportar_para_google_sheets(emails_filtrados_exibidos)
                st.info("Exportado para Google Sheets!")
            except Exception as e:
                st.error(f"Erro ao exportar para Google Sheets: {e}")
    with col3:
        if st.button("Enviar para Telegram"):
            try:
                enviar_resumo_telegram(emails_filtrados_exibidos)
                st.info("Resumo enviado para Telegram!")
            except Exception as e:
                st.error(f"Erro ao enviar para Telegram: {e}")
else:
    st.warning("Nenhum email filtrado encontrado.")
