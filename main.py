from email_reader import ler_emails
from email_sender import enviar_email
from config import EMAIL_USUARIO
from exportador import exportar_csv
from exportador_sheets import exportar_para_google_sheets
from bot_telegram import enviar_resumo_telegram


def main():
    emails_filtrados, resumo = ler_emails()
    print("Resumo retornado:",resumo)

    if emails_filtrados:
        enviar_email(resumo, EMAIL_USUARIO)
        exportar_csv(emails_filtrados)
        exportar_para_google_sheets(emails_filtrados)
        enviar_resumo_telegram(emails_filtrados)
    else:
        print("Nenhum email filtrado encontrado")

if __name__ == "__main__":
    main()
