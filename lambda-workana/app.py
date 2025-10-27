import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

# ===========================================================
# Carrega variáveis do arquivo .env
# ===========================================================
load_dotenv()

# ===========================================================
# CONFIGURAÇÕES BÁSICAS
# ===========================================================

# Palavras-chave de busca
KEYWORDS = [
    "frontend", "front end", "html", "css", "javascript", "react", "vue", "angular",
    "backend", "back end", "python", "django", "flask", "node", "express",
    "api", "fullstack", "full stack", "typescript", "php", "laravel",
    "mysql", "postgresql", "sql", "nosql", "mongo",
    "data", "analise de dados", "data science", "machine learning", "pandas"
]

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
DEST_EMAIL = os.getenv("DEST_EMAIL")

# ===========================================================
# FUNÇÕES PRINCIPAIS
# ===========================================================

def coletar_projetos():
    """Coleta os projetos mais recentes da Workana filtrando por palavras-chave."""
    resultados = []
    url = "https://www.workana.com/jobs?language=pt&category=it-programming"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return resultados

    html = response.text.lower()

    for palavra in KEYWORDS:
        if palavra.lower() in html:
            resultados.append(palavra)

    return list(set(resultados))  # remove duplicados


# def enviar_email(projetos):
    """Envia o resumo por e-mail."""
    if not projetos:
        body = "Nenhum projeto novo encontrado hoje 😕"
    else:
        body = "<h2>Novos projetos relacionados encontrados no Workana:</h2><ul>"
        for p in projetos:
            body += f"<li>{p}</li>"
        body += "</ul>"

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = DEST_EMAIL
    msg["Subject"] = f"Novos projetos Workana — {datetime.now().strftime('%d/%m/%Y')}"

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, DEST_EMAIL, msg.as_string())

    print(f"E-mail enviado para {DEST_EMAIL} com {len(projetos)} projetos.")


def lambda_handler(event=None, context=None):
    """Handler padrão do AWS Lambda."""
    print("Iniciando busca de projetos Workana...")
    projetos = coletar_projetos()
    # enviar_email(projetos)
    return {"statusCode": 200, "body": f"{len(projetos)} projetos enviados por e-mail."}


if __name__ == "__main__":
    lambda_handler()
