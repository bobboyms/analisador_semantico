# -*- coding: utf-8 -*-
import spacy
from verifica_artigo.busca_artigos import Sites
from toolz.itertoolz import frequencies
#from app.regras_de_negocio import sites, palavra_chave, urls

# nlp = spacy.load('pt_core_news_sm')
# 
# def main():
#     
#     sites = Sites(palavra_chave="Matriz BCG")
#     
#     for site in sites.obter_sites_indexados():
#         print(site.url)
# 
# if __name__ == "__main__":
#    main()