import feedparser
import requests
import re

def atualizar_site():
    print("Iniciando varredura pela Lagum...\n")
    
    # ---------------------------------------------------------
    # 1. NOTÍCIAS (Ordenadas e com Manchetes Limpas)
    # ---------------------------------------------------------
    rss_url = "https://news.google.com/rss/search?q=Banda+Lagum&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(rss_url)
    
    # Força a lista a ser ordenada por data (reverse=True = Mais nova no topo)
    noticias_ordenadas = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
    
    html_noticias = ""
    for entrada in noticias_ordenadas[:6]:
        # Limpeza da manchete: Corta fora o nome do site que o Google anexa no final
        pedacos = entrada.title.split(" - ")
        titulo_limpo = " - ".join(pedacos[:-1]) if len(pedacos) > 1 else entrada.title
        
        html_noticias += f"""
        <article class="card">
            <small>Atualizado em: {entrada.published[5:22]}</small>
            <h3>{titulo_limpo}</h3>
            <p>Confira os detalhes clicando no link abaixo.</p>
            <a href="{entrada.link}" target="_blank">Ler matéria completa &rarr;</a>
        </article>
        """

    # ---------------------------------------------------------
    # 2. BOT DO YOUTUBE (Scraping com Regex)
    # ---------------------------------------------------------
    # Acessa a página oficial e caça o link do RSS de vídeos oculto no código
    url_canal = "https://www.youtube.com/@LagumOficial"
    html_yt = requests.get(url_canal).text
    
    match = re.search(r'href="(https://www.youtube.com/feeds/videos\.xml\?channel_id=[^"]+)"', html_yt)
    
    html_youtube = ""
    if match:
        rss_yt = match.group(1)
        feed_yt = feedparser.parse(rss_yt)
        
        # Pega o primeiríssimo vídeo (Lançamento)
        ultimo_video = feed_yt.entries[0] 
        id_video = ultimo_video.link.split("v=")[-1]
        capa_yt = f"https://img.youtube.com/vi/{id_video}/hqdefault.jpg"
        
        html_youtube = f"""
        <div class="card" style="border-left-color: #ff0000;">
            <img src="{capa_yt}" style="width:100%; border-radius:12px; margin-bottom: 15px;" alt="Capa do Vídeo">
            <p style="margin-top:0;"><strong>{ultimo_video.title}</strong></p>
            <a href="{ultimo_video.link}" target="_blank" style="color: #ff0000; background-color: #ffeaea;">Assistir no YouTube &rarr;</a>
        </div>
        """

    # ---------------------------------------------------------
    # 3. LANÇAMENTO MUSICAL E SHOWS
    # ---------------------------------------------------------
    url_itunes = "https://itunes.apple.com/search?term=banda+lagum&entity=musicTrack&limit=1&sort=recent"
    resposta = requests.get(url_itunes).json()
    
    html_lancamento = ""
    if resposta['resultCount'] > 0:
        musica = resposta['results'][0]
        capa = musica['artworkUrl100'].replace('100x100bb', '400x400bb') 
        html_lancamento = f"""
        <div class="card" style="border-left-color: #1DB954;">
            <img src="{capa}" style="width:100%; border-radius:12px; margin-bottom: 15px;" alt="Capa">
            <p style="margin-top:0;"><strong>{musica['trackName']}</strong></p>
            <p style="font-size: 0.9rem; color: gray;">{musica['collectionName']}</p>
            <a href="{musica['trackViewUrl']}" target="_blank" style="color: #1DB954; background-color: #e8f8ee;">Ouvir Agora &rarr;</a>
        </div>
        """

    shows = [
        {"data": "17 de Out", "local": "Arena Hall, BH"},
        {"data": "07 de Nov", "local": "Qualistage, RJ"},
        {"data": "28 de Nov", "local": "Ulysses C. Convenções, BSB"}
    ]
    html_shows = ""
    for show in shows:
        html_shows += f"<li><strong>{show['data']}</strong> - {show['local']}</li>\n"

    # ---------------------------------------------------------
    # 4. INJETANDO NO TEMPLATE
    # ---------------------------------------------------------
    with open("template.html", "r", encoding="utf-8") as arquivo:
        template = arquivo.read()
        
    template = template.replace("{{ lista_de_noticias }}", html_noticias)
    template = template.replace("{{ secao_youtube }}", html_youtube)
    template = template.replace("{{ secao_lancamento }}", html_lancamento)
    template = template.replace("{{ lista_de_shows }}", html_shows)
    
    with open("index.html", "w", encoding="utf-8") as arquivo_final:
        arquivo_final.write(template)
        
    print("Sucesso! O Bot de Notícias e o Bot do YouTube trabalharam em conjunto.")

if __name__ == "__main__":
    atualizar_site()