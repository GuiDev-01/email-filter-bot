import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def enviar_resumo_telegram(emails_filtrados):
    if not emails_filtrados:
        print("Nenhum email para enviar no Telegram.")
        return

    import re
    def limpar_html(texto):
        return re.sub(r"<.*?>", "", texto)

    def limpar_markdown(texto):
        # Remove todos os caracteres especiais do Markdown do Telegram, inclusive o asterisco
        especiais = r"([*_`\[\]()~>#+=|{}.!-])"
        return re.sub(especiais, "", texto)

    mensagem_cabecalho = "\u2728 Resumo de e-mails filtrados \u2728\n\n"
    mensagens = []
    mensagem_atual = mensagem_cabecalho
    for idx, email in enumerate(emails_filtrados, 1):
        assunto = limpar_markdown(email["assunto"])
        corpo_limpo = limpar_html(email["corpo"])
        corpo_resumido = limpar_markdown(corpo_limpo[:400].strip().replace("\n", " "))
        bloco = f"{assunto}\n{corpo_resumido}\n\n-----------------------------\n"
        if len(mensagem_atual) + len(bloco) > 4000:
            mensagens.append(mensagem_atual)
            mensagem_atual = mensagem_cabecalho + bloco
        else:
            mensagem_atual += bloco
    if mensagem_atual.strip() != mensagem_cabecalho.strip():
        mensagens.append(mensagem_atual)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for msg in mensagens:
        payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("Resumo enviado com sucesso para o Telegram!")
            else:
                print(f"Erro ao enviar para o Telegram: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro na requisição para o Telegram: {e}")

