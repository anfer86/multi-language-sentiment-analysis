# Projeto multi-language-sentimento-analysis

Este projeto tem como objetivos explorar:
- Captura de avaliações de aplicativos do Google Play Store via webscrapping com Selenium e google-play-scrapper ([link](../blob/master/data/app_scrapping.py)).
- Utilização do modelo BERT para representação de sentenças e construção de um classificador multilingue para análise de sentimentos: revisões positivas e negativas ([link](../blob/master/model/exploring_bert.ipynb)).
- Construção de uma API em Flask que permite classificar sentenças e uma página web simples que usa essa API via requisição assíncrona com Javascript/JQuery.