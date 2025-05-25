import imaplib
import email
from email.header import decode_header
from config import EMAIL_USUARIO, SENHA_APP
import re

def limpar_html(texto):
    texto_sem_args = re.sub(r"<.*?>", "", texto)
    return texto_sem_args


def ler_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USUARIO, SENHA_APP)
        print("Conectado com sucesso ao servidor de email")
    except Exception as e:
        print(f"Erro ao conectar com o servidor de email: {e}")
        return [], ""

    mail.select("inbox")
    status, mensagens = mail.search(None, "ALL")
    if status != "OK":
        print("Erro ao buscar emails.")
        return [], ""

    emails_filtrados = []
    resumo = ""

    email_ids = mensagens[0].split()
    email_ids = email_ids[-5:]

    for num in email_ids:
        status, dados = mail.fetch(num, "(RFC822)")
        if status != "OK":
            print(f"Erro ao recuperar email {num}.")
            continue

        for resposta in dados:
            if isinstance(resposta, tuple):
                msg = email.message_from_bytes(resposta[1])
                assunto, encoding = decode_header(msg["Subject"])[0]
                if isinstance(assunto, bytes):
                    assunto = assunto.decode(encoding if encoding else "utf-8")

                corpo = ""

                if msg.is_multipart():
                    for parte in msg.walk():
                        tipo_content = parte.get_content_type()
                        if tipo_content == "text/plain":
                            try:
                                corpo_raw = parte.get_payload(decode=True)
                                try:
                                    corpo = corpo_raw.decode('utf-8')
                                except UnicodeDecodeError:
                                    try:
                                        corpo = corpo_raw.decode('latin1')
                                    except Exception as e:
                                        print(f"Erro ao decodificar corpo do email com latin1: {e}")
                                        corpo = ""
                            except Exception as e:
                                print(f"Erro ao decodificar parte do email: {e}")
                                corpo = ""
                else:
                    try:
                        corpo_raw = msg.get_payload(decode=True)
                        try:
                            corpo = corpo_raw.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                corpo = corpo_raw.decode('latin1')
                            except Exception as e:
                                print(f"Erro ao decodificar corpo do email com latint1: {e}")
                                corpo = ""
                    except Exception as e:
                        print(f"Erro ao decodificar o corpo do email: {e}")
                        corpo = ""

                PALAVRAS_NIVEL = ['iniciante', 'junior', 'nível básico', 'estágio']
                PALAVRAS_TECNOLOGIA = ['python', 'sql', 'dados', 'power bi', 'excel']
                PALAVRAS_CONTEXTO = ['projeto', 'freela', 'vaga', 'remoto', 'analista']

                texto_completo = f"{assunto.lower()} {corpo.lower()}"

                nivel_ok =any(p in texto_completo for p in PALAVRAS_NIVEL)

                tecnologia_ok =any(p in texto_completo for p in PALAVRAS_TECNOLOGIA)

                contexto_ok =any(p in texto_completo for p in PALAVRAS_CONTEXTO)
                print("\n--- DEBUG ---")
                print("Assunto:", assunto)
                print("Corpo (trecho):", corpo[:200])
                print("Texto completo:", texto_completo)
                print("Nível OK?", nivel_ok)
                print("Tecnologia OK?", tecnologia_ok)
                print("Contexto OK?", contexto_ok)
                print("----------------\n")

                if nivel_ok and tecnologia_ok and contexto_ok:
                    corpo_limpo = limpar_html(corpo)
                    emails_filtrados.append({"assunto": assunto, "corpo": corpo_limpo})
                    resumo += f"Assunto: {assunto}\n\n{'-'*50}\n"
    mail.logout()
    return emails_filtrados, resumo
