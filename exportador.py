import csv
from datetime import datetime
import os

def exportar_csv(emails_filtrados):
    if not emails_filtrados:
        print(f'Nenhum email para exportar.')
        return
    
    nome_arquivo = f"emails_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    caminho_arquivo = os.path.join(os.getcwd(),nome_arquivo)

    try:
        with open(nome_arquivo, mode='w', newline='',encoding='utf-8') as arquivo:
            writer = csv.DictWriter(arquivo, fieldnames=["assunto", "corpo"])
            writer.writeheader()
            for email in emails_filtrados:
                writer.writerow(email)
        print(f"Exportado com sucesso para {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao exportar para CSV: {e}")
