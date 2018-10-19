# -*- coding: utf-8 -*-
from collections import defaultdict
from string import punctuation

from bs4 import BeautifulSoup
from googlesearch import search
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import spacy
import re
import urllib3 as urlb
from spacy.tests.pipeline.test_pipe_methods import nlp

# from urllib.request import Request, urlopen
urlb.disable_warnings(urlb.exceptions.InsecureRequestWarning)
nlp = spacy.load('pt_core_news_sm')

TIPO_SITE_CONCORRENTE = "CC"
TIPO_SITE_PESSOAL = "PS"

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class Site(object):
    
    def __init__(self, sopa, url, palavra_chave, tipo_site=TIPO_SITE_CONCORRENTE):
        self.sopa = sopa
        self.url = url
        self.texto_artigo = ""
        self.paragrafos = []
        self.palavra_chave = palavra_chave
        self.palavras_sem_stopwords = []
        self.tipo_site = tipo_site
        self.total_de_palavras = 0
        self.subtitulos_h2 = []
        self.obter_paragrafos_tag_artigo()
    
    """
    Obtem a distancia media da palavra chave no texto
    """

    def obter_distancia_media_palavra_chave(self):
        
        chaves = word_tokenize(self.palavra_chave)
        palavras = self.obter_palavras_do_texto()
        
        distancias = []
        
        i = 0
        contador = 0
        while len(palavras) != i:
        
            j = 0
            achou = False
            while len(chaves) != j:    
                if palavras[i + j] == chaves[j]:
                    j = j + 1
                    achou = True
                else:
                    achou = False
                    break
            
            if (achou):
                distancias.append(contador)
                contador = 0
            else:
                contador = contador + 1
            
            i += 1
    
        if sum(distancias) == 0 and len(distancias) ==0:
            return 0
    
        distancia_media = round((sum(distancias) / len(distancias)))
        return distancia_media
    
    """
    Retorna sentenção (Frases) do texto
    """

    def obter_sentencas_do_texto(self):
        lista = []
        for sentencas in sent_tokenize(self.texto_artigo):
            tmps = sentencas.split(".")
            for tmp in tmps:
                lista.append(tmp)
        
        return lista
    
    def obter_frequencia_palavras_stopwords(self, total=40):
        fdist = nltk.FreqDist(self.obter_palavras_sem_stopwords())
        return fdist.most_common(total)
    
    def obter_frequencia_palavras(self, total=40):
        fdist = nltk.FreqDist(self.obter_palavras_do_texto())
        return fdist.most_common(total)
    
    """
    Verifica a similaridade geral do Texto com a palavra chave
    """

    def obter_similaridade_geral_do_texto(self):
        doc_chave = nlp(self.palavra_chave)
        doc_texto = nlp(self.obter_artigo_texto())
        similaridade = doc_chave.similarity(doc_texto)
        return float(round(similaridade, 2))
        
    """
    Obtem frequencia de palavras com a maior similaridade com a palavra chave
    """

    def obter_frequencia_com_maior_similaridade(self, total=50, valor_similaridade=0.4):
        
        lista_dados = []
        
        doc_chave = nlp(self.palavra_chave)
        
        for palavra, frequencia in self.obter_frequencia_palavras_stopwords(total):
            doc_palavra = nlp(palavra)
            if palavra not in self.palavra_chave:
                similaridade = doc_chave.similarity(doc_palavra)
                
                if similaridade > valor_similaridade:
                    lista_dados.append([palavra, frequencia, float(round(similaridade, 2))])
        
        return lista_dados
    
    """
    Retorna todos os paragrafos <P> Que estão dentro do <article>
    """

    def obter_paragrafos_tag_artigo(self):
        
        artigo = self.sopa.find("body")
        if artigo != None:
           ps = artigo.find_all("p")
           for p in ps:
               if p != None and len(p.text.strip()) > 0: 
                   self.texto_artigo = self.texto_artigo + p.text
                   self.paragrafos.append(p.text.strip())
    
        self.texto_artigo = self.texto_artigo.lower()
        return self.paragrafos
    
    def obter_titulo_h1(self):
        
        lista = []
        doc_chave = nlp(self.palavra_chave)
        
        similaridade = 0
        artigo = self.sopa.find("body")
        h1 = "- - - - - - - "
        if artigo != None:
           h1 = artigo.find("h1")
           doc_titulo = nlp(h1.text.strip())
           similaridade = doc_chave.similarity(doc_titulo)
    
        return str([h1.text.strip(),round(similaridade,2)])
    
    
    def obter_subtitulos_h2(self):
        artigo = self.sopa.find("body")
        if artigo != None:
           h2s = artigo.find_all("h2")
           for h2 in h2s:
               if h2 != None and len(h2.text.strip()) > 0: 
                   self.subtitulos_h2.append(h2.text.strip())
    
        return self.subtitulos_h2
    
    """
    Retorna uma lista de palavras com o stopWord removido
    """

    def obter_palavras_sem_stopwords(self):
        
        from nltk.corpus import stopwords
        
        palavras = word_tokenize(self.texto_artigo.lower())
        stopwords = set(stopwords.words('portuguese') + list(punctuation))
        stopwords.add('“')
        stopwords.add('”')
        self.palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
        return self.palavras_sem_stopwords
    
    """
    Obtem a densidade da palavra chave no texto
    """

    def obter_densidade_da_palavra_chave(self):
        
        total_palavras_texto = self.obter_total_de_palavras()
        
        chaves = word_tokenize(self.palavra_chave)
        palavras = self.obter_palavras_do_texto()
        
        distancias = []
        contador = 0
        
        i = 0
        contador = 0
        while len(palavras) != i:
        
            j = 0
            achou = False
            while len(chaves) != j:    
                if palavras[i + j] == chaves[j]:
                    j = j + 1
                    achou = True
                else:
                    achou = False
                    break
            
            if (achou):
                distancias.append(contador)
                contador = 0
            else:
                contador = contador + 1
            
            i += 1
    
