import re
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDENTIALS_PATH, EMAIL_USUARIO
from datetime import datetime

def limpar_html(texto):
    texto_sem_tags = re.sub(r"<.*?>", "", texto)
    return texto_sem_tags

def exportar_para_google_sheets(emails_filtrados):
    if not emails_filtrados:
        print("Nenhum email para exportar para o Google Sheets.")
        return
    try:
        escopos = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"
        ]
        credenciais = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH,scopes=escopos)
        cliente = gspread.authorize(credenciais)

        nome_planilha = f"Emails Filtrados - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        planilha = cliente.create(nome_planilha)
        planilha.share(EMAIL_USUARIO, perm_type='user', role='writer')

        aba = planilha.sheet1
        aba.append_row(["Assunto", "Corpo"])

        for email in emails_filtrados:
            corpo_limpo = limpar_html(email["corpo"])
            corpo_limitado = corpo_limpo[:5000]
            aba.append_row([email["assunto"],corpo_limitado])
        print("Exportado para o Google Sheets com sucesso!")
    except Exception as e:
        print(f"Erro ao exportar para o Google Sheets: {e}")
