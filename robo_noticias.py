import feedparser
import requests
import re

def atualizar_site():
    print("Iniciando varredura pela Lagum...\n")
    
    # ---------------------------------------------------------
    # 1. NOTÍCIAS
    # ---------------------------------------------------------
    rss_url = "https://news.google.com/rss/search?q=Banda+Lagum&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(rss_url)
    
    noticias_ordenadas = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
    html_noticias = ""
    for entrada in noticias_ordenadas[:6]:
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
    # 2. BOT DO YOUTUBE
    # ---------------------------------------------------------
    url_canal = "https://www.youtube.com/@LagumOficial"
    html_yt = requests.get(url_canal).text
    match = re.search(r'href="(https://www.youtube.com/feeds/videos\.xml\?channel_id=[^"]+)"', html_yt)
    
    html_youtube = ""
    if match:
        rss_yt = match.group(1)
        feed_yt = feedparser.parse(rss_yt)
        ultimo_video = feed_yt.entries[0] 
        id_video = ultimo_video.link.split("v=")[-1]
        capa_yt = f"https://img.youtube.com/vi/{id_video}/hqdefault.jpg"
        
        html_youtube = f"""
        <div class="card" style="border-left-color: #ff0000;">
            <img src="{capa_yt}" style="width:100%; border-radius:12px; margin-bottom: 15px;" alt="Capa do Vídeo">
            <p style="margin-top:0;"><strong>{ultimo_video.title}</strong></p>
            <a href="{ultimo_video.link}" target="_blank" style="color: #ff0000; background-color: #ffeaea; padding: 5px 15px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">Assistir no YouTube &rarr;</a>
        </div>
        """

    # ---------------------------------------------------------
    # 3. LANÇAMENTO MUSICAL (Spotify)
    # ---------------------------------------------------------
    url_itunes = "https://itunes.apple.com/search?term=lagum&attribute=artistTerm&entity=musicTrack&limit=15&sort=recent"
    resposta = requests.get(url_itunes).json()
    
    html_lancamento = "<div class='card'><p>Nenhum lançamento recente encontrado.</p></div>"
    
    if resposta['resultCount'] > 0:
        for musica in resposta['results']:
            if musica['artistName'].lower() == 'lagum':
                capa = musica['artworkUrl100'].replace('100x100bb', '400x400bb') 
                nome_musica = musica['trackName']
                
                # Sequestro de rota: Cria o link direto para buscar no Spotify
                busca_formatada = nome_musica.replace(" ", "%20") + "%20Lagum"
                link_spotify = f"https://open.spotify.com/search/{busca_formatada}"
                
                html_lancamento = f"""
                <div class="card" style="border-left-color: #1DB954;">
                    <img src="{capa}" style="width:100%; border-radius:12px; margin-bottom: 15px;" alt="Capa">
                    <p style="margin-top:0;"><strong>{nome_musica}</strong></p>
                    <p style="font-size: 0.9rem; color: gray;">{musica['collectionName']}</p>
                    <a href="{link_spotify}" target="_blank" style="color: white; background-color: #1DB954; padding: 8px 15px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">Ouvir no Spotify &rarr;</a>
                </div>
                """
                break

    # ---------------------------------------------------------
    # 4. AGENDA DE SHOWS (O erro estava aqui!)
    # ---------------------------------------------------------
    shows = [
        {"data": "17 de Out", "local": "Arena Hall, BH"},
        {"data": "07 de Nov", "local": "Qualistage, RJ"},
        {"data": "28 de Nov", "local": "Ulysses C. Convenções, BSB"}
    ]
    
    html_shows = ""
    for show in shows:
        html_shows += f"<li><strong>{show['data']}</strong> - {show['local']}</li>\n"

    # ---------------------------------------------------------
    # 5. INJETANDO TUDO NO TEMPLATE
    # ---------------------------------------------------------
    with open("template.html", "r", encoding="utf-8") as arquivo:
        template = arquivo.read()
        
    template = template.replace("{{ lista_de_noticias }}", html_noticias)
    template = template.replace("{{ secao_youtube }}", html_youtube)
    template = template.replace("{{ secao_lancamento }}", html_lancamento)
    template = template.replace("{{ lista_de_shows }}", html_shows)
    
    with open("index.html", "w", encoding="utf-8") as arquivo_final:
        arquivo_final.write(template)
        
    print("Sucesso! Site atualizado com Spotify e agenda completa.")

if __name__ == "__main__":
    atualizar_site()