#         print("DISTANCIA %s : %s" % (str(distancias), total_palavras_texto))
            
        densidade = ((len(distancias) / total_palavras_texto) * 100)
        return densidade
    
    def obter_palavras(self):
        from nltk.corpus import stopwords
        
        palavras = word_tokenize(self.texto_artigo.lower())
        stopwords = set(list(punctuation))
        stopwords.add('“')
        stopwords.add('”')
        palavras = [palavra for palavra in palavras if palavra not in stopwords]
        return palavras
    
    """
    Retorna uma lista de palavras que contem no corpo do artigo
    """

    def obter_palavras_do_texto(self):
        return word_tokenize(self.texto_artigo.lower())
    
    def obter_artigo_texto(self):
        return self.texto_artigo.lower()
    
    """
    Obtem o total de palavras do texto
    """

    def obter_total_de_palavras(self):
        
        self.total_de_palavras = len(self.obter_palavras())
        return self.total_de_palavras

    
class Sites(object):
    
    def __init__(self, palavra_chave, urls=[], texto_artigos="", criar_sites=True):
        self.palavra_chave = palavra_chave.lower().strip()        
        self.urls = urls
        self.sites = []
        self.texto_artigos = texto_artigos
        self.palavras_sem_stopwords = []
        
        if criar_sites:
            self.criar_todos_os_sites()
            
    def obter_lista_urls(self):
        
        if len(self.palavra_chave) == 0:
            return []

        
        print("QTD URL %s" % len(self.urls))
        if len(self.urls) == 1:
            return self.urls
        
        for url in search(self.palavra_chave, tld='com', lang='pt', stop=10):
            url = url.split("#")[0]
            self.urls.append(url)
        return set(self.urls)
    
    """
    Concatena os textos de todos os artigos indexados
    """

    def obter_texto_artigos(self):
        
        self.texto_artigos = ""
        
        for site in self.sites:
            self.texto_artigos = self.texto_artigos + site.obter_artigo_texto()
        
        return self.texto_artigos.lower()
    
    """
    Retorna sentenção (Frases) do texto
    """

    def obter_sentencas_dos_textos(self):
        lista = []
        for sentencas in sent_tokenize(self.obter_texto_artigos()):
            tmps = sentencas.split(".")
            for tmp in tmps:
                lista.append(tmp)
        
        return lista
    
    """
    Retorna um lista de objetos de sites
    """

    def obter_sites_indexados(self):
        return self.sites
    
    """
    Retorna uma lista de palavras que contem no corpo do artigo
    """

    def obter_palavras_dos_textos(self):
        return word_tokenize(self.obter_texto_artigos())
    
    """
    Retorna uma lista de palavras com o stopWord removido
    """

    def obter_palavras_sem_stopwords(self):
        
        from nltk.corpus import stopwords
        
        palavras = word_tokenize(self.obter_texto_artigos())
        stopwords = set(stopwords.words('portuguese') + list(punctuation))
        stopwords.add('“')
        stopwords.add('”')
        self.palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
        return self.palavras_sem_stopwords
    
    """
    Retorna a frequencia de distribuição de palavras sem stopWords
    """

    def obter_frequencia_palavras_stopwords(self, total=40):
        fdist = nltk.FreqDist(self.obter_palavras_sem_stopwords())
        return fdist.most_common(total)
    
    """
    Retorna a frequencia de distribuição de palavras
    """

    def obter_frequencia_palavras(self, total=40):
        fdist = nltk.FreqDist(self.obter_palavras_sem_stopwords())
        return fdist.most_common(total)
    
    """
    Cria todos os sites que possui a tag article
    """

    def criar_todos_os_sites(self):
        
        print("CRIANDO SITES %s" % self.palavra_chave)
        urls = self.obter_lista_urls()
        
        contador = 0
        for url in urls:
            print("URL %s" % url)
            sopa = self.obter_sopa_site(url)
            artigo = sopa.find("body")
            if artigo != None:
                ps = artigo.find_all("p")
                if ps != None and len(ps) > 10:
                    site = Site(sopa, url, self.palavra_chave)
                    if self.palavra_chave in site.obter_artigo_texto():
                        self.sites.append(site)
                        contador += 1
                        if contador == 5:
                            break
#             else:
#                 artigo = sopa.find(class_="content")
#                 if artigo != None:
#                     ps = artigo.find_all("p")
#                     if ps != None and len(ps) > 10:
#                         site = Site(sopa, url, self.palavra_chave)
#                         if self.palavra_chave in site.obter_artigo_texto():
#                             self.sites.append(site)
        return self
    
    """
    Retorna as sentencas mais similares as palavras chaves
    """

    def obter_setencas_similares(self, valor_similaridade=0.4, palavra_chave_local=None, verifica_chave=True):
        
        if (palavra_chave_local != None):
            palavra_chave = palavra_chave_local
            doc_chave = nlp(palavra_chave_local)
        else:
            palavra_chave = self.palavra_chave
            doc_chave = nlp(self.palavra_chave)
        lista = []
        for sentenca in self.obter_sentencas_dos_textos():
            doc_sentenca = nlp(sentenca)
            similaridade = doc_chave.similarity(doc_sentenca)
            
            if similaridade > valor_similaridade:
                
                if verifica_chave:
                    if palavra_chave in sentenca:
                        lista.append([sentenca, similaridade])
                else:
                    lista.append([sentenca, similaridade])
                
        return lista

    """
    Retorna a densidade média de palavras chave
    """

    def obter_densidade_media_de_palavra_chave(self):
        
        soma = 0
        for site in self.sites:
            soma = soma + site.obter_densidade_da_palavra_chave()
            
        return (soma / len(self.sites))

    """
    Retorna a distancia média da palavras
    """

    def obter_distancia_media_palavra_chave(self):
        soma = 0
        for site in self.sites:
            soma = soma + site.obter_distancia_media_palavra_chave()
        
        return (soma / len(self.sites))
    
    """
    obter a quantidade média de palavras para o texto
    """

    def obter_quantidade_media_palavras_para_texto(self):
        soma = 0
        for site in self.sites:
            soma = soma + site.obter_total_de_palavras()
        
        return (soma / len(self.sites))
    
    """
    Obter a similaridade média
    """
    def obter_similaridade_media_documento(self):
        soma = 0
        for site in self.sites:
            soma = soma + site.obter_similaridade_geral_do_texto()
        
        return (soma / len(self.sites))
    
    """
    Retorna temas importantes para falar relacionados a palavra chave
    """

    def obter_temas_importantes(self):
        
        lista_h2_todos = set()
        for site in self.obter_sites_indexados():
            for h2 in site.obter_subtitulos_h2():
                lista_h2_todos.add(h2.lower().strip())   
        
        lista_h2_usar = set()
        doc_chave = nlp(self.palavra_chave)
        
#         for h2 in lista_h2_todos:
#             for h2_tp in lista_h2_todos:
#                 doc1 = nlp(h2)
#                 doc2 = nlp(h2_tp)
#                 similiaridade = doc1.similarity(doc2)
#                 if similiaridade < 0.8:
#                     similiaridade = doc_chave.similarity(doc1)
#                     print(similiaridade)
#                     if similiaridade >= 0.6:
#                         lista_h2_usar.add(h2)
        lista_retorno = []
        for h2 in lista_h2_todos:
            doc1 = nlp(h2)
            similiaridade = doc_chave.similarity(doc1)
            
            if similiaridade > 0.48 and len(h2.split()) >= 3 :
                lista_retorno.append([h2, similiaridade])
        
        return lista_retorno
        
    """
    Retorna o objeto SOAP do site
    """

    def obter_sopa_site(self, url):
        http = urlb.PoolManager()
        dados_pagina = http.request('get', url)
        return BeautifulSoup(dados_pagina.data, "lxml")
        
