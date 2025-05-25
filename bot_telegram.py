import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def enviar_resumo_telegram(emails_filtrados):
    if not emails_filtrados:
        print("Nenhum email para enviar no Telegram.")
        return

    mensagens = []
    mensagem_atual = "Resumo de Projetos Encontrados:*\n\n"
    for email in emails_filtrados:
        assunto = email["assunto"]
        corpo_resumido = email["corpo"][:500].strip().replace("\n", " ")
        bloco = f"{assunto}*\n{corpo_resumido}\n\n"

        if len(mensagem_atual) + len(bloco) > 4000:
            mensagens.append(mensagem_atual)
            mensagem_atual = bloco
        else:
            mensagem_atual += bloco
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

