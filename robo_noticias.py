import feedparser

# URL do RSS do Google News focado na Lagum
rss_url = "https://news.google.com/rss/search?q=Banda+Lagum&hl=pt-BR&gl=BR&ceid=BR:pt-419"

def atualizar_site():
    print("Buscando novidades na ilha...\n")
    feed = feedparser.parse(rss_url)
    
    # Pegando a notícia mais recente (a primeira da lista)
    noticia_recente = feed.entries[0]
    titulo = noticia_recente.title
    link = noticia_recente.link
    
    # O Google News retorna datas em um formato longo, vamos usar como vem no feed para simplificar
    data = noticia_recente.published 
    
    print(f"Notícia encontrada: {titulo}")
    print("Injetando dados no HTML...")
    
    # Abrindo e lendo o nosso molde (template)
    with open("template.html", "r", encoding="utf-8") as arquivo:
        html_conteudo = arquivo.read()
        
    # Substituindo as tags (marcadores) pelos dados reais
    html_conteudo = html_conteudo.replace("{{ titulo_noticia }}", titulo)
    html_conteudo = html_conteudo.replace("{{ link_original }}", link)
    html_conteudo = html_conteudo.replace("{{ data_noticia }}", data)
    
    # O RSS do Google nem sempre manda um resumo limpo, então colocamos uma chamada padrão
    html_conteudo = html_conteudo.replace("{{ resumo_noticia }}", "Confira os detalhes desta matéria clicando no link abaixo.") 

    # Salvando o resultado em um novo arquivo index.html pronto para ir ao ar
    with open("index.html", "w", encoding="utf-8") as arquivo_final:
        arquivo_final.write(html_conteudo)
        
    print("\nSucesso! O arquivo index.html foi gerado e o site está atualizado.")

if __name__ == "__main__":
    atualizar_site()