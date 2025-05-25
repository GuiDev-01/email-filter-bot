import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_USUARIO, SENHA_APP

def enviar_email(resumo,destinatario):
    msg = MIMEMultipart()
    msg["from"] = EMAIL_USUARIO
    msg["to"] = destinatario
    msg["Subject"] = "Resumo de Projetos Encontrados"

    corpo = MIMEText(resumo,'plain')
    msg.attach(corpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USUARIO, SENHA_APP)
            smtp.send_message(msg)
            print("Resumo enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o email: {e}")

