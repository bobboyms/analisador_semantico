# coding: utf-8
import pickle
from app import app, flash, session
from flask import render_template, redirect, url_for
#from app.regras_de_negocio import sites
from app.models.formulario_principal import FormularioPrincipal
from app.models.formulario_texto import FormularioTexto
from verifica_artigo.busca_artigos import Sites, Site
from app.models import formulario_texto
from flask.globals import request

"""
Se se o objeto site ja foi criado para palavra, Retorna
"""
def obter_site(chave):
    dicionario = app.config['SITES_OBJECT']
    
    if (dicionario.get(chave) == None):
        print("NOVO SITE CRIADO %s" % chave)
        
        
        dicionario[chave] = Sites(palavra_chave=chave)
        
    sites = dicionario[chave]
    return sites

@app.route("/",methods=['POST','GET'])
def principal():
    
    formulario_principal = FormularioPrincipal()
    
    if formulario_principal.validate_on_submit():
        chave = formulario_principal.palavra_chave.data
        return redirect(url_for("analisador", chave=chave))
     
    return render_template("principal.html", form=formulario_principal)

@app.route("/analise", defaults={'chave' : None})
@app.route("/analise/<chave>", methods=['POST','GET'])
def analisador(chave):
    
    if chave != None:
        session['CHAVE'] = chave
    else:
        return redirect(url_for("principal"))
    
    sites = obter_site(chave)
    return render_template("analise.html",
                           palavra_chave=chave,
                           similares=sites.obter_setencas_similares(),
                           sites=sites.obter_sites_indexados(),
                           temas = sites.obter_temas_importantes(),
                           densidade_media_de_palavra_chave=sites.obter_densidade_media_de_palavra_chave(),
                           distancia_media_palavra_chave=sites.obter_distancia_media_palavra_chave(),
                           quantidade_media_palavras_para_texto=sites.obter_quantidade_media_palavras_para_texto(),
                           similaridade_media_documento=sites.obter_similaridade_media_documento())
    

@app.route("/verificar/palavra/", defaults={'chave' : None, 'palavra' : None, 'verifica' : None})
@app.route("/verificar/palavra/<chave>/<palavra>", methods=['POST','GET'])
def analisar_palavra_especifica(chave, palavra):
    
    if chave == None or palavra == None:
        return render_template("principal.html")
    
    sites = obter_site(chave) 
    return render_template("analise_especifica_palavra.html",
                           palavra_chave=palavra,
                           similares=sites.obter_setencas_similares(valor_similaridade=0.2, 
                                                                    palavra_chave_local=palavra))
 
@app.route("/analisar/texto/", methods=['POST','GET'])
def analisar_texto():
    
    chave = session['CHAVE']
    
    formulario_texto = FormularioTexto()
    
    if formulario_texto.validate_on_submit():
        url = formulario_texto.texto.data
        meu_site = Sites(palavra_chave=chave, urls=[url])
        sites = obter_site(chave) 

        
        
        return render_template("analisar_texto.html", form=formulario_texto,tem_informacoes=True,
                            meu_densidade_media_de_palavra_chave=meu_site.obter_densidade_media_de_palavra_chave(),
                            meu_distancia_media_palavra_chave=meu_site.obter_distancia_media_palavra_chave(),
                            meu_quantidade_media_palavras_para_texto=meu_site.obter_quantidade_media_palavras_para_texto(),
                            meu_similaridade_media_documento=meu_site.obter_similaridade_media_documento(),
                            densidade_media_de_palavra_chave=sites.obter_densidade_media_de_palavra_chave(),
                            distancia_media_palavra_chave=sites.obter_distancia_media_palavra_chave(),
                            quantidade_media_palavras_para_texto=sites.obter_quantidade_media_palavras_para_texto(),
                            similaridade_media_documento=sites.obter_similaridade_media_documento(),
                            listas=obter_lista_palavras_usadas(meu_site,sites),
                            palavra_chave=chave)
        
    return render_template("analisar_texto.html", form=formulario_texto)

def obter_lista_palavras_usadas(meu_site, sites):

    palavras = meu_site.obter_palavras_sem_stopwords()
    
    lista = []
    for palavra in sites.obter_frequencia_com_maior_similaridade():
        
        if palavra[0] in palavras:
            lista.append([palavra[0],palavra[1],palavra[2],"SIM"])
        else:
            lista.append([palavra[0],palavra[1],palavra[2],"NÃO"])

    return lista
