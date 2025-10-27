from requests_html import HTMLSession
import logging

# Silencia warnings do Pyppeteer
logging.getLogger('pyppeteer').setLevel(logging.ERROR)

url = "https://www.workana.com/jobs?category=it-programming"

session = HTMLSession()
response = session.get(url)

# Renderiza a página completa — aumenta o tempo para o JS carregar tudo
response.html.render(timeout=90, sleep=10, keep_page=True)

projetos = []

# Pega todos os cards de projetos
for card in response.html.find("div.project-item"):
    titulo_tag = card.find("h2.project-title a", first=True)

    # tenta pegar o preço pelos seletores conhecidos
    preco_tag = (
        card.find("div.project-budget span.values", first=True)
        or card.find("span[class*=budget]", first=True)
    )

    if titulo_tag:
        titulo = titulo_tag.text.strip()
        link = "https://www.workana.com" + titulo_tag.attrs["href"]
        preco = preco_tag.text.strip() if preco_tag else "Sem valor"

        projetos.append({
            "titulo": titulo,
            "link": link,
            "preco": preco
        })

# Exibe o resultado
print(f"✅ {len(projetos)} projetos encontrados.\n")

for p in projetos[:10]:  # mostra só os 10 primeiros
    print(f"- {p['titulo']} | {p['preco']}")
    print(p['link'])
    print()

def lambda_handler(event=None, context=None):
    print("✅ Lambda executada com sucesso!")
    return {
        "statusCode": 200,
        "body": "Lambda funcionando localmente!"
    }