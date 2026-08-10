import feedparser
import requests

def atualizar_site():
    print("Buscando novidades na ilha...\n")
    
    # ---------------------------------------------------------
    # 1. BUSCANDO MÚLTIPLAS NOTÍCIAS (Agora buscando 6)
    # ---------------------------------------------------------
    rss_url = "https://news.google.com/rss/search?q=Banda+Lagum&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(rss_url)
    
    html_noticias = ""
    
    # Pegando as 6 notícias mais recentes. O feed já faz a rotação automática!
    for entrada in feed.entries[:6]:
        html_noticias += f"""
        <article class="card">
            <small>Atualizado em: {entrada.published[5:22]}</small>
            <h3>{entrada.title}</h3>
            <p>Confira os detalhes desta matéria clicando no link abaixo.</p>
            <a href="{entrada.link}" target="_blank">Ler matéria completa &rarr;</a>
        </article>
        """

    # ---------------------------------------------------------
    # 2. BUSCANDO O ÚLTIMO LANÇAMENTO (API do iTunes)
    # ---------------------------------------------------------
    url_itunes = "https://itunes.apple.com/search?term=banda+lagum&entity=musicTrack&limit=1&sort=recent"
    resposta = requests.get(url_itunes).json()
    
    html_lancamento = ""
    
    if resposta['resultCount'] > 0:
        musica = resposta['results'][0]
        capa = musica['artworkUrl100'].replace('100x100bb', '400x400bb') 
        
        html_lancamento = f"""
        <div class="card">
            <img src="{capa}" style="width:100%; border-radius:12px; margin-bottom: 15px;" alt="Capa do Lançamento">
            <p style="margin-top:0;"><strong>{musica['trackName']}</strong></p>
            <p style="font-size: 0.9rem; color: gray;">{musica['collectionName']}</p>
            <a href="{musica['trackViewUrl']}" target="_blank">Ouvir Agora &rarr;</a>
        </div>
        """
    else:
        html_lancamento = "<div class='card'><p>Nenhum lançamento recente encontrado.</p></div>"

    # ---------------------------------------------------------
    # 3. GERENCIANDO A AGENDA DE SHOWS
    # ---------------------------------------------------------
    # Edite esta lista no futuro sempre que quiser adicionar novos shows
    shows = [
        {"data": "17 de Out", "local": "Arena Hall, BH"},
        {"data": "07 de Nov", "local": "Qualistage, RJ"},
        {"data": "28 de Nov", "local": "Ulysses C. Convenções, BSB"}
    ]
    
    html_shows = ""
    for show in shows:
        html_shows += f"<li><strong>{show['data']}</strong> - {show['local']}</li>\n"

    # ---------------------------------------------------------
    # 4. INJETANDO TUDO NO TEMPLATE
    # ---------------------------------------------------------
    with open("template.html", "r", encoding="utf-8") as arquivo:
        template = arquivo.read()
        
    template = template.replace("{{ lista_de_noticias }}", html_noticias)
    template = template.replace("{{ secao_lancamento }}", html_lancamento)
    template = template.replace("{{ lista_de_shows }}", html_shows)
    
    with open("index.html", "w", encoding="utf-8") as arquivo_final:
        arquivo_final.write(template)
        
    print("Sucesso! Site atualizado com 6 notícias, lançamentos e agenda limpa.")

if __name__ == "__main__":
    atualizar_site()