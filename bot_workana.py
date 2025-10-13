from requests_html import HTMLSession

url = "https://www.workana.com/jobs?category=it-programming"

session = HTMLSession()
response = session.get(url)
response.html.render(timeout=30, sleep=2)

projetos = []

# Pega todos os cards de projetos
for card in response.html.find("div.project-item"):
    titulo_tag = card.find("h2.project-title a", first=True)
    preco_tag = card.find("div.project-budget span", first=True)

    if titulo_tag:
        titulo = titulo_tag.text.strip()
        link = "https://www.workana.com" + titulo_tag.attrs["href"]
        preco = preco_tag.text.strip() if preco_tag else "Sem valor"

        projetos.append({
            "titulo": titulo,
            "link": link,
            "preco": preco
        })

print(f"✅ {len(projetos)} projetos encontrados.")
for p in projetos[:5]:  # mostra só os 5 primeiros
    print(f"- {p['titulo']} | {p['preco']}")
    print(f"  {p['link']}")
