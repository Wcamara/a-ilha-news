import feedparser
import requests
import re
import random

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
        
        # Trava de segurança: Verifica se a lista não está vazia antes de acessar o índice [0]
        if len(feed_yt.entries) > 0:
            ultimo_video = feed_yt.entries[0] 
            id_video = ultimo_video.link.split("v=")[-1]
            capa_yt = f"https://img.youtube.com/vi/{id_video}/hqdefault.jpg"
            
            html_youtube = f"""
            <div class="card" style="border-left-color: #ff0000;">
                <img src="{capa_yt}" style="width:100%; border-radius:12px; margin-bottom: 15px;" alt="Capa">
                <p style="margin-top:0;"><strong>{ultimo_video.title}</strong></p>
                <a href="{ultimo_video.link}" target="_blank" style="color: white; background-color: #ff0000; padding: 5px 15px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">Assistir no YouTube &rarr;</a>
            </div>
            """
        else:
            html_youtube = "<div class='card'><p>Vídeo mais recente temporariamente indisponível.</p></div>"

    # ---------------------------------------------------------
    # 3. LETRA DO DIA (Sorteador automático)
    # ---------------------------------------------------------
    letras = [
        '"Deixa o vento bater, o cabelo voar, deixa o tempo dizer..."',
        '"Seja o que eu quiser, eu não vou fugir..."',
        '"Ninguém me ensinou a viver assim, eu fui aprendendo..."',
        '"Hoje eu quero me perder pra me encontrar..."',
        '"Eu não sou de fazer planos, mas contigo eu faço..."'
    ]
    letra_do_dia = random.choice(letras)

    # ---------------------------------------------------------
    # 4. AGENDA DE SHOWS E MOTOR DO CONTADOR
    # ---------------------------------------------------------
    shows = [
        {"data": "17 de Out", "local": "Arena Hall, BH", "data_js": "Oct 17, 2026 20:00:00"},
        {"data": "07 de Nov", "local": "Qualistage, RJ", "data_js": "Nov 07, 2026 20:00:00"},
        {"data": "28 de Nov", "local": "Ulysses C. Convenções, BSB", "data_js": "Nov 28, 2026 20:00:00"}
    ]
    
    html_shows = ""
    for show in shows:
        html_shows += f"<li><strong>{show['data']}</strong> - {show['local']}</li>\n"
        
    data_proximo_show = shows[0]["data_js"]

    # ---------------------------------------------------------
    # 5. INJETANDO TUDO NO TEMPLATE
    # ---------------------------------------------------------
    with open("template.html", "r", encoding="utf-8") as arquivo:
        template = arquivo.read()
        
    template = template.replace("{{ lista_de_noticias }}", html_noticias)
    template = template.replace("{{ secao_youtube }}", html_youtube)
    template = template.replace("{{ lista_de_shows }}", html_shows)
    template = template.replace("{{ letra_do_dia }}", letra_do_dia)
    template = template.replace("{{ data_proximo_show }}", data_proximo_show)
    
    with open("index.html", "w", encoding="utf-8") as arquivo_final:
        arquivo_final.write(template)
        
    print("Sucesso! Site atualizado com Modo Escuro, Contador, Letras e Comentários.")

if __name__ == "__main__":
    atualizar_site()