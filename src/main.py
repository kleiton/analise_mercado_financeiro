import logging
from datetime import datetime

import pandas as pd

from scraping.scraping import Scraping
from gerar_pdf import CsvParaPdf
from modelos import MagicForm, ModelBazin, ModelGrahan
from util import Utils

if __name__ == "__main__":
    
    data_atual = datetime.now().strftime("%d_%m_%Y")
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    tipo_papel = "acoes" # Tipo de papel pode assumir os tipos ('acoes' ou 'fiis').
    
    d_base = "./dados/"
    d_extraidos = f"{d_base}01_extraidos/"
    d_processados = f"{d_base}02_processados/"
    dfinal = f"{d_base}03_final/"
    
    scraping = Scraping()

    if scraping:
        Utils.criar_diretorios()
        lista_papeis = scraping.retornar_lista_papeis(tipo=tipo_papel, diretorio=d_extraidos,
                                                      nome_do_arquivo=f'lista_de_{tipo_papel}_')

        # Descomentar a linha abaixo se dejar usar a lista de papeis salvos no lugar de extrair novamente.
        # dados_papeis = scraping.coleta_indicadores_de_ativos(f"{d_extraidos}lista_de_{tipo_papel}_{data_atual}.csv")
        dados_papeis = scraping.coleta_indicadores_de_ativos(lista_papeis)
        
        dados_processados = scraping.salvar_dataframe_como_csv(dados_papeis, tipo_papel,
                                                               diretorio=d_processados,
                                                               nome_do_arquivo=f'{tipo_papel}_consolidados_')
        
        # Filtrando apenas os registros que a data de cotação está atualizada, para trabalhar apenas com as ações ATIVAS
        dados_filtrados = pd.read_csv(f"{d_processados}{tipo_papel}_consolidados_{data_atual}.csv")
        dados_filtrados['dt_ult_cot'] = pd.to_datetime(dados_filtrados['dt_ult_cot'], format='%d/%m/%Y',
                                                       errors='coerce')
        dados_filtrados = dados_filtrados.dropna(subset=['dt_ult_cot'])

        dados_filtrados = dados_filtrados[(dados_filtrados['dt_ult_cot'].dt.month == mes_atual) &
                                          (dados_filtrados['dt_ult_cot'].dt.year == ano_atual)]

        scraping.salvar_dataframe_como_csv(dados_filtrados, tipo_papel, diretorio=d_processados,
                                           nome_do_arquivo=f'{tipo_papel}_consolidados_tratados_')

        dados_filtrados_renomeado = Utils.renomear_colunas(dados_filtrados, tipo_papel)

        scraping.salvar_dataframe_como_csv(dados_filtrados_renomeado, tipo_papel, diretorio=d_processados,
                                           nome_do_arquivo=f'{tipo_papel}_consolidados_tratados_renomeados_')
        
        if tipo_papel == "acoes":
            ModelGrahan().model_grahan()
            MagicForm().magic_form()
            ModelBazin().model_bazin()
            CsvParaPdf().gerar_pdf_de_csv()
            logging.info(f"Processamento dos dados de {tipo_papel} finalizado!")
        else:
                logging.info(f"Processamento dos dados de {tipo_papel} finalizado!")
    else:
        logging.info("Erro ao realizar o processamento dos dados")
