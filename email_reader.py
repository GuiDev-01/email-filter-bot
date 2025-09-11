import imaplib
import email
from email.header import decode_header
from config import EMAIL_USUARIO, SENHA_APP
import re

def limpar_html(texto):
    texto_sem_args = re.sub(r"<.*?>", "", texto)
    return texto_sem_args


def ler_emails():
    if not EMAIL_USUARIO or not SENHA_APP:
        print("EMAIL_USUARIO ou SENHA_APP não definidos. Verifique o .env.")
        return [], ""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(str(EMAIL_USUARIO), str(SENHA_APP))
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
                                if isinstance(corpo_raw, bytes):
                                    try:
                                        corpo = corpo_raw.decode('utf-8')
                                    except UnicodeDecodeError:
                                        try:
                                            corpo = corpo_raw.decode('latin1')
                                        except Exception as e:
                                            print(f"Erro ao decodificar corpo do email com latin1: {e}")
                                            corpo = ""
                                elif isinstance(corpo_raw, str):
                                    corpo = corpo_raw
                                else:
                                    corpo = str(corpo_raw)
                            except Exception as e:
                                print(f"Erro ao decodificar parte do email: {e}")
                                corpo = ""
                else:
                    try:
                        corpo_raw = msg.get_payload(decode=True)
                        if isinstance(corpo_raw, bytes):
                            try:
                                corpo = corpo_raw.decode('utf-8')
                            except UnicodeDecodeError:
                                try:
                                    corpo = corpo_raw.decode('latin1')
                                except Exception as e:
                                    print(f"Erro ao decodificar corpo do email com latin1: {e}")
                                    corpo = ""
                        elif isinstance(corpo_raw, str):
                            corpo = corpo_raw
                        else:
                            corpo = str(corpo_raw)
                    except Exception as e:
                        print(f"Erro ao decodificar o corpo do email: {e}")
                        corpo = ""

                PALAVRAS_CHAVE = [
                    'python', 'sql', 'dados', 'power bi', 'excel', 'projeto', 'freela', 'vaga', 'remoto', 'analista',
                    'iniciante', 'junior', 'nível básico', 'estágio', 'trabalho', 'oportunidade', 'desenvolvedor', 'estudante'
                ]

                texto_completo = f"{assunto.lower()} {corpo.lower()}"

                contem_palavra_chave = any(p in texto_completo for p in PALAVRAS_CHAVE)
                print("\n--- DEBUG ---")
                print("Assunto:", assunto)
                print("Corpo (trecho):", corpo[:200])
                print("Texto completo:", texto_completo)
                print("Contém palavra-chave?", contem_palavra_chave)
                print("----------------\n")

                if contem_palavra_chave:
                    corpo_limpo = limpar_html(corpo)
                    emails_filtrados.append({"assunto": assunto, "corpo": corpo_limpo})
                    resumo += f"Assunto: {assunto}\n\n{'-'*50}\n"
    mail.logout()
    return emails_filtrados, resumo